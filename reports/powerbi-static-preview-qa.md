# Power BI static-preview QA

Reviewed 9 September 2026.

## Method and evidence class

`src/reporting/build_powerbi_previews.py` reads only canonical processed/quality CSVs after confirming `data/processed/run.json` is `success`. Page names, count and visual intent were cross-checked against Microsoft's report-authoring `preview-pages`, `preview-visuals` and `preview-filters` inventories for the checked-in PBIR report. The output is local presentation evidence, not Power BI execution evidence.

## Result

- Four PNGs generated at exactly 1920 × 1080.
- All four inspected at original resolution; headings, KPI cards, axes, tables, evidence labels and footers fit without visible clipping or overlap.
- Retained headline values agree with the verified analytical outputs and claim audit.
- Each image includes `STATIC DESIGN PREVIEW`; monitor/analysis footers explicitly state the non-runtime boundary, and this record applies that boundary to all four files.
- SHA-256 values are recorded in `screenshots/README.md` and in the reviewer ZIP manifest.

## Limit

This QA does not cover M refresh, DAX results, native visual formatting, slicer behaviour, cross-highlighting, keyboard/screen-reader accessibility, empty states or Performance Analyzer. Those remain in `reports/powerbi-live-verification-checklist.md` for a licensed Windows reviewer.
