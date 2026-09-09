"""Reconcile downloaded price evidence without refetching or changing raw files."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import pandas as pd
from src.validate.run_status import require_successful_run


def reconcile(processed=Path('data/processed')):
    require_successful_run(processed)
    cases=json.loads((processed/'investigations.json').read_text())
    output=[]
    for case in cases:
        root=Path(case['context_snapshot'])
        # A context snapshot has the same immutable-byte contract as core data.
        receipts=json.loads((root/'manifest.json').read_text())
        if not receipts or any(r.get('status')!='success' for r in receipts):
            raise ValueError('Context snapshot integrity: incomplete retrieval')
        verified=set()
        for receipt in receipts:
            content=(root/receipt['file']).read_bytes()
            if hashlib.sha256(content).hexdigest()!=receipt['sha256']:
                raise ValueError('Context snapshot integrity failure')
            verified.add(receipt['file'])
        stem=f"{case['settlement_date']}-SP{case['settlement_period']:02}"
        if not {f'{stem}-summary.json',f'{stem}-bid.json',f'{stem}-offer.json'} <= verified:
            raise ValueError('Context snapshot integrity: missing case evidence')
        summary=json.loads((root/f'{stem}-summary.json').read_text())
        side='offer' if case['niv']>0 else 'bid'
        stack=json.loads((root/f'{stem}-{side}.json').read_text())['data']
        retained=[r for r in stack if r.get('parAdjustedVolume') not in (None,0)]
        volume=sum(Decimal(str(r['tlmAdjustedVolume'])) for r in retained)
        cost=sum(Decimal(str(r['tlmAdjustedCost'])) for r in retained)
        calculated=cost/volume+Decimal(summary['adjuster']) if volume else None
        match=calculated is not None and abs(calculated-Decimal(str(case['system_price'])))<Decimal('.005')
        aligned=all(r['createdDateTime']==summary['createdDateTime'] for r in retained)
        output.append(dict(event_id=case['event_id'],side=side,retained_rows=len(retained),
            retained_par_volume=sum(float(r['parAdjustedVolume']) for r in retained),
            tlm_adjusted_volume=float(volume),tlm_adjusted_cost=float(cost),
            adjuster=summary['adjuster'],reconstructed_price=float(calculated) if calculated is not None else None,
            source_price=case['system_price'],matches_to_penny=match,
            stack_summary_creation_aligned=aligned,created_at=summary['createdDateTime']))
        # Replace generated commentary, including older outputs, instead of
        # accumulating another sentence on every deterministic rebuild.
        case['known']=re.sub(r' DERIVED: \d+ retained (?:bid|offer) rows reconstruct .*?Stack and summary creation times agree\.', '', case['known'])
        case['investigation_status']='Price-mechanism reconciliation requires review; underlying cause not established'
        case['recommended_next_checks']='Review unmatched price or creation timestamps before extending attribution.'
        if match and aligned:
            case['known']+=f' DERIVED: {len(retained)} retained {side} rows reconstruct GBP {calculated:.2f}/MWh from transmission-loss-adjusted cost/volume and the source adjuster. Stack and summary creation times agree.'
            case['investigation_status']='Price-mechanism reconciliation passed; underlying cause not established'
            case['recommended_next_checks']='Review why the retained actions were accepted using official balancing-action and targeted demand/generation evidence. Confirm source vintages before extending attribution; check incident history only if a data-control exception emerges.'
    pd.DataFrame(output).to_csv(processed/'price_reconciliation.csv',index=False)
    (processed/'investigations.json').write_text(json.dumps(cases,indent=2))
    pd.DataFrame(cases).to_csv(processed/'investigations.csv',index=False)
    print(pd.DataFrame(output).to_string(index=False))


if __name__=='__main__':reconcile()
