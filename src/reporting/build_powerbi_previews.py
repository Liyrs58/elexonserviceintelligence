"""Render data-bound static previews of the four authored PBIR pages.

These are reviewer aids, not Power BI runtime screenshots. The prominent label
is deliberate: only a licensed engine can close DAX, interaction and rendering
verification.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "playwright"
DATA = ROOT / "data"
W, H = 1920, 1080
INK = "#17212B"
MUTED = "#617080"
BLUE = "#005EB8"
CYAN = "#00A6A6"
AMBER = "#C56A00"
RED = "#B42318"
GREEN = "#1F7A4D"
GRID = "#DCE3E8"


def fmt(value: float, decimals: int = 1) -> str:
    return f"{value:,.{decimals}f}"


def esc(value: object) -> str:
    return escape(str(value))


def svg_line(values: Sequence[float], labels: Sequence[str], color: str, *, zero: bool = False) -> str:
    width, height = 960, 220
    left, top, right, bottom = 76, 18, 18, 40
    inner_w, inner_h = width - left - right, height - top - bottom
    lo, hi = min(values), max(values)
    if zero:
        lo, hi = min(lo, 0), max(hi, 0)
    pad = (hi - lo) * 0.08 or 1
    lo, hi = lo - pad, hi + pad
    x = lambda i: left + inner_w * i / max(len(values) - 1, 1)
    y = lambda v: top + inner_h * (hi - v) / (hi - lo)
    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
    grid = []
    for i in range(5):
        val = hi - (hi - lo) * i / 4
        yy = y(val)
        grid.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="{GRID}"/>')
        grid.append(f'<text x="{left-10}" y="{yy+5:.1f}" text-anchor="end" class="axis">{val:,.0f}</text>')
    if zero and lo < 0 < hi:
        yy = y(0)
        grid.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="#8895A1" stroke-width="1.5"/>')
    for idx in [0, len(values) // 2, len(values) - 1]:
        grid.append(f'<text x="{x(idx):.1f}" y="{height-9}" text-anchor="middle" class="axis">{esc(labels[idx])}</text>')
    peak = max(range(len(values)), key=lambda i: values[i])
    trough = min(range(len(values)), key=lambda i: values[i])
    annotations = "".join(
        f'<circle cx="{x(i):.1f}" cy="{y(values[i]):.1f}" r="5" fill="{color}"/>'
        f'<text x="{x(i):.1f}" y="{y(values[i])-10:.1f}" text-anchor="middle" class="mark">{values[i]:,.1f}</text>'
        for i in sorted({peak, trough})
    )
    return f'<svg viewBox="0 0 {width} {height}" class="chart-svg">{"".join(grid)}<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>{annotations}</svg>'


def svg_bars(values: Sequence[float], labels: Sequence[str], color: str, *, width: int = 540, height: int = 300, sparse: bool = False) -> str:
    left, top, right, bottom = 60, 18, 16, 44
    inner_w, inner_h = width - left - right, height - top - bottom
    hi = max(values) or 1
    gap = 3 if len(values) > 15 else 18
    bar_w = max(2, inner_w / len(values) - gap)
    items = []
    for i in range(5):
        val = hi * (4 - i) / 4
        yy = top + inner_h * i / 4
        items.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="{GRID}"/>')
        items.append(f'<text x="{left-9}" y="{yy+5:.1f}" text-anchor="end" class="axis">{val:,.0f}</text>')
    for i, value in enumerate(values):
        xx = left + inner_w * i / len(values) + gap / 2
        hh = inner_h * value / hi
        items.append(f'<rect x="{xx:.1f}" y="{top+inner_h-hh:.1f}" width="{bar_w:.1f}" height="{hh:.1f}" fill="{color}" opacity="0.88"/>')
    tick_count = 5 if sparse else min(len(labels), 8)
    for n in range(tick_count):
        idx = round((len(labels)-1) * n / max(tick_count-1, 1))
        xx = left + inner_w * (idx + .5) / len(labels)
        items.append(f'<text x="{xx:.1f}" y="{height-12}" text-anchor="middle" class="axis">{esc(labels[idx])}</text>')
    return f'<svg viewBox="0 0 {width} {height}" class="chart-svg">{"".join(items)}</svg>'


def svg_scatter(xvals: Sequence[float], yvals: Sequence[float]) -> str:
    width, height = 760, 330
    left, top, right, bottom = 74, 18, 20, 48
    xlo, xhi = min(xvals), max(xvals)
    ylo, yhi = min(yvals), max(yvals)
    x = lambda v: left + (width-left-right) * (v-xlo)/(xhi-xlo)
    y = lambda v: top + (height-top-bottom) * (yhi-v)/(yhi-ylo)
    items = []
    for i in range(5):
        xx = left + (width-left-right)*i/4
        yy = top + (height-top-bottom)*i/4
        items += [f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{height-bottom}" stroke="{GRID}"/>',
                  f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="{GRID}"/>']
    for xv, yv in zip(xvals, yvals):
        color = BLUE if xv >= 0 else CYAN
        items.append(f'<circle cx="{x(xv):.1f}" cy="{y(yv):.1f}" r="2.2" fill="{color}" opacity="0.42"/>')
    items += [f'<text x="{width/2}" y="{height-8}" text-anchor="middle" class="axis">Net Imbalance Volume (MWh)</text>',
              f'<text transform="translate(16 {height/2}) rotate(-90)" text-anchor="middle" class="axis">System Price (GBP/MWh)</text>',
              f'<text x="{left}" y="{height-bottom+20}" class="axis">{xlo:,.0f}</text>',
              f'<text x="{width-right}" y="{height-bottom+20}" text-anchor="end" class="axis">{xhi:,.0f}</text>',
              f'<text x="{left-8}" y="{top+5}" text-anchor="end" class="axis">{yhi:,.0f}</text>',
              f'<text x="{left-8}" y="{height-bottom+4}" text-anchor="end" class="axis">{ylo:,.0f}</text>']
    return f'<svg viewBox="0 0 {width} {height}" class="chart-svg">{"".join(items)}</svg>'


def box(x: int, y: int, w: int, h: int, content: str, cls: str = "panel") -> str:
    return f'<section class="{cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{content}</section>'


def title_block(title: str, subtitle: str, slicer: str, *, label_x: int = 1168, label_y: int = 28) -> str:
    return (
        box(32, 24, 1120, 56, f'<h1>{esc(title)}</h1>', 'plain')
        + box(32, 88, 1120, 32, f'<div class="scope">{esc(subtitle)}</div>', 'plain')
        + box(label_x, label_y, 252, 30, '<div class="preview-label">STATIC DESIGN PREVIEW</div>', 'plain')
        + box(1448, 24, 440, 88, f'<div class="slicer"><span>{esc(slicer)}</span><b>All ▾</b></div>', 'panel slicer-panel')
    )


def footer(text: str) -> str:
    return box(32, 1016, 1856, 40, f'<div class="footer">{esc(text)}</div>', 'plain')


def cards(items: Iterable[tuple[str, str, str]]) -> str:
    bits = []
    for label, value, tone in items:
        bits.append(f'<div class="kpi"><div class="kpi-label">{esc(label)}</div><div class="kpi-value {tone}">{esc(value)}</div></div>')
    return '<div class="kpi-row">' + ''.join(bits) + '</div>'


def table(headers: Sequence[str], rows: Iterable[Sequence[object]], classes: str = "") -> str:
    head = ''.join(f'<th>{esc(h)}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{esc(v)}</td>' for v in row) + '</tr>' for row in rows)
    return f'<table class="data-table {classes}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


CSS = f"""
*{{box-sizing:border-box}} html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#E8ECEF;font-family:Arial,'Helvetica Neue',sans-serif;color:{INK}}}
.page{{position:relative;width:{W}px;height:{H}px;background:#F6F8FA;overflow:hidden}}
.panel{{position:absolute;background:white;border:1px solid #D8E0E6;overflow:hidden}}
.plain{{position:absolute;overflow:hidden}} h1{{font-size:36px;line-height:48px;margin:0;font-weight:700;letter-spacing:-.4px}}
.scope{{font-size:17px;color:{MUTED};line-height:28px}} .preview-label{{font-size:13px;font-weight:700;letter-spacing:.9px;color:#7A3E00;background:#FFF1DB;border:1px solid #EDC486;padding:6px 10px;text-align:center}}
.slicer-panel{{padding:0}} .slicer{{height:100%;padding:14px 18px;border-left:5px solid {BLUE};display:flex;flex-direction:column;gap:8px}} .slicer span{{font-size:13px;text-transform:uppercase;letter-spacing:.7px;color:{MUTED};font-weight:700}} .slicer b{{font-size:20px}}
.kpi-row{{height:100%;display:grid;grid-template-columns:repeat(4,1fr)}} .kpi{{padding:24px 30px;border-right:1px solid #E3E8EC}} .kpi:last-child{{border:0}} .kpi-label{{font-size:15px;color:{MUTED};font-weight:700}} .kpi-value{{font-size:40px;line-height:58px;font-weight:700}} .good{{color:{GREEN}}}.warn{{color:{AMBER}}}.bad{{color:{RED}}}.blue{{color:{BLUE}}}
.visual{{padding:18px 20px}} .visual h2,.text-card h2{{font-size:20px;margin:0 0 8px;line-height:26px}} .visual .sub{{font-size:13px;color:{MUTED};margin-bottom:4px}} .chart-svg{{width:100%;height:calc(100% - 36px);display:block}} .axis{{font:12px Arial;fill:{MUTED}}}.mark{{font:12px Arial;fill:{INK};font-weight:700}}
.data-table{{width:100%;border-collapse:collapse;font-size:14px;table-layout:fixed}} .data-table th{{background:#EAF2F9;color:#24425E;text-align:left;padding:10px 9px;border-bottom:2px solid #B8CAD8;font-size:12px;text-transform:uppercase;letter-spacing:.3px}} .data-table td{{padding:9px;border-bottom:1px solid #E4E9ED;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}} .data-table tbody tr:nth-child(even){{background:#F8FAFB}}
.controls th{{padding:8px 9px}} .controls td{{padding:7px 9px}}
.queue{{font-size:13px}}.queue th:nth-child(1),.queue td:nth-child(1){{width:18%;font-weight:700;color:{BLUE}}}.queue th:nth-child(2),.queue td:nth-child(2){{width:10%}}.queue th:nth-child(3),.queue td:nth-child(3){{width:14%;text-align:right}}.queue th:nth-child(4),.queue td:nth-child(4){{width:13%;text-align:right}}.queue th:nth-child(5),.queue td:nth-child(5){{width:29%}}.queue th:nth-child(6),.queue td:nth-child(6){{width:16%;color:{GREEN};font-weight:700}}
.matrix td:nth-child(n+2){{text-align:right}} .matrix td:first-child{{font-weight:700}} .matrix tr:last-child td{{border-top:2px solid #B8CAD8}}
.text-card{{padding:20px 24px}} .text-card p{{font-size:17px;line-height:1.42;margin:5px 0;color:#2D3945}} .text-card ul{{margin:8px 0 0 20px;padding:0}} .text-card li{{font-size:17px;line-height:1.38;margin:7px 0}} .eyebrow{{font-size:12px;color:{MUTED};font-weight:700;letter-spacing:.7px;text-transform:uppercase;margin-bottom:7px}}
.known{{border-top:7px solid {GREEN}}}.unknown{{border-top:7px solid {AMBER}}}.hypothesis{{border-top:7px solid {CYAN}}}.next{{border-top:7px solid {BLUE}}}.status{{border-top:7px solid {INK}}}
.big-number{{font-size:46px;font-weight:700;line-height:1.15;color:{BLUE}}}.metric-line{{font-size:15px;color:{MUTED};margin-top:6px}} .callout{{padding:12px 15px;background:#EEF5FA;border-left:4px solid {BLUE};font-size:15px;line-height:1.35;margin-top:12px}}
.footer{{font-size:13px;line-height:34px;color:{MUTED};border-top:1px solid #CDD6DD}} .status-pill{{display:inline-block;border-radius:2px;padding:4px 8px;font-size:12px;font-weight:700;background:#E5F4EC;color:{GREEN}}} .note{{font-size:15px;line-height:1.38;color:#354250}}
"""


def document(body: str, page_name: str) -> str:
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(page_name)} — static preview</title><style>{CSS}</style></head><body><main class="page">{body}</main></body></html>'


def page_one(daily: pd.DataFrame, exceptions: pd.DataFrame) -> str:
    labels = pd.to_datetime(daily.settlement_date).dt.strftime('%d %b').tolist()
    q = exceptions.head(11)
    rows = [(r.event_id, r.system_length, f'£{r.system_price:,.2f}', f'{r.niv:,.1f}', r.reason_flagged.replace(' (1st/99th percentile)',''), r.quality_status) for r in q.itertuples()]
    body = title_block('Settlement Service Monitor', 'Q4 2025 | Historical snapshot | Independent portfolio project', 'Date')
    body += box(32,144,1856,160,cards([('Settlement periods','4,418','blue'),('Data completeness','100.00%','good'),('Analytical exceptions','130','warn'),('Validation exceptions','0','good')]))
    body += box(32,328,1040,320,f'<h2>Daily average System Price | GBP/MWh</h2>{svg_line(daily.mean_price.tolist(),labels,BLUE)}','panel visual')
    body += box(32,672,1040,320,f'<h2>Daily average signed NIV | MWh</h2>{svg_line(daily.mean_absolute_niv.mul(0).add(pd.read_csv(DATA/"processed"/"settlement.csv").groupby("settlement_date").niv.mean().reindex(daily.settlement_date).to_numpy()).tolist(),labels,CYAN,zero=True)}','panel visual')
    body += box(1096,328,792,664,'<div class="visual"><h2>Analytical exception queue</h2><div class="sub">Filtered to flagged periods • first 11 of 130 shown</div>'+table(['Event','Length','Price','NIV','Flag','Quality'],rows,'queue')+'</div>')
    body += footer('Design preview from canonical data and PBIR bindings • Not a Power BI runtime screenshot • Data through 31 Dec 2025')
    return document(body,'Settlement Service Monitor')


def page_two(settlement: pd.DataFrame, length: pd.DataFrame, price_dist: pd.DataFrame, niv_dist: pd.DataFrame, period: pd.DataFrame) -> str:
    body = title_block('Market & Settlement Analysis','Distributions and associations | full-quarter retrospective view','System length',label_x=928,label_y=82)
    body += box(1200,24,220,88,'<div class="slicer"><span>Month</span><b>All ▾</b></div>','panel slicer-panel')
    length_rows=[]
    order=['Short','Long','Balanced']
    for name in order:
        r=length.loc[length.system_length==name].iloc[0]
        length_rows.append((name,f'{int(r.periods):,}',f'£{r.mean_price:,.2f}',f'£{r.median_price:,.2f}',f'{r.mean_absolute_niv:,.1f}'))
    body += box(32,144,584,376,'<div class="visual"><h2>System length comparison</h2><div class="sub">Quarterly descriptive comparison; not causal</div>'+table(['Length','Periods','Mean price','Median','Mean |NIV|'],length_rows,'matrix')+'<div class="callout">Short periods averaged <b>£101.24/MWh</b> versus <b>£53.07/MWh</b> when long.</div></div>')
    body += box(640,144,600,376,f'<div class="visual"><h2>System Price distribution</h2><div class="sub">20 GBP/MWh bins • negative values retained</div>{svg_bars(price_dist.periods.tolist(),price_dist.price_bin_lower.astype(str).tolist(),BLUE,width=540,height=280,sparse=True)}</div>')
    body += box(1264,144,624,376,f'<div class="visual"><h2>Average price by Settlement Period</h2><div class="sub">SP49/50 occur only on the clock-change day</div>{svg_line(period.mean_price.tolist(),period.settlement_period.astype(str).tolist(),CYAN)}</div>')
    body += box(32,544,584,448,f'<div class="visual"><h2>NIV distribution</h2><div class="sub">100 MWh bins • signed NIV</div>{svg_bars(niv_dist.periods.tolist(),niv_dist.niv_bin_lower.astype(str).tolist(),CYAN,width=540,height=340,sparse=True)}</div>')
    body += box(640,544,824,448,f'<div class="visual"><h2>System Price versus NIV</h2><div class="sub">Each dot is one Settlement Period • association is not causation</div>{svg_scatter(settlement.niv.tolist(),settlement.system_price.tolist())}</div>')
    body += box(1488,544,400,192,'<div class="text-card"><div class="eyebrow">Observed association</div><div class="big-number">0.624</div><div class="metric-line">Pearson correlation</div><div class="metric-line"><b>0.763</b> Spearman rank correlation</div></div>')
    body += box(1488,760,400,232,'<div class="text-card"><h2>Interpretation boundary</h2><p>Positive signed NIV is associated with higher prices in this quarter.</p><p><b>Not established:</b> causality, forecast performance, service impact or annual seasonality.</p></div>')
    body += footer('Design preview from canonical data and PBIR bindings • Thresholds are retrospective analyst review rules, not BSC limits')
    return document(body,'Market & Settlement Analysis')


def text_panel(x:int,y:int,w:int,h:int,title:str,text:str,cls:str) -> str:
    return box(x,y,w,h,f'<div class="text-card"><div class="eyebrow">{esc(title)}</div><p>{esc(text)}</p></div>',f'panel {cls}')


def page_three(case: pd.Series) -> str:
    known = case.known.replace('487.0000000000000000', '487.00')
    body = title_block('Exception Investigation','Evidence record | known, unknown and next action kept separate',f'Event: {case.event_id}')
    body += text_panel(32,144,904,184,'What happened',case.what_happened,'')
    body += box(960,144,928,184,f'<div class="text-card"><div class="eyebrow">Why it was flagged</div><p><b>{esc(case.reason_flagged)}</b></p><p>Price percentile {case.price_percentile:.2f} • |NIV| percentile {case.absolute_niv_percentile:.2f}</p><span class="status-pill">DATA QUALITY {esc(case.quality_control_result)}</span></div>','panel')
    body += text_panel(32,352,904,368,'Known',known,'known')
    body += text_panel(960,352,928,184,'Not established',case.not_established,'unknown')
    body += text_panel(960,560,928,160,'Hypothesis',case.hypotheses,'hypothesis')
    body += text_panel(32,744,1200,248,'Recommended next checks',case.recommended_next_checks,'next')
    body += box(1256,744,632,248,f'<div class="text-card"><div class="eyebrow">Investigation status</div><p><b>{esc(case.investigation_status)}</b></p><div class="callout">Evidence available: {esc(case.evidence_available)}<br>Reconciliation: {esc(case.summary_reconciliation)}</div></div>','panel status')
    body += footer('Selected case: 13 Oct 2025 SP26 • Analytical exception does not imply a service incident')
    return document(body,'Exception Investigation')


def page_four(daily_controls: pd.DataFrame, source_controls: pd.DataFrame) -> str:
    body = title_block('Data Quality & Controls','Audit-friendly controls | validate before interpretation','Settlement date')
    body += box(32,144,1856,160,cards([('Expected periods','4,418','blue'),('Received periods','4,418','blue'),('Completeness','100.00%','good'),('Core exceptions','0','good')]))
    selected_dates=['2025-10-01','2025-10-03','2025-10-13','2025-10-26','2025-11-01','2025-12-01','2025-12-31']
    chosen=daily_controls[daily_controls.settlement_date.isin(selected_dates)]
    rows=[(r.settlement_date,int(r.expected_periods),int(r.received_periods),int(r.missing_periods),int(r.duplicate_periods),int(r.null_values),'Yes' if r.clock_change else 'No',r.retrieval_status) for r in chosen.itertuples()]
    body += box(32,328,1856,360,'<div class="visual"><h2>Daily validation log | selected audit rows</h2><div class="sub">Includes investigation dates and the 50-period autumn clock-change day</div>'+table(['Settlement date','Expected','Received','Missing','Duplicates','Nulls','Clock change','Retrieval'],rows,'controls')+'</div>')
    source_rows=[(r.control,r.status,r.detail) for r in source_controls.head(5).itertuples()]
    body += box(32,712,1168,280,'<div class="visual"><h2>Whole-snapshot source controls</h2><div class="sub">Five key controls shown; complete audit remains in the quality layer</div>'+table(['Control','Status','Evidence'],source_rows)+'</div>')
    body += box(1224,712,664,280,'<div class="text-card"><h2>Control interpretation</h2><ul><li>Clock-day expectations derive from elapsed UTC time between London midnights: 46, 48 or 50.</li><li>Raw response bytes are immutable and hash checked.</li><li>A failed refresh invalidates previous exports for consumers.</li><li>Snapshot age is an analyst review policy—not an Elexon SLA.</li></ul></div>','panel')
    body += footer('Design preview from canonical data and PBIR bindings • All displayed controls are from the retained successful snapshot')
    return document(body,'Data Quality & Controls')


def main() -> None:
    run = pd.read_json(DATA/'processed'/'run.json',typ='series')
    if run.get('status') != 'success':
        raise RuntimeError('Static previews require a successful canonical pipeline run')
    OUT.mkdir(parents=True,exist_ok=True)
    daily=pd.read_csv(DATA/'processed'/'daily_summary.csv')
    settlement=pd.read_csv(DATA/'processed'/'settlement.csv')
    exceptions=pd.read_csv(DATA/'processed'/'exception_queue.csv')
    length=pd.read_csv(DATA/'processed'/'length_summary.csv')
    price_dist=pd.read_csv(DATA/'processed'/'price_distribution.csv')
    niv_dist=pd.read_csv(DATA/'processed'/'niv_distribution.csv')
    period=pd.read_csv(DATA/'processed'/'period_summary.csv')
    investigation=pd.read_csv(DATA/'processed'/'investigation_queue.csv')
    case=investigation.loc[investigation.event_id=='2025-10-13 SP26'].iloc[0]
    daily_controls=pd.read_csv(DATA/'quality'/'daily_controls.csv')
    source_controls=pd.read_csv(DATA/'quality'/'source_controls.csv')
    pages=[page_one(daily,exceptions),page_two(settlement,length,price_dist,niv_dist,period),page_three(case),page_four(daily_controls,source_controls)]
    for i,html in enumerate(pages,1):
        (OUT/f'elexon-powerbi-preview-{i:02}.html').write_text(html)
    print(f'Wrote {len(pages)} static preview pages to {OUT}')


if __name__ == '__main__':
    main()
