import pandas as pd
import pytest

from src.analysis.statistics import analyse, flag_periods
from src.transform.settlement import transform_records


def test_transform_preserves_observed_values_and_signed_length():
    row = {'settlementDate': '2025-10-26', 'settlementPeriod': 5,
           'startTime': '2025-10-26T01:00:00Z', 'systemBuyPrice': -12.5,
           'systemSellPrice': -12.5, 'netImbalanceVolume': -200.25}
    result = transform_records([row]).iloc[0]
    assert result.system_price == -12.5
    assert result.niv == -200.25
    assert result.system_length == 'Long'
    assert result.local_start == '2025-10-26T01:00:00+00:00'
    assert row['startTime'] == '2025-10-26T01:00:00Z'


def test_differing_buy_sell_prices_are_not_silently_collapsed():
    row = {'settlementDate': '2025-10-01', 'settlementPeriod': 1,
           'startTime': '2025-09-30T23:00:00Z', 'systemBuyPrice': 12,
           'systemSellPrice': 13, 'netImbalanceVolume': 20}
    with pytest.raises(ValueError, match='Buy/Sell'):
        transform_records([row])


def test_quantiles_use_linear_interpolation_and_inclusive_ties():
    frame = pd.DataFrame({'system_price': list(range(101)), 'niv': list(range(-50,51))})
    result, thresholds = flag_periods(frame)
    assert thresholds['price_p01'] == 1
    assert thresholds['price_p99'] == 99
    assert result.price_flag.sum() == 4
    assert result.imbalance_flag.sum() == 2
    assert result.price_percentile.iloc[-1] == 100


def test_constant_data_has_no_statistical_flags():
    result, _ = flag_periods(pd.DataFrame({'system_price': [5.0]*20, 'niv': [0.0]*20}))
    assert not result.is_exception.any()
    assert (result.price_robust_z == 0).all()


def test_independent_summary_known_values():
    frame = pd.DataFrame({'system_price': [0., 10., 20., 30.], 'niv': [-2., -1., 1., 2.],
                          'system_length': ['Long','Long','Short','Short']})
    flagged, _ = flag_periods(frame)
    summary = analyse(flagged)
    assert summary['records'] == 4
    assert summary['median_price'] == 15
    assert summary['maximum_absolute_niv'] == 2
    assert summary['short_periods'] == 2
