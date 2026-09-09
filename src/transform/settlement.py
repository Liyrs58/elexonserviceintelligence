"""Deterministic source mapping; raw records are never mutated."""
import pandas as pd
from src.validate.controls import system_length


def transform_records(records: list[dict]) -> pd.DataFrame:
    rows = []
    for source in records:
        if source['systemBuyPrice'] != source['systemSellPrice']:
            raise ValueError('Buy/Sell prices differ; single-price interpretation requires review')
        row = dict(source)
        row.update(settlement_date=source['settlementDate'],
                   settlement_period=source['settlementPeriod'], start_time=source['startTime'],
                   system_price=source['systemBuyPrice'], niv=source['netImbalanceVolume'])
        row['system_length'] = system_length(row['niv'])
        row['absolute_niv'] = abs(row['niv'])
        row['local_start'] = pd.Timestamp(row['start_time']).tz_convert('Europe/London').isoformat()
        row['event_id'] = f"{row['settlement_date']} SP{row['settlement_period']:02d}"
        rows.append(row)
    return pd.DataFrame(rows).sort_values(['settlement_date','settlement_period']).reset_index(drop=True)
