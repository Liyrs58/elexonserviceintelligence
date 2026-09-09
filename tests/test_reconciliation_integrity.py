import json
import hashlib
import pytest
from src.analysis.reconcile import reconcile
from src.pipeline import run


def test_reconciliation_rejects_changed_context(tmp_path):
    (tmp_path/'run.json').write_text('{"status":"success"}')
    context = tmp_path/'raw'
    context.mkdir()
    (context/'x.json').write_text('{}')
    (context/'manifest.json').write_text(json.dumps([dict(status='success',file='x.json',sha256='wrong')]))
    (tmp_path/'investigations.json').write_text(json.dumps([dict(context_snapshot=str(context),settlement_date='2025-10-13',settlement_period=26)]))
    with pytest.raises(ValueError,match='integrity'):
        reconcile(tmp_path)


def test_reconciliation_is_idempotent(tmp_path):
    (tmp_path/'run.json').write_text('{"status":"success"}')
    context=tmp_path/'raw'
    context.mkdir()
    summary=dict(adjuster='0',createdDateTime='2025-10-14T00:00:00Z')
    stack=dict(data=[dict(parAdjustedVolume=1,tlmAdjustedVolume=1,
                         tlmAdjustedCost=487,createdDateTime=summary['createdDateTime'])])
    receipts=[]
    for kind,payload in [('summary',summary),('bid',dict(data=[])),('offer',stack)]:
        filename=f'2025-10-13-SP26-{kind}.json'
        content=json.dumps(payload).encode()
        (context/filename).write_bytes(content)
        receipts.append(dict(file=filename,status='success',sha256=hashlib.sha256(content).hexdigest()))
    (context/'manifest.json').write_text(json.dumps(receipts))
    cases=[dict(context_snapshot=str(context),settlement_date='2025-10-13',settlement_period=26,
                event_id='2025-10-13 SP26',niv=100,system_price=487,known='OBSERVED: price 487.')]
    (tmp_path/'investigations.json').write_text(json.dumps(cases))
    reconcile(tmp_path)
    first=(tmp_path/'investigations.json').read_bytes()
    reconcile(tmp_path)
    assert (tmp_path/'investigations.json').read_bytes()==first


def test_failed_refresh_invalidates_previous_success(tmp_path):
    output=tmp_path/'processed'
    output.mkdir()
    (output/'run.json').write_text('{"status":"success"}')
    manifest=tmp_path/'manifest.json'
    manifest.write_text('{"status":"failed"}')
    with pytest.raises(ValueError,match='incomplete'):
        run(manifest,output)
    status=json.loads((output/'run.json').read_text())
    assert status['status']=='failed'
    assert 'incomplete' in status['error']
