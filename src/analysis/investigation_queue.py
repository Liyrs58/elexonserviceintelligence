"""Expand the review queue without pretending all cases were investigated."""
import json
from pathlib import Path
import pandas as pd
from src.validate.run_status import require_successful_run

def build():
    root=Path('data/processed')
    require_successful_run(root)
    frame=pd.read_csv(root/'settlement.csv')
    reviewed={r['event_id']:r for r in json.loads((root/'investigations.json').read_text())}
    rows=[]
    for _,r in frame[frame.is_exception].iterrows():
        record=dict(event_id=r.event_id,settlement_date=r.settlement_date,
          what_happened=f'Price {r.system_price:.2f} GBP/MWh; NIV {r.niv:.2f} MWh; {r.system_length}.',
          reason_flagged=r.reason_flagged,quality_control_result=r.quality_status,
          known=f'OBSERVED source price and NIV. DERIVED price percentile {r.price_percentile:.2f}; absolute-NIV percentile {r.niv_percentile:.2f}.',
          not_established='Cause, service incident linkage and detailed price mechanism have not been established for this case.',
          hypotheses='No case-specific hypothesis assessed yet.',
          recommended_next_checks='Inspect official summary and both price stacks for this date/period; align creation times and reconcile before assessing broader context.',
          investigation_status='Queued; Level 1 screening only')
        if r.event_id in reviewed:
            record.update(reviewed[r.event_id])
        rows.append(record)
    pd.DataFrame(rows).to_csv(root/'investigation_queue.csv',index=False)
    print(f'{len(rows)} investigation records, {len(reviewed)} with detailed evidence')

if __name__=='__main__':build()
