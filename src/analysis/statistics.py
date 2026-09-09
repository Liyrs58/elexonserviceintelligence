"""Descriptive screening, not prediction or causal attribution."""
import pandas as pd


def flag_periods(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    result = frame.copy()
    price, magnitude = result.system_price, result.niv.abs()
    low, high = price.quantile([.01,.99], interpolation='linear')
    large = magnitude.quantile(.99, interpolation='linear')
    median = price.median()
    mad = (price-median).abs().median()
    result['absolute_niv'] = magnitude
    result['price_percentile'] = price.rank(method='max',pct=True)*100
    result['niv_percentile'] = magnitude.rank(method='max',pct=True)*100
    # Equal-valued samples contain no tail evidence. Inclusive ties remain together.
    result['price_flag'] = ((price <= low) | (price >= high)) & (price.min() < price.max())
    result['imbalance_flag'] = (magnitude >= large) & (magnitude.min() < magnitude.max())
    result['is_exception'] = result.price_flag | result.imbalance_flag
    result['price_robust_z'] = (price-median)/(1.4826*mad) if mad > 0 else 0.0
    result['reason_flagged'] = result.apply(lambda r: '; '.join(
        label for yes,label in [(r.price_flag,'Price tail (1st/99th percentile)'),
                                (r.imbalance_flag,'Absolute NIV upper 1%')] if yes) or 'Within screening thresholds',axis=1)
    result['severity'] = result.apply(lambda r: 'Joint tail' if r.price_flag and r.imbalance_flag
                                     else 'Review' if r.is_exception else 'Normal',axis=1)
    return result, dict(price_p01=float(low),price_p99=float(high),absolute_niv_p99=float(large),
                        price_median=float(median),price_mad=float(mad),
                        basis='Full-window retrospective linear quantiles; inclusive ties; not an operational SLA')


def analyse(frame: pd.DataFrame) -> dict:
    return dict(records=len(frame),mean_price=float(frame.system_price.mean()),
                median_price=float(frame.system_price.median()),
                maximum_price=float(frame.system_price.max()),minimum_price=float(frame.system_price.min()),
                maximum_absolute_niv=float(frame.niv.abs().max()),
                short_periods=int((frame.system_length=='Short').sum()),
                long_periods=int((frame.system_length=='Long').sum()),
                balanced_periods=int((frame.system_length=='Balanced').sum()),
                negative_price_periods=int((frame.system_price<0).sum()),
                exception_periods=int(frame.is_exception.sum()),
                price_flag_periods=int(frame.price_flag.sum()),
                imbalance_flag_periods=int(frame.imbalance_flag.sum()),
                pearson_niv_price=float(frame.niv.corr(frame.system_price)),
                spearman_niv_price=float(frame.niv.rank().corr(frame.system_price.rank())))
