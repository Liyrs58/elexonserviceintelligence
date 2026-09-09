# Project state

## Objective and status

Finish, verify and package the GB Settlement & Imbalance Service Intelligence Monitor in `PROJECT_SPEC.md` without rebuilding completed work. As of 9 September 2026, all work that can be verified on this Mac is complete. Final completion is **partially blocked** by the licensed Power BI runtime gate described below.

## Verified analytical package

- Canonical Q4 2025 core snapshot: `data/raw/20260909T163243Z-dc4f225d/manifest.json`; 92/92 requests, 4,418/4,418 expected periods and zero core quality exceptions.
- Independent reproduction snapshot: `data/raw/20260909T170020Z-a1f525b9/manifest.json`; all 92 daily response hashes match the canonical snapshot. An isolated rebuild matches 13 CSVs exactly, the 4,418 × 43 Parquet table exactly after excluding retrieval timestamp, and all summary/threshold values.
- Detailed evidence snapshot: `data/raw/20260909T163543Z-context-afc7db2e/manifest.json`; summary and bid/offer stacks for three selected cases, with manifest hashes verified before reconciliation.
- Current suite: 38 tests pass. Coverage includes GB clock changes, malformed and incomplete input, retry behaviour, source-vintage controls, raw hash integrity, failed-refresh gating, reconciliation completeness and idempotence.
- The pipeline writes `running` before work, writes `failed` on any exception and exposes outputs only when the current run marker is `success`. Investigation, reconciliation, queue generation and all six Power BI imports enforce the same gate.
- Python and DuckDB agree within 1e-8 on nine key aggregates.

## Current findings

The quarter contains mean/median prices of £75.7241020665/£74.705 per MWh, a £487 maximum, a -£30 minimum and maximum absolute NIV of 1,563.3382684622 MWh. There are 2,076 short, 2,340 long and two balanced periods. Screening identifies 130 distinct flagged periods: 92 price flags, 45 imbalance flags and seven overlaps. The retrospective inclusive thresholds are price <= -£11.22 or >= £153.8997/MWh and absolute NIV >= 876.0417 MWh; they are analyst review rules, not BSC limits or SLAs.

Three detailed cases cover maximum price, minimum price and maximum absolute NIV. Their retained stack cost/volume plus adjuster reconciles each published price to penny precision, and stack/summary timestamps align. This validates the available calculation evidence; it does not establish the underlying market or service cause.

## Delivered artifacts

- Power BI project: `powerbi/project/Settlement.pbip`, with six semantic-model tables, four single-direction relationships, 19 explicit measures and four report pages containing 39 data-bound visuals.
- Official Microsoft report-authoring validation: zero errors and zero warnings. The official Modeling MCP also imports the TMDL folder successfully and returns all 19 measures in ready state. This final gate found and prompted correction of invalid generated date-column property sequencing. These checks prove parsable definitions and bindings; they do not execute M or DAX.
- One-page service note: `reports/service-insight-note.pdf`, with source builder and visual QA.
- Eight-slide editable presentation: `reports/presentation/settlement-service-intelligence.pptx`, plus reviewed PDF export. Package, geometry, font, first-party reimport and native-chart checks pass.
- Reviewer records: `reports/reproducibility-qa.md`, `reports/powerbi-definition-qa.md`, `reports/insight-note-qa.md`, `reports/presentation-qa.md`, `reports/source-link-qa.md`, `reports/claim-audit.md` and `reports/requirements-audit.md`.
- Reviewer documentation: `README.md`, `METHODOLOGY.md`, `DECISIONS.md`, `SOURCES.md`, `SETUP_REPORT.md`, `SETUP_SOURCES.md` and `data/README.md`.

## Remaining external gate

Power BI Desktop is unavailable natively on this Mac. The in-app browser previously reached Power BI Service but was at Microsoft sign-in, the browser-control service was unavailable on the final continuation, and the available Fabric identity returned `UserNotLicensed`. The Modeling MCP connection is offline and rejects DAX query execution. Consequently M refresh, actual DAX results, slicer/filter interactions, rendered visual accessibility/clipping, empty states, performance and genuine report screenshots are unverified.

The smallest close is to open `powerbi/project/Settlement.pbip` in a licensed Power BI Desktop environment, set `DataFolder` to this project's `data` directory, refresh, compare all 19 measures with `powerbi/measure-catalog.json` and the Python/SQL outputs, test interactions and capture all four pages. A licensed Fabric workspace with a supported route to the local files is the alternative. Do not claim runtime verification or use a dashboard screenshot until this passes.

GitHub publishing was not authorised and was not attempted. CV bullets and interview answers remain deferred under `PROJECT_SPEC.md` until live Power BI verification completes.

## Reproduction and verification commands

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m src.ingest.client --start 2025-10-01 --end 2025-12-31
.venv/bin/python -m src.pipeline --manifest data/raw/REPLACE_WITH_NEW_SNAPSHOT/manifest.json
.venv/bin/python -m src.analysis.investigate
.venv/bin/python -m src.analysis.reconcile
.venv/bin/python -m src.analysis.investigation_queue
node powerbi/build_model.mjs
node powerbi/build_report.mjs
.tools/powerbi-cli/node_modules/.bin/powerbi-report-author validate powerbi/project/Settlement.Report
```

Network retrieval creates a new immutable snapshot and needs internet access. The core rebuild is offline after retrieval. Detailed investigation retrieval is separate; reconciliation and queue generation are offline. Raw and processed data are ignored by Git; retained local snapshots are evidence for this review, not guaranteed checkout content.

## Authoritative paths

- Brief: `PROJECT_SPEC.md`
- State/decisions: `PROJECT_STATE.md`, `DECISIONS.md`
- Source register: `SOURCES.md`
- Method: `METHODOLOGY.md`
- Analysis: `src/`, `sql/`, `tests/`
- Canonical outputs: `data/processed/`, `data/quality/`
- Power BI definitions: `powerbi/project/`, `powerbi/measure-catalog.json`
- Final artifacts and QA: `reports/`
