# Insight note QA - 9 September 2026

Final artifact: `reports/service-insight-note.pdf`. One A4 page, nine requested sections, two working PDF link annotations, and independent/non-endorsement footer. Produced using the bundled Python runtime and ReportLab. PDF skill operation marker completed once before authoring.

## Evidence and claim review

- Numeric content reads `summary.json`, `thresholds.json`, `investigations.json` and `price_reconciliation.csv` dynamically. Counts, mean, median, thresholds and percentile rank are DERIVED/FLAG rather than new source observations.
- Selected 13 October SP26 values independently checked against SHA-256-verified daily raw response: buy=sell=487 GBP/MWh, NIV=184.92249316358024 MWh.
- Builder checks all three reconciliation records pass penny-precision and creation-time alignment before reporting this result.
- Exact median 74.705 is retained to avoid contradictory two-decimal tie rounding. Threshold display rounding is explicit; actual comparisons use unrounded pipeline thresholds.
- Revision: NIV threshold now reads "at/above 876.0417 MWh", preserving inclusive comparison and four-decimal display precision. Latest revised PDF re-rendered and visually inspected with no layout defects; one-page count and threshold text checked through PDF extraction.
- Builder calls `require_successful_run` before reading any processed output. A simulated failed-run guard raised before build; previous verified PDF is preserved, not overwritten by a stale-data refresh. A successful old PDF does not constitute proof of a new successful run.
- Hypothesis explicitly not confirmed. Price reconstruction is not causal explanation. Historical completeness is not service availability. Power BI execution/interactions explicitly remain unverified.
- Official source links are Elexon API catalogue and formal imbalance pricing guidance; repository sources/methodology identify snapshot provenance and calculation method.

## Visual review

Latest PDF rendered with bundled Poppler at 130 dpi and inspected in full after increasing body type to 10.3pt. All nine sections, footer and source references visible. No clipping, overlap, missing glyphs or broken lines observed. Near-black body text on white with restrained teal headings; typography and left alignment consistent. PDF text extraction confirms one page, exact median and corrected percentile wording.

Local renderer required `FONTCONFIG_FILE=/private/tmp/elexon-note-fonts.conf` pointing at `/System/Library/Fonts` and a writable temporary cache. Initial unconfigured renderer emitted font-cache warnings; the configured final rendering succeeded. Preview is an intermediate in `tmp/pdfs/`, not a Power BI screenshot.

## Rebuild

Run the installed Python environment with ReportLab: `python src/reporting/build_insight_note.py`. This regenerates the note from current processed outputs. Re-render and inspect after changes; do not treat this QA as transferable to a modified artifact.
