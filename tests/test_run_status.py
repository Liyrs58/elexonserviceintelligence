import json
import pytest
from src.analysis.investigate import investigate
from src.analysis.reconcile import reconcile
from src.analysis.investigation_queue import build


@pytest.mark.parametrize('consumer',['investigate','reconcile','queue'])
@pytest.mark.parametrize('status',['failed','running','missing','malformed'])
def test_consumers_reject_unusable_run(tmp_path,monkeypatch,consumer,status):
    processed=tmp_path/'data'/'processed'
    processed.mkdir(parents=True)
    if status!='missing':
        (processed/'run.json').write_text('{' if status=='malformed' else json.dumps(dict(status=status)))
    monkeypatch.chdir(tmp_path)
    action={'investigate':lambda:investigate(processed,tmp_path/'raw'),
            'reconcile':lambda:reconcile(processed),'queue':build}[consumer]
    with pytest.raises(ValueError,match='successful pipeline run'):
        action()
    assert not (tmp_path/'raw').exists()
