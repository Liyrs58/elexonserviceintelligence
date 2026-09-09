"""Reconcile downloaded price evidence without refetching or changing raw files."""
from decimal import Decimal
import json
from pathlib import Path
import pandas as pd


def reconcile(processed=Path('data/processed')):
    cases=json.loads((processed/'investigations.json').read_text())
    output=[]
    for case in cases:
        root=Path(case['context_snapshot'])
        stem=f"{case['settlement_date']}-SP{case['settlement_period']:02}"
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
        if match and aligned:
            case['known']+=f' DERIVED: {len(retained)} retained {side} rows reconstruct GBP {calculated:.2f}/MWh from transmission-loss-adjusted cost/volume and the source adjuster. Stack and summary creation times agree.'
            case['investigation_status']='Price-mechanism reconciliation passed; underlying cause not established'
            case['recommended_next_checks']='Review why the retained actions were accepted using official balancing-action and targeted demand/generation evidence. Confirm source vintages before extending attribution; check incident history only if a data-control exception emerges.'
    pd.DataFrame(output).to_csv(processed/'price_reconciliation.csv',index=False)
    (processed/'investigations.json').write_text(json.dumps(cases,indent=2))
    pd.DataFrame(cases).to_csv(processed/'investigations.csv',index=False)
    print(pd.DataFrame(output).to_string(index=False))


if __name__=='__main__':reconcile()
