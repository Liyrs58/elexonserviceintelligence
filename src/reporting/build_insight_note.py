"""Build the one-page stakeholder note from saved, validated project outputs."""
from pathlib import Path
import csv
import json
import sys
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.validate.run_status import require_successful_run


def build() -> Path:
    data = ROOT / "data/processed"
    require_successful_run(data)
    summary = json.loads((data / "summary.json").read_text())
    thresholds = json.loads((data / "thresholds.json").read_text())
    cases = json.loads((data / "investigations.json").read_text())
    event = max(cases, key=lambda item: item["system_price"])
    with (data / "price_reconciliation.csv").open() as stream:
        reconciliations = list(csv.DictReader(stream))
    reconciliation = next(row for row in reconciliations if row["event_id"] == event["event_id"])
    assert len(reconciliations) == 3
    assert all(row["matches_to_penny"] == "True" for row in reconciliations)
    assert all(row["stack_summary_creation_aligned"] == "True" for row in reconciliations)
    assert summary["records"] == summary["expected_records"]
    output = ROOT / "reports/service-insight-note.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, invariant=True)
    page.setTitle("Service Insight Note - GB Imbalance & System Price Monitoring")
    page.setAuthor("Independent portfolio analysis")
    width, height = A4
    ink, accent = HexColor("#17212B"), HexColor("#006A70")
    style = ParagraphStyle("Body", fontName="Helvetica", fontSize=10.3, leading=13.5, textColor=ink)

    def paragraph(text: str, x: float, top: float, available_width: float, size=None) -> float:
        current = style if size is None else ParagraphStyle("Small", parent=style, fontSize=size, leading=size + 2.4)
        item = Paragraph(text, current)
        _, used = item.wrap(available_width, height)
        item.drawOn(page, x, top - used)
        return top - used

    page.setFillColor(accent)
    page.rect(36, height - 43, width - 72, 4, fill=1, stroke=0)
    page.setFillColor(ink)
    page.setFont("Helvetica-Bold", 21)
    page.drawString(36, height - 76, "Service Insight Note")
    page.setFont("Helvetica", 14)
    page.drawString(36, height - 98, "GB Imbalance & System Price Monitoring")
    y = paragraph("Q4 2025 | Historical analytical review | Prepared 9 September 2026", 36, height - 111, width - 72, 8.7)

    sections = [
        ("ANALYTICAL QUESTION", "Which unusual Settlement Periods merit investigation, and what does the available evidence establish before any escalation?"),
        ("DATA / SOURCE", f"Official Elexon Insights API: {summary['start_date']} to {summary['end_date']}. Latest settlement-run price/NIV snapshot retrieved {summary['retrieved_at'][:10]} at {summary['retrieved_at'][11:16]} UTC; detailed summary and bid/offer stacks for three selected periods. [1]"),
        ("SERVICE / DATA STATUS", f"<b>DERIVED:</b> {summary['records']:,}/{summary['expected_records']:,} expected periods ({summary['completeness']:.0%}); {summary['validation_exceptions']} core validation exceptions. Includes 50 periods on 26 October. These checks establish snapshot coverage and validity, <b>not live service availability</b>."),
        ("KEY FINDINGS", f"<b>DERIVED:</b> Mean price GBP {summary['mean_price']:.2f}/MWh; median GBP {summary['median_price']:.3f}/MWh. <b>FLAG:</b> {summary['exception_periods']} distinct periods ({summary['price_flag_periods']} price-tail; {summary['imbalance_flag_periods']} large-|NIV|; {summary['price_flag_periods'] + summary['imbalance_flag_periods'] - summary['exception_periods']} overlap). Full-window thresholds: price at/below {thresholds['price_p01']:.2f} or at/above {thresholds['price_p99']:.4f} GBP/MWh; |NIV| at/above {thresholds['absolute_niv_p99']:.4f} MWh (display-rounded). These are review flags, not incidents."),
        ("MATERIAL EXCEPTION", f"<b>OBSERVED:</b> {escape(event['event_id'])}: price GBP {event['system_price']:.2f}/MWh; NIV +{event['niv']:.2f} MWh. <b>DERIVED:</b> quarter-high price; short system. Its |NIV| percentile rank is only {event['absolute_niv_percentile']:.1f}%: the largest price and imbalance are different cases."),
        ("WHAT IS KNOWN", f"<b>DERIVED:</b> {reconciliation['retained_rows']} retained offer-stack rows reconstruct GBP {float(reconciliation['reconstructed_price']):.2f}/MWh from loss-adjusted cost/volume plus the source adjuster. Stack and summary creation times agree. All three selected cases reconcile to penny precision; this supports the published calculation, not its underlying cause. [1, 2]"),
        ("WHAT IS NOT ESTABLISHED", "Why the balancing actions were needed; demand or generation causality; any service incident. <b>HYPOTHESIS:</b> action prices may explain price severity better than NIV magnitude alone. This is not a confirmed causal finding."),
        ("RECOMMENDED NEXT CHECKS", "Confirm calculation vintages; review why retained actions were accepted using official action-level evidence, then targeted demand/generation context. Record evidence and an owner before escalation. Investigate official incident history if a data-control exception emerges."),
        ("LIMITATIONS", "One quarter, one retrieval vintage; retrospective percentile screening with inclusive ties, not BSC limits or a predictive detector. Different datasets can carry different vintages despite price agreement. Power BI runtime and interactions remain unverified; no deployment is claimed."),
    ]
    for heading, body in sections:
        y -= 12
        page.setFillColor(accent)
        page.setFont("Helvetica-Bold", 8.6)
        page.drawString(36, y - 8.6, heading)
        y = paragraph(body, 36, y - 14, width - 72)
    assert y > 69, f"Body exceeds footer clearance: {y}"
    page.setStrokeColor(HexColor("#CBD2D5"))
    page.line(36, 62, width - 36, 62)
    paragraph('[1] <link href="https://developer.data.elexon.co.uk/api-details#api=prod-insol-insights-api" color="#006A70">Elexon API catalogue</link>; immutable snapshots and calculations: repository SOURCES.md / METHODOLOGY.md.<br/>[2] <link href="https://bscdocs.elexon.co.uk/guidance-notes/imbalance-pricing-guidance" color="#006A70">Elexon imbalance pricing guidance</link>. Independent portfolio project; not affiliated with or endorsed by Elexon.', 36, 55, width - 72, 7.2)
    page.showPage()
    page.save()
    return output


if __name__ == "__main__":
    print(build())
