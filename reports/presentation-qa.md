# Presentation QA

Verified 9 September 2026 against `reports/presentation/settlement-service-intelligence.pptx` and its PDF export.

## Structural checks

- Finalizer found eight slides, one editable native chart and four editable native tables.
- Package-integrity, geometry, heading-fit, font-policy and first-party re-import checks passed with zero findings.
- The slide 4 chart has an embedded workbook snapshot whose categories and two numeric values match the chart cache. This proves portable chart structure, not native Microsoft PowerPoint execution.
- Final PPTX SHA-256: `9c8de43fa0a163fbf628cde33d67635047905b23bdd3e94af67fd925a61762dd`.

## Visual inspection

The final PPTX was exported with the bundled headless LibreOffice runtime to an eight-page PDF, rendered at 120 dpi with bundled Poppler, and every page was inspected individually. Earlier drafts exposed cross-application wrapping and footer clipping; the presentation source was corrected and the final export was rerendered.

The final review found no clipped text, unwanted overlap, missing glyphs, broken table borders, illegible labels or inconsistent page numbering. Titles, evidence-class distinctions, units and source footers remain readable. Slide 4 chart labels and the short/long counts agree with `data/processed/length_summary.csv` and `summary.json`. Slides 5-6 agree with the investigation records and price reconciliation.

## Scope boundary

The PDF proves a readable export and the package checks prove editability/structure. Microsoft PowerPoint was not available, so native PowerPoint opening and editing were not tested. This does not affect the supplied editable PPTX but remains a target-application limitation. The presentation does not substitute for Power BI screenshots or live report verification.
