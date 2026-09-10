# Power BI static design previews

These four images provide a Mac-readable review of the intended Power BI report. They were generated on 9 September 2026 from the successful canonical data outputs and the checked-in PBIR page/visual inventories, then inspected at full 1920 × 1080 resolution.

They are **not Power BI runtime screenshots**. They do not prove M refresh, DAX execution, filter interactions, accessibility or performance. Every image carries the label `STATIC DESIGN PREVIEW` and a footer stating its evidence boundary.

| File | Intended report page | SHA-256 |
|---|---|---|
| `powerbi-static-preview-01-monitor.png` | Settlement Service Monitor | `32530aef48cce35d528425d45eddc5ed23b19aa3b36e3f8b58b8d554b5ecfb2a` |
| `powerbi-static-preview-02-analysis.png` | Market & Settlement Analysis | `583ee5d5575971ef8105bb890dc6f12afb5fec32ff4fcf8738a02ecad0c327c7` |
| `powerbi-static-preview-03-investigation.png` | Exception Investigation | `f1f3ca710d561397129366924bffa0e4b4942a0377b5e29f771971b6653b0e5e` |
| `powerbi-static-preview-04-controls.png` | Data Quality & Controls | `51f74ed8c341bc24a8e3e6e13e98b9d52fe569fed1782310e3c3db23b83abdfe` |

The reproducible source is `src/reporting/build_powerbi_previews.py`. Genuine runtime captures must use the names and acceptance checks in `reports/powerbi-live-verification-checklist.md`.
