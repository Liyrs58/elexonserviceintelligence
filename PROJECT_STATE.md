# Project state

## Objective
Build, verify and package the full GB Settlement & Imbalance Service Intelligence Monitor specified in PROJECT_SPEC.md.

## Completed work
Preserved full specification. Official domain/API/benchmark research saved. Implemented ingestion, calendar controls, transformation, percentile screening, SQL, investigation retrieval and price reconciliation. Current meaningful suite: 20 tests pass. Downloaded Q4 2025: all 92 requests succeeded, 4,418 expected/received periods, no core quality exceptions. Python/SQL key aggregates agree within 1e-8. Retrieved and reconciled official summary and both stacks for three selected cases.

## Current work
Source controls and semantic model implemented; report design and artifact production now next. Full brief remains active; project is NOT complete.

## Outstanding work
Finish report design and four-page PBIR report. Semantic model definitions now exist but are unverified in a model engine. Produce one-page PDF insight note, eight-slide editable/PDF presentation, genuine report screenshots if runtime available, README, claim/requirement audit and final interview outputs. Clean-state reretrieval/rebuild and meaningful independent QA remain. Do not label mock renderings as Power BI screenshots or local DAX definitions as executed measures.

Additional completed work: source schema signatures, source UTC/creation/retrieval controls, explicit 30-day snapshot review policy; all pass current data. 23 meaningful tests pass, including interrupted-retrieval manifest persistence. CSV distributions/descriptive percentiles and field provenance generated. Quality outputs standardised to data/quality. powerbi/build_model.mjs generates six tables, four relationships and 19 explicit measures. src/analysis/investigation_queue.py expands all130 flagged cases, three reviewed, remainder Level1 only. No report pages yet.

## Findings and decisions
Q4 2025 statistics: mean price 75.7241020665 GBP/MWh; median74.705; max487; min−30; max|NIV|1563.3382684622MWh; short2076 long2340 balanced2; negative prices151. 130 distinct flagged periods (92 price,45 imbalance,7 overlap). Thresholds price≤−11.22 or ≥153.8997; |NIV|≥876.0417274123. Full-window retrospective, inclusive ties, not BSC/SLA thresholds.

Three investigations: 2025-10-13 SP26 (max price487), 2025-11-01 SP19 (min−30), 2025-10-03 SP37 (max|NIV|; price109.4). Retained stack cost/volume plus adjuster reconciles each to penny precision; stack/summary creation timestamps align. Underlying market causes remain unestablished. Root inspected highest-price retained rows directly.

## Known issues and blockers
Power BI browser works (in-app browser through CUA), but app.powerbi.com displays email sign-in. Fabric workspace list with existing Azure login returned HTTP Unauthorized/UserNotLicensed, non-retriable. No MCP modeling tools exposed in current inventory. Local official CLI authoring remains available. Windows Desktop unavailable on Mac. Complete all unaffected outputs before requesting licensed runtime access. Subagents errored at account usage limit; their saved files were inspected and tests run by root.

Initial sandbox Python retrieval failed DNS and was interrupted; an empty incomplete raw directory may remain. Escalated public retrieval succeeded. No live process remains from ingestion/investigation.

## Important paths
PROJECT_SPEC.md: full brief. research/: discovery evidence. .tools/ and .venv/: ignored dependencies. Main snapshot data/raw/20260909T163243Z-dc4f225d/manifest.json. Context snapshot data/raw/20260909T163543Z-context-afc7db2e/manifest.json. Canonical results data/processed/summary.json, thresholds.json, settlement.csv/parquet, investigations.json/csv and price_reconciliation.csv. Controls now data/quality/; old data/processed/quality/ outputs are obsolete leftovers. SQL sql/analysis.sql. Model powerbi/project/Settlement.SemanticModel/definition; measure catalog powerbi/measure-catalog.json explicitly labels runtime unverified.

## Exact inspection commands
`git status --short`
`cat PROJECT_SPEC.md PROJECT_STATE.md DECISIONS.md SOURCES.md METHODOLOGY.md`

`.venv/bin/python -m pytest -q`
`.venv/bin/python -m src.ingest.client --start 2025-10-01 --end 2025-12-31`
`.venv/bin/python -m src.pipeline --manifest data/raw/20260909T163243Z-dc4f225d/manifest.json`
`.venv/bin/python -m src.analysis.investigate`
`.venv/bin/python -m src.analysis.reconcile`
`.venv/bin/python -m src.analysis.investigation_queue`
`node powerbi/build_model.mjs`

Fetch commands need external network permission in this sandbox. Each fetch creates a new immutable snapshot. Rebuild uses named manifest. Investigation retrieval currently selects three cases and reconciliation reads saved context.

## Next action
Finish remaining data controls, then author semantic model and four report pages. Main agent has read semantic-model-authoring (complete across calls), report-design and report-authoring SKILL.md plus modeling-guidelines, TMDL, PBIP, DAX references. Read required design/archetype/authoring reference files before implementation. Presentation SKILL.md was partly truncated; reread remaining content and mandatory implementation/quickstart/finalization references before authoring. PDF skill read. Runtime paths from load_workspace_dependencies are available. No slides/PDF/report currently exists.

Report reference-reading progress: authoring.md, expressions.md, textbox.md, formatting-overview.md, table.md, card.md, visual-cookbook.md, chart-selection.md and analytical-canvas archetype fully read. operational-monitor and narrative-story main bodies read across earlier output. layout/design-brief combined read had a small truncation around boundary; reread relevant missing portion. Cartesian reference1497 lines was truncated: selected introductory/last examples read, middle needs reading if used. Slicers502 lines, formatting469 lines, theming/base-theme, accessibility/anti-patterns and preflight references still needed for their applicable authoring operations. User overrides decorative gradients/curved-smoothed charts and unnecessary requirements interviews. Official CLI is available locally; inspect capabilities before creating visuals.
