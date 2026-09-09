"""Source-vintage and retrieval audit for a historical snapshot."""
from datetime import datetime, timedelta, timezone


def audit_sources(manifest, records, now=None, max_snapshot_age_days=30):
    """Freshness is a declared review policy, never an Elexon availability SLA.

    Historical observation age is informational. A snapshot older than 30 days
    warrants revision review, but does not invalidate historical calculations.
    """
    now = now or datetime.now(timezone.utc)
    checks=[]
    def add(control,status,detail):
        checks.append(dict(control=control,status=status,detail=detail))
    requests=manifest.get('requests',[])
    failed=sum(r.get('status')!='success' for r in requests)
    add('retrieval_status','FAIL' if failed else 'PASS',f'{len(requests)} requests; {failed} failed')
    schemas={tuple(r.get('source_fields',[])) for r in requests if r.get('status')=='success'}
    add('source_schema_drift','REVIEW' if len(schemas)>1 else 'PASS',f'{len(schemas)} source field signatures across daily responses')
    invalid,after_retrieval,before_period=0,0,0
    for row in records:
        try:
            created=datetime.fromisoformat(row['createdDateTime'].replace('Z','+00:00'))
            retrieved=datetime.fromisoformat(row['retrieved_at'].replace('Z','+00:00'))
            start=datetime.fromisoformat(row['startTime'].replace('Z','+00:00'))
            if any(t.tzinfo is None or t.utcoffset()!=timedelta(0) for t in [created,retrieved,start]):
                raise ValueError('Timestamp lacks UTC offset')
            after_retrieval+=created>retrieved
            before_period+=created<start
        except (KeyError,ValueError,TypeError):
            invalid+=1
    add('source_timestamp_schema','FAIL' if invalid else 'PASS',f'{invalid} missing/malformed/non-UTC source timestamps')
    add('source_created_before_retrieved','FAIL' if after_retrieval else 'PASS',f'{after_retrieval} source timestamps after retrieval')
    add('source_created_after_period_start','REVIEW' if before_period else 'PASS',f'{before_period} source timestamps preceding period start')
    try:
        retrieved=datetime.fromisoformat(manifest['retrieved_at'])
        if retrieved.tzinfo is None:
            raise ValueError('Naive retrieval time')
        age=(now-retrieved).total_seconds()/86400
        status='FAIL' if age<0 else 'REVIEW' if age>max_snapshot_age_days else 'PASS'
        add('snapshot_revision_review',status,f'Snapshot age {age:.2f} days; analyst review policy {max_snapshot_age_days} days')
    except (KeyError,ValueError,TypeError):
        add('snapshot_revision_review','FAIL','Invalid retrieval timestamp')
    add('historical_scope','INFO',f"Historical data through {manifest['end_date']}; not a current service-availability measurement")
    return checks
