from datetime import datetime, timezone

import pytest

from src.validate.controls import expected_periods, expected_start, system_length, validate_records


def complete(day):
    return [dict(settlement_date=day, settlement_period=sp,
                 start_time=expected_start(day, sp).isoformat(), system_price=-1.5, niv=0.0)
            for sp in range(1, expected_periods(day) + 1)]


def codes(rows, start='2025-01-01', end='2025-01-01'):
    return {item['control'] for item in validate_records(rows, start, end)}


@pytest.mark.parametrize('day,count', [('2025-01-01',48),('2025-03-30',46),('2025-10-26',50)])
def test_calendar_and_clean_records(day,count):
    assert expected_periods(day) == count
    assert validate_records(complete(day), day, day) == []


def test_repeated_clock_hour_and_summer_midnight():
    assert expected_start('2025-10-26',3) == datetime(2025,10,26,0,tzinfo=timezone.utc)
    assert expected_start('2025-10-26',5) == datetime(2025,10,26,1,tzinfo=timezone.utc)
    assert expected_start('2025-07-01',1) == datetime(2025,6,30,23,tzinfo=timezone.utc)
    with pytest.raises(ValueError): expected_start('2025-03-30',47)


def test_lengths():
    assert [system_length(x) for x in [-2,0,2]] == ['Long','Balanced','Short']
    for value in [None, True, '2', float('nan'),float('inf')]:
        with pytest.raises((TypeError,ValueError)): system_length(value)


def test_missing_null_duplicate_and_schema():
    rows=complete('2025-01-01')
    rows.pop()
    rows[0]['niv']=None
    rows.append(dict(rows[1]))
    rows.append({'settlement_date':'2025-01-01'})
    found=codes(rows)
    assert {'missing_period','null_value','duplicate_row','duplicate_key','required_schema'} <= found


def test_conflicting_duplicate_key_is_visible():
    rows=complete('2025-01-01')
    extra=dict(rows[0],system_price=99)
    rows.append(extra)
    assert 'duplicate_key' in codes(rows)
    assert 'duplicate_row' not in codes(rows)


def test_bad_values_and_dates():
    rows=complete('2025-01-01')
    rows[0]['system_price']=float('inf')
    rows[1]['niv']='2'
    rows[2]['settlement_period']=49
    rows[3]['settlement_date']='2025-01-02'
    rows[4]['start_time']='2025-01-01T04:00:00Z'
    rows[5]['start_time']='2025-01-01T02:30:00'
    rows[6]['settlement_date']='not-a-date'
    rows[7]['settlement_period']=True
    assert {'nonfinite_value','type_error','unexpected_period','date_out_of_range',
            'utc_mismatch','invalid_timestamp','invalid_date'} <= codes(rows)


def test_empty_data_and_invalid_window():
    events=validate_records([], '2025-03-30','2025-03-30')
    assert len(events)==46
    assert all(e['control']=='missing_period' and e['severity']=='error' for e in events)
    with pytest.raises(ValueError): validate_records([], '2025-01-02','2025-01-01')


def test_issue_contract():
    issue=validate_records([None], '2025-01-01','2025-01-01')[0]
    assert set(['control','severity','settlement_date','settlement_period','detail']) <= issue.keys()
