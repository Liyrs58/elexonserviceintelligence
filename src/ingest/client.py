"""Bounded public Elexon retrieval into unique, immutable snapshots."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import logging
from pathlib import Path
import time
import uuid
import requests

BASE = 'https://data.elexon.co.uk/bmrs/api/v1'
CORE = {'settlementDate','settlementPeriod','startTime','systemBuyPrice','systemSellPrice','netImbalanceVolume'}
LOG = logging.getLogger(__name__)


def parse_daily(payload: dict) -> list[dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get('data'), list):
        raise ValueError('Malformed data envelope')
    if not payload['data']:
        raise ValueError('Empty data response')
    for row in payload['data']:
        if not isinstance(row, dict) or not CORE <= row.keys():
            raise ValueError('Missing required source schema')
    return payload['data']


def get_response(session, url: str, sleeper=time.sleep):
    for attempt in range(1,4):
        try:
            response = session.get(url, timeout=(10,60))
            if response.status_code == 429 or response.status_code >= 500:
                if attempt == 3:
                    response.raise_for_status()
                try:
                    delay = min(30,max(0,float(response.headers.get('Retry-After',2**attempt))))
                except ValueError:
                    delay = 2**attempt
                sleeper(delay)
                continue
            response.raise_for_status()
            return response, attempt
        except (requests.ConnectionError, requests.Timeout):
            if attempt == 3:
                raise
            sleeper(2**attempt)
    raise RuntimeError('Retry budget exhausted')


def write_new(path: Path, content: bytes):
    with path.open('xb') as handle:
        handle.write(content)


def fetch_window(start_date: str, end_date: str, raw_root: Path) -> Path:
    start,end = date.fromisoformat(start_date),date.fromisoformat(end_date)
    if start>end:
        raise ValueError('Invalid date window')
    snapshot = raw_root / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    snapshot.mkdir(parents=True,exist_ok=False)
    manifest = dict(start_date=start_date,end_date=end_date,source_basis='DISEBSP latest settlement-run message',
                    retrieved_at=datetime.now(timezone.utc).isoformat(),requests=[],status='running')
    failed=False
    with requests.Session() as session:
        day=start
        while day<=end:
            url=f'{BASE}/balancing/settlement/system-prices/{day}?format=json'
            entry=dict(settlement_date=str(day),url=url,retrieved_at=datetime.now(timezone.utc).isoformat())
            began=time.monotonic()
            try:
                response,attempts=get_response(session,url)
                filename=f'{day}.json'
                write_new(snapshot/filename,response.content)
                entry.update(file=filename,sha256=hashlib.sha256(response.content).hexdigest(),
                             http_status=response.status_code,attempts=attempts)
                rows=parse_daily(response.json())
                entry.update(records=len(rows),status='success',source_fields=sorted(rows[0]))
            except (requests.RequestException,ValueError) as error:
                entry.update(status='failed',error=str(error))
                failed=True
            entry['elapsed_seconds']=round(time.monotonic()-began,3)
            manifest['requests'].append(entry)
            LOG.info('%s %s %s',day,entry['status'],entry.get('records',''))
            day+=timedelta(days=1)
    manifest['status']='failed' if failed else 'success'
    manifest['finished_at']=datetime.now(timezone.utc).isoformat()
    path=snapshot/'manifest.json'
    write_new(path,json.dumps(manifest,indent=2).encode())
    if failed:
        raise RuntimeError(f'Retrieval incomplete; inspect {path}')
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--start',required=True)
    parser.add_argument('--end',required=True)
    parser.add_argument('--raw-root',type=Path,default=Path('data/raw'))
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    print(fetch_window(args.start,args.end,args.raw_root))
