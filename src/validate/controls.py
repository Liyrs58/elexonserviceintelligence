"""Validate without repairing, imputing, or silently discarding observations.

validate_records returns a list of exception dictionaries. Empty means all supplied
records and every expected key pass. Counts may be summarized by control/severity;
one record can generate multiple exceptions. Dates are inclusive. All controls
currently have error severity. A malformed window raises ValueError.
"""
from collections.abc import Mapping
from datetime import date, datetime, time, timedelta, timezone
import math
from numbers import Real
from zoneinfo import ZoneInfo

LONDON = ZoneInfo('Europe/London')
REQUIRED = ('settlement_date', 'settlement_period', 'start_time', 'system_price', 'niv')


def _date(value):
    if type(value) is date:
        return value
    if not isinstance(value, str):
        raise ValueError('Expected ISO YYYY-MM-DD date')
    parsed = date.fromisoformat(value)
    if value != parsed.isoformat():
        raise ValueError('Expected ISO YYYY-MM-DD date')
    return parsed


def _midnight(day):
    return datetime.combine(day, time(), LONDON).astimezone(timezone.utc)


def expected_periods(day):
    """Return 46, 48 or 50 half-hours between adjacent local midnights."""
    day = _date(day)
    return int((_midnight(day + timedelta(days=1)) - _midnight(day)).total_seconds() / 1800)


def expected_start(day, sp):
    """Return aware UTC datetime, rejecting invalid settlement-period indices."""
    day = _date(day)
    if type(sp) is not int or not 1 <= sp <= expected_periods(day):
        raise ValueError('Settlement period outside local-day calendar')
    return _midnight(day) + timedelta(minutes=30 * (sp - 1))


def system_length(niv):
    """Strict numeric classification; callers must handle missing values explicitly."""
    if isinstance(niv, bool) or not isinstance(niv, Real):
        raise TypeError('NIV must be numeric')
    if not math.isfinite(niv):
        raise ValueError('NIV must be finite')
    return 'Short' if niv > 0 else 'Long' if niv < 0 else 'Balanced'


def validate_records(records, start_date, end_date):
    """Return machine-readable exceptions, retaining duplicate/conflict evidence.

    Keys have control, severity, settlement_date, settlement_period, detail, and
    row_index (zero-based; None for absent expected records). Completeness counts
    presence of a valid business key, independent of value validity. Therefore a
    present null-valued price produces a null exception, not a missing-period one.
    start_time must be a timezone-aware ISO string with zero UTC offset.
    """
    start, end = _date(start_date), _date(end_date)
    if start > end:
        raise ValueError('start_date must not exceed end_date')
    issues, seen_keys, seen_rows = [], {}, {}

    def add(control, detail, day=None, sp=None, row=None):
        issues.append(dict(control=control, severity='error', settlement_date=day,
                           settlement_period=sp, detail=detail, row_index=row))

    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            add('required_schema', 'Record must be a mapping', row=index)
            continue
        # repr permits reporting malformed nested/unhashable values as well.
        fingerprint = tuple(sorted((str(k), repr(v)) for k, v in record.items()))
        if fingerprint in seen_rows:
            add('duplicate_row', f'Exact record duplicate of row {seen_rows[fingerprint]}',
                record.get('settlement_date'), record.get('settlement_period'), index)
        else:
            seen_rows[fingerprint] = index
        missing = [field for field in REQUIRED if field not in record]
        raw_day, sp = record.get('settlement_date'), record.get('settlement_period')
        if missing:
            add('required_schema', 'Missing fields: ' + ', '.join(missing), raw_day, sp, index)
        for field in REQUIRED:
            if field in record and record[field] is None:
                add('null_value', f'{field} is null', raw_day, sp, index)
        for field in ('system_price', 'niv'):
            value = record.get(field)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, Real):
                add('type_error', f'{field} must be numeric', raw_day, sp, index)
            elif not math.isfinite(value):
                add('nonfinite_value', f'{field} must be finite', raw_day, sp, index)
        try:
            if not isinstance(raw_day, str):
                raise ValueError('Date field must be ISO string')
            day = _date(raw_day)
        except (ValueError, TypeError):
            add('invalid_date', 'settlement_date must be ISO YYYY-MM-DD',
                raw_day if isinstance(raw_day, str) else None, sp, index)
            continue
        if not start <= day <= end:
            add('date_out_of_range', 'Date outside requested inclusive window', raw_day, sp, index)
        if type(sp) is not int:
            add('type_error', 'settlement_period must be an integer', raw_day, sp, index)
            continue
        if not 1 <= sp <= expected_periods(day):
            add('unexpected_period', 'Period outside DST-aware calendar', raw_day, sp, index)
            continue
        key = (raw_day, sp)
        if key in seen_keys:
            add('duplicate_key', f'Business key duplicate of row {seen_keys[key]}', raw_day, sp, index)
        else:
            seen_keys[key] = index
        value = record.get('start_time')
        try:
            if not isinstance(value, str):
                raise ValueError('Timestamp must be ISO string')
            timestamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if timestamp.tzinfo is None or timestamp.utcoffset() != timedelta(0):
                raise ValueError('Timestamp must carry UTC offset')
        except (ValueError, TypeError):
            add('invalid_timestamp', 'start_time must be an aware UTC ISO timestamp', raw_day, sp, index)
        else:
            expected = expected_start(day, sp)
            if timestamp != expected:
                add('utc_mismatch', f'Expected {expected.isoformat()}, received {value}', raw_day, sp, index)
    day = start
    while day <= end:
        for sp in range(1, expected_periods(day) + 1):
            if (day.isoformat(), sp) not in seen_keys:
                add('missing_period', 'Expected business key absent', day.isoformat(), sp)
        day += timedelta(days=1)
    return issues
