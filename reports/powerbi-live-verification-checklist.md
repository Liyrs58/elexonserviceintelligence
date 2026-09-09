# Power BI live-verification checklist

Use this only in a licensed Power BI Desktop or supported Fabric environment. Static definitions already pass the official report validator and Modeling MCP folder import. This checklist closes the remaining execution and presentation gate; it does not author a different report.

## 1. Open and refresh

1. Ensure `data/processed/run.json` has `"status": "success"` and the canonical processed/quality CSVs are present.
2. Open `powerbi/project/Settlement.pbip`.
3. Set the `DataFolder` parameter to the absolute `data` directory for this checkout.
4. Run a full refresh. Record the Power BI version, machine, refresh start/end time and any warnings.
5. Stop on any M, relationship, type or credential error. Do not use retained visuals as evidence of a successful refresh.

## 2. Verify all 19 measures

Use an unfiltered whole-quarter page or a DAX query view. Counts must match exactly. Compare unrounded decimal values within `1e-8`; the report may display the documented rounded format.

| Table | Measure | Expected whole-quarter value |
|---|---|---:|
| Date | Expected Settlement Periods | 4,418 |
| Settlement | Settlement Periods | 4,418 |
| Settlement | Average System Price | 75.724102066468 GBP/MWh |
| Settlement | Median System Price | 74.705 GBP/MWh |
| Settlement | Maximum System Price | 487 GBP/MWh |
| Settlement | Minimum System Price | -30 GBP/MWh |
| Settlement | Average NIV | -22.876913205075 MWh |
| Settlement | Average Absolute NIV | 204.582328872881 MWh |
| Settlement | Maximum Absolute NIV | 1,563.338268462202 MWh |
| Settlement | Short Settlement Periods | 2,076 |
| Settlement | Long Settlement Periods | 2,340 |
| Settlement | Extreme Price Periods | 92 |
| Settlement | Extreme Imbalance Periods | 45 |
| Settlement | Analytical Exceptions | 130 |
| Daily Controls | Data Completeness % | 100.00% |
| Daily Controls | Missing Settlement Periods | 0 |
| Daily Controls | Duplicate Settlement Periods | 0 |
| Daily Controls | Validation Exceptions | 0 |
| Daily Controls | Null Values | 0 |

Record every mismatch before changing DAX. Reconcile filter context, row grain and source refresh first.

## 3. Test filter context and interactions

- Clear all filters and confirm the whole-quarter values above.
- Select 26 October 2025: expected and received periods must both be 50 and completeness must remain 100%.
- Select October 2025: expected and received periods must both be 1,490.
- Select system length `Short`: Settlement Periods must be 2,076 while Expected Settlement Periods and the Daily Controls completeness denominator remain whole-date values. This verifies the intended one-direction model behaviour.
- Clear the length filter and confirm all values restore.
- Confirm the Page 1 operational queue contains only flagged periods and totals 130 when the quarter is unfiltered.
- On Exception Investigation, select `2025-10-13 SP26`; confirm £487/MWh, +184.9225 MWh, `Short`, price-tail reason, passed data quality, known/not-established separation and recommended next checks.
- Test every date, month, system-length and investigation-event slicer. Confirm each intended visual changes, unrelated whole-snapshot controls do not, and clearing the slicer restores state.
- Check empty/no-selection and multi-selection states for misleading titles, blank cards or stale narrative text.

## 4. Inspect all four pages

At 100% and a normal laptop viewport, inspect titles, units, sorting, legends, labels, contrast, keyboard focus, colour-independent status cues, clipping, overlap and whitespace.

1. Settlement Service Monitor — status band, aligned price/NIV time views and operational queue.
2. Market & Settlement Analysis — length comparison, distributions, intraday pattern and NIV/price association.
3. Exception Investigation — event, flag, quality, known, not established, hypotheses and next checks.
4. Data Quality & Controls — retrieval, expected/received, completeness, duplicates, null/schema exceptions, clock change and audit table.

Capture genuine page images only after refresh and interaction checks pass. Save them as `screenshots/powerbi-01-monitor.png` through `screenshots/powerbi-04-controls.png`; then add a labelled hero image to the README. Never substitute the presentation artwork or a mock dashboard.

## 5. Performance check

Use Performance Analyzer on each page after clearing cache, refresh visuals once, and export or record the timings. Investigate the slowest visuals and any obviously disproportionate DAX/query/render time; do not invent a pass threshold. Record page, visual title, DAX/query duration, render duration, total duration and any change made. Re-run after any optimisation.

## 6. Completion record

Append the observed results to `reports/powerbi-definition-qa.md` and update `reports/requirements-audit.md`, `PROJECT_STATE.md`, README delivery status and `powerbi/measure-catalog.json` runtime status. Include:

- environment and Power BI version;
- refresh result and duration;
- 19-measure comparison outcome;
- interaction scenarios passed/failed;
- four-page visual/accessibility review;
- Performance Analyzer evidence;
- screenshot paths and hashes;
- remaining limitations;
- reviewer and date.

Only then may the project be labelled live Power BI verified and the CV/interview package be finalized.
