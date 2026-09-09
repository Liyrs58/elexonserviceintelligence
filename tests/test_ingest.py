from unittest.mock import Mock
import pytest
import requests
from src.ingest.client import get_response,parse_daily,write_new


def test_envelope_fails_closed():
    for payload in [[],{}, {'data':[]},{'data':[{}]}]:
        with pytest.raises(ValueError): parse_daily(payload)


def test_retry_transient_then_success():
    session=Mock()
    busy=Mock(status_code=429,headers={'Retry-After':'0'})
    good=Mock(status_code=200)
    session.get.side_effect=[busy,good]
    sleep=Mock()
    response,attempts=get_response(session,'https://example.test',sleep)
    assert response is good and attempts==2
    sleep.assert_called_once_with(0)


def test_no_retry_permanent_http_failure():
    session=Mock()
    session.get.return_value.status_code=400
    session.get.return_value.raise_for_status.side_effect=requests.HTTPError('400')
    with pytest.raises(requests.HTTPError):get_response(session,'https://example.test',Mock())
    assert session.get.call_count==1


def test_connection_failure_is_bounded():
    session=Mock()
    session.get.side_effect=requests.Timeout('timeout')
    with pytest.raises(requests.Timeout):get_response(session,'https://example.test',Mock())
    assert session.get.call_count==3


def test_raw_file_cannot_be_overwritten(tmp_path):
    path=tmp_path/'raw.json'
    write_new(path,b'original')
    with pytest.raises(FileExistsError):write_new(path,b'changed')
    assert path.read_bytes()==b'original'
