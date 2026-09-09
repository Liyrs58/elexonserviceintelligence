"""Rebuild analysis from a named immutable retrieval manifest."""
import argparse
from datetime import date,datetime,timedelta,timezone
import hashlib
import json
from pathlib import Path
import duckdb
import pandas as pd
from src.ingest.client import parse_daily
from src.transform.settlement import transform_records
from src.validate.controls import expected_periods,validate_records
from src.analysis.statistics import analyse,flag_periods
from src.validate.source_audit import audit_sources


def run(manifest_path: Path, output: Path, quality: Path | None = None):
    manifest=json.loads(manifest_path.read_text())
    if manifest['status']!='success':
        raise ValueError('Cannot analyse incomplete ingestion')
    output.mkdir(parents=True,exist_ok=True)
    quality=quality or output.parent/'quality'
    quality.mkdir(parents=True,exist_ok=True)
    originals=[]
    for request in manifest['requests']:
        content=(manifest_path.parent/request['file']).read_bytes()
        if hashlib.sha256(content).hexdigest()!=request['sha256']:
            raise ValueError('Raw snapshot integrity failure')
        for source in parse_daily(json.loads(content)):
            originals.append(dict(source,source_endpoint=request['url'],retrieved_at=request['retrieved_at']))
    source_checks=audit_sources(manifest,originals)
    pd.DataFrame(source_checks).to_csv(quality/'source_controls.csv',index=False)
    # Validate core values before transformations could coerce or hide invalid types.
    canonical=[dict(settlement_date=r.get('settlementDate'),settlement_period=r.get('settlementPeriod'),
                    start_time=r.get('startTime'),system_price=r.get('systemBuyPrice'),
                    niv=r.get('netImbalanceVolume')) for r in originals]
    issues=validate_records(canonical,manifest['start_date'],manifest['end_date'])
    for index,row in enumerate(originals):
        if row.get('systemBuyPrice')!=row.get('systemSellPrice'):
            issues.append(dict(control='buy_sell_mismatch',severity='error',row_index=index,
                               settlement_date=row.get('settlementDate'),settlement_period=row.get('settlementPeriod'),
                               detail='Single System Price cannot be established'))
    columns=['control','severity','settlement_date','settlement_period','detail','row_index']
    pd.DataFrame(issues,columns=columns).to_csv(quality/'exceptions.csv',index=False)
    (quality/'exceptions.json').write_text(json.dumps(issues,indent=2))
    if issues or any(c['status']=='FAIL' for c in source_checks):
        raise ValueError(f'{len(issues)} validation exceptions; inspect {quality}')
    frame=transform_records(originals)
    frame,thresholds=flag_periods(frame)
    frame['quality_status']='PASS'
    # Deterministic bins are display groups, not exception thresholds.
    frame['price_bin_lower']=(frame.system_price//20*20).astype(int)
    frame['niv_bin_lower']=(frame.niv//100*100).astype(int)
    frame.to_csv(output/'settlement.csv',index=False)
    expected=[]
    day=date.fromisoformat(manifest['start_date'])
    while day<=date.fromisoformat(manifest['end_date']):
        expected.append(dict(settlement_date=str(day),expected_periods=expected_periods(day),
                             year=day.year,month=day.month,month_name=day.strftime('%B'),
                             weekday=day.strftime('%A'),clock_change=expected_periods(day)!=48))
        day+=timedelta(days=1)
    dates=pd.DataFrame(expected)
    dates.to_csv(output/'dates.csv',index=False)
    pd.DataFrame({'settlement_period':range(1,51)}).to_csv(output/'periods.csv',index=False)
    daily=frame.groupby('settlement_date').agg(received_periods=('settlement_period','size')).reset_index()
    daily=dates.merge(daily,on='settlement_date',how='left').fillna({'received_periods':0})
    daily['missing_periods']=daily.expected_periods-daily.received_periods
    daily['completeness']=daily.received_periods/daily.expected_periods
    daily['validation_exceptions']=0
    daily['duplicate_periods']=0
    daily['null_values']=0
    daily['schema_exceptions']=0
    daily['retrieval_status']='Success'
    daily.to_csv(quality/'daily_controls.csv',index=False)
    frame[['system_price','niv','absolute_niv']].describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]).to_csv(output/'descriptive_statistics.csv')
    frame.groupby('price_bin_lower').size().rename('periods').to_csv(output/'price_distribution.csv')
    frame.groupby('niv_bin_lower').size().rename('periods').to_csv(output/'niv_distribution.csv')
    metadata=[]
    for field in frame.columns:
        evidence='OBSERVED' if field in originals[0] else 'FLAG' if field in ['price_flag','imbalance_flag','is_exception','reason_flagged','severity','quality_status'] else 'DERIVED'
        metadata.append(dict(field=field,evidence_class=evidence,definition='Original source or retrieval field' if evidence=='OBSERVED' else 'See METHODOLOGY.md and source implementation'))
    pd.DataFrame(metadata).to_csv(output/'field_provenance.csv',index=False)
    statistics=analyse(frame)
    statistics.update(expected_records=int(dates.expected_periods.sum()),completeness=len(frame)/dates.expected_periods.sum(),
                      validation_exceptions=len(issues),start_date=manifest['start_date'],end_date=manifest['end_date'],
                      retrieved_at=manifest['retrieved_at'])
    con=duckdb.connect()
    con.register('settlement',frame)
    con.execute(Path('sql/analysis.sql').read_text())
    sql_summary=con.sql('SELECT * FROM summary').df().iloc[0].to_dict()
    comparison=[]
    for key,value in sql_summary.items():
        difference=abs(statistics[key]-value)
        if difference>1e-8:
            raise ValueError(f'Python/SQL mismatch {key}: {difference}')
        comparison.append(dict(metric=key,python_value=statistics[key],sql_value=value,absolute_difference=difference,status='PASS'))
    pd.DataFrame(comparison).to_csv(quality/'cross_system_validation.csv',index=False)
    for view in ['daily_summary','period_summary','length_summary','extreme_periods','exception_queue','duplicate_keys']:
        con.sql(f'SELECT * FROM {view}').df().to_csv(output/f'{view}.csv',index=False)
    con.execute('COPY settlement TO ? (FORMAT PARQUET)',[str(output/'settlement.parquet')])
    (output/'summary.json').write_text(json.dumps(statistics,indent=2,default=float))
    (output/'thresholds.json').write_text(json.dumps(thresholds,indent=2))
    (output/'run.json').write_text(json.dumps(dict(manifest=str(manifest_path.resolve()),
         manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
         built_at=datetime.now(timezone.utc).isoformat(),status='success'),indent=2))
    print(json.dumps(statistics,indent=2,default=float))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=Path('data/processed'))
    args=parser.parse_args()
    run(args.manifest,args.output)
