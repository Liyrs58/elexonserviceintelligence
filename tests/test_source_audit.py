from datetime import datetime,timezone
from src.validate.source_audit import audit_sources


def test_schema_change_and_stale_snapshot_are_review_items():
    manifest=dict(end_date='2025-12-31',retrieved_at='2026-01-01T00:00:00+00:00',requests=[
        dict(status='success',source_fields=['a']),dict(status='success',source_fields=['a','b'])])
    checks={x['control']:x['status'] for x in audit_sources(manifest,[],datetime(2026,3,1,tzinfo=timezone.utc))}
    assert checks['source_schema_drift']=='REVIEW'
    assert checks['snapshot_revision_review']=='REVIEW'
    assert checks['historical_scope']=='INFO'


def test_future_source_creation_and_naive_timestamps_fail():
    manifest=dict(end_date='2025-12-31',retrieved_at='2026-01-01T00:00:00+00:00',requests=[])
    rows=[dict(createdDateTime='2026-01-02T00:00:00Z',retrieved_at=manifest['retrieved_at'],startTime='2025-12-31T00:00:00Z'),
          dict(createdDateTime='2026-01-01',retrieved_at=manifest['retrieved_at'],startTime='2025-12-31T00:00:00Z')]
    checks={x['control']:x['status'] for x in audit_sources(manifest,rows,datetime(2026,1,2,tzinfo=timezone.utc))}
    assert checks['source_created_before_retrieved']=='FAIL'
    assert checks['source_timestamp_schema']=='FAIL'
