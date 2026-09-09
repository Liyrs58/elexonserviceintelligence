"""Retrieve official price-mechanism evidence for selected material cases."""
import argparse
from datetime import datetime,timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import uuid
import pandas as pd
import requests
from src.ingest.client import BASE,get_response,write_new


def investigate(processed: Path, raw_root: Path):
    frame=pd.read_csv(processed/'settlement.csv')
    selected=frame.loc[[frame.system_price.idxmax(),frame.system_price.idxmin(),frame.niv.abs().idxmax()]].drop_duplicates('event_id')
    snapshot=raw_root/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-context-'+uuid.uuid4().hex[:8])
    snapshot.mkdir(parents=True,exist_ok=False)
    audit,results=[],[]
    with requests.Session() as session:
        for _,row in selected.iterrows():
            day,sp=row.settlement_date,int(row.settlement_period)
            observed={}
            for name,path in [('summary',f'summary/{day}/{sp}'),('bid',f'stack/all/bid/{day}/{sp}'),('offer',f'stack/all/offer/{day}/{sp}')]:
                url=f'{BASE}/balancing/settlement/{path}?format=json'
                entry=dict(event_id=row.event_id,dataset=name,url=url,retrieved_at=datetime.now(timezone.utc).isoformat())
                try:
                    response,attempts=get_response(session,url)
                    filename=f'{day}-SP{sp:02}-{name}.json'
                    write_new(snapshot/filename,response.content)
                    payload=response.json()
                    observed[name]=payload
                    entry.update(status='success',http_status=response.status_code,attempts=attempts,file=filename,
                                 sha256=hashlib.sha256(response.content).hexdigest())
                except (requests.RequestException,ValueError) as error:
                    entry.update(status='failed',error=str(error))
                audit.append(entry)
            known=f"OBSERVED: System Price GBP {row.system_price:.2f}/MWh; NIV {row.niv:.2f} MWh. DERIVED: {row.system_length} system."
            reconciliation='Unavailable'
            summary=observed.get('summary',{})
            if summary:
                price=summary.get('systemBuyPrice')
                if isinstance(price,(str,int,float)):
                    matches=abs(Decimal(str(price))-Decimal(str(row.system_price)))<Decimal('.005')
                    reconciliation='Matches to GBP 0.01/MWh' if matches else 'VINTAGE MISMATCH: investigate before combining'
                    known+=f' Official calculation summary price {price}: {reconciliation}.'
            result=dict(event_id=row.event_id,settlement_date=day,settlement_period=sp,system_price=row.system_price,
                        niv=row.niv,system_length=row.system_length,price_percentile=row.price_percentile,
                        absolute_niv_percentile=row.niv_percentile,quality_control_result=row.quality_status,
                        reason_flagged=row.reason_flagged,evidence_available=', '.join(observed),known=known,
                        not_established='Underlying cause of the market condition; generator or demand causality; service incident attribution. Latest sources may have different calculation vintages.',
                        hypotheses='HYPOTHESIS: the prices of the remaining balancing actions may explain price severity better than the magnitude of NIV alone. Test using the priced stack.',
                        recommended_next_checks='Check summary and bid/offer stack creation times, PAR-adjusted volume and final prices; reconcile price before inspecting targeted demand/generation and incident context.',
                        investigation_status='Price evidence retrieved; reconciliation review pending',
                        summary_reconciliation=reconciliation,context_snapshot=str(snapshot))
            results.append(result)
    write_new(snapshot/'manifest.json',json.dumps(audit,indent=2).encode())
    (processed/'investigations.json').write_text(json.dumps(results,indent=2))
    pd.DataFrame(results).to_csv(processed/'investigations.csv',index=False)
    print(pd.DataFrame(results)[['event_id','summary_reconciliation','evidence_available']].to_string(index=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--processed',type=Path,default=Path('data/processed'))
    parser.add_argument('--raw-root',type=Path,default=Path('data/raw'))
    args=parser.parse_args()
    investigate(args.processed,args.raw_root)
