# GB Settlement & Imbalance Service Intelligence Monitor

An independent operational analytics project using public Elexon data to validate Settlement Period information, identify unusual market conditions and structure evidence-led investigation.

**This is an independent portfolio project and is not affiliated with or endorsed by Elexon.**

Q4 2025 · 4,418 validated Settlement Periods · 130 analytical exceptions · three detailed price investigations

**Delivery status:** the reproducible Python/SQL analysis is verified. Four Power BI report pages pass Microsoft's report validator, and the semantic model imports successfully through Microsoft's Modeling MCP with all 19 measures in ready state. Live DAX, filtering and visual verification remain pending a licensed Power BI environment. A genuine dashboard hero screenshot belongs here after that verification. No mock image is presented as a Power BI screenshot.

## The problem

An unusual price is a reason to investigate—not proof of a data defect or service incident. An analyst needs to establish data quality first, identify meaningful exceptions, trace relevant evidence and communicate uncertainty without turning a plausible explanation into a confirmed cause.

This project follows **CONTROL → DETECT → INVESTIGATE → COMMUNICATE → RECOMMEND**. Standard price/NIV analysis provides the baseline; the differentiator is the structured review record, its explicit evidence boundaries and its recommended next checks.

## Verified findings

| Q4 2025 measure | Result |
|---|---:|
| Received / expected periods | 4,418 / 4,418 |
| Core validation exceptions | 0 |
| Mean / median System Price | £75.7241 / £74.705 per MWh |
| Highest / lowest price | £487 / −£30 per MWh |
| Largest absolute NIV | 1,563.3383 MWh |
| Short / long / balanced periods | 2,076 / 2,340 / 2 |
| Distinct flagged periods | 130 |

Short periods averaged £101.2391/MWh versus £53.0677/MWh for long periods. Signed NIV and price have a Pearson correlation of 0.6236 in this quarter; this describes association, not causation.

There are 92 price-tail flags and 45 absolute-NIV flags, with seven overlaps. Screening uses full-quarter retrospective linear percentiles: price ≤ −£11.22 or ≥ £153.8997/MWh; absolute NIV ≥ 876.0417 MWh. Inclusive ties are retained. These are transparent analytical review rules, not BSC limits, operational SLAs, incident counts or forecasts.

Two separately retrieved snapshots produced identical daily response hashes (92/92) and identical analytical outputs after excluding retrieval timestamps. See `reports/reproducibility-qa.md` for scope and exact comparisons.

## An investigation, not a causal story

On **13 October 2025, SP26**, the source price was £487/MWh and NIV was +184.9225 MWh: a short system and the quarter's highest price. It was selected after core data checks passed.

The official detailed price evidence contains three retained offer rows. Their transmission-loss-adjusted cost divided by volume, plus the reported adjuster, reconstructs £487/MWh; stack and summary creation timestamps agree. This supports the price-calculation mechanism. It does **not** establish why those actions were accepted, what caused the system condition or whether a service incident occurred.

The next check is targeted balancing-action and demand/generation evidence, with source vintages aligned before extending attribution. The lowest-price and largest-absolute-NIV cases also reconcile to penny precision. Only these three cases are reviewed at that depth; the other 127 remain Level 1 screening records.

## Evidence and controls

- **OBSERVED:** original authoritative source values and retained source records.
- **DERIVED:** deterministic calculations, classifications and reconciliations.
- **FLAG:** analyst screening and validation outcomes.
- **HYPOTHESIS:** an explanation that the available evidence has not established.

The controls cover required schemas, null/type/nonfinite core values, duplicate rows and date-period keys, expected coverage, dates and UTC timestamps, retrieval failures, bounded retries, source schema signatures, creation/retrieval ordering and snapshot-age review. Clock-change expectations come from consecutive London midnights in UTC: 46, 48 or 50 periods—not a universal 48.

Original response bytes are immutable and hash-checked. Invalid input stops analysis. Refresh marks the run `running` first and `failed` on error, so downstream consumers refuse preserved prior exports. Python/SQL crosschecks independently verify nine key aggregates. The current 38-test suite includes clock-change, malformed input, retry, source-vintage, hash integrity, idempotence and failed-refresh regressions.

## Architecture and Power BI

Official daily API → immutable response/manifest → executable controls → validated CSV/Parquet → Python screening + DuckDB SQL → structured investigations → Power BI / insight note / presentation

The semantic model has Date and Settlement Period dimensions, Settlement and Daily Controls facts, an Investigation fact and a disconnected whole-snapshot Source Controls table. Explicit measures have documented units and definitions. Daily completeness intentionally responds to date selection, not market-length filters.

| Report page | Decision supported |
|---|---|
| Settlement Service Monitor | What does this historical data snapshot show, and which periods require review? |
| Market & Settlement Analysis | How do distributions, system length, intraday patterns and NIV/price association differ? |
| Exception Investigation | What happened, what is known, what is not established and what should be checked next? |
| Data Quality & Controls | Can the selected snapshot be trusted, including retrieval and clock-change coverage? |

`powerbi/project/Settlement.pbip` is the entry point. The DataFolder parameter must point to this project's `data` directory on the machine performing refresh. Local files require an appropriate Desktop or gateway-supported service route. The checked-in definitions parse through the official Modeling MCP but are not a published report or proof that measures execute. Genuine screenshots, interaction checks and runtime performance evidence remain pending; current authenticated Fabric discovery returned `UserNotLicensed`.

## Deliverables and reviewer documents

- Service insight note: `reports/service-insight-note.pdf`.
- Editable presentation: `reports/presentation/settlement-service-intelligence.pptx`; reviewed PDF export: `reports/presentation/settlement-service-intelligence.pdf`.
- Presentation verification: `reports/presentation-qa.md`.
- Licensed Power BI close-out checklist: `reports/powerbi-live-verification-checklist.md`.
- Reproducibility audit: `reports/reproducibility-qa.md`.
- Definitions and analytical assumptions: `METHODOLOGY.md`.
- Domain/API/tool sources and benchmark references: `SOURCES.md` and `research/`.
- Measure definitions: `powerbi/measure-catalog.json`.
- Full brief, decisions and exact outstanding work: `PROJECT_SPEC.md`, `DECISIONS.md`, `PROJECT_STATE.md`.

No CV or interview claim should imply live deployment, Power BI runtime verification or proven market causality. Final career wording is deferred until the deliverables pass their verification gates.

## Reproduce the analysis

Run commands from this project directory. Tested with Python 3.14.6 and Node.js 24.14; Python package versions are pinned in `requirements.txt`. Public API requests require internet access; no API secret is used.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m src.ingest.client --start 2025-10-01 --end 2025-12-31
```

The fetch prints its new manifest path. Substitute that exact path below; do not select an incomplete snapshot. A new retrieval can legitimately contain revisions, so compare source vintages before expecting identical numbers.

```sh
.venv/bin/python -m src.pipeline --manifest data/raw/REPLACE_WITH_NEW_SNAPSHOT/manifest.json
.venv/bin/python -m src.analysis.investigate
.venv/bin/python -m src.analysis.reconcile
.venv/bin/python -m src.analysis.investigation_queue
node powerbi/build_model.mjs
node powerbi/build_report.mjs
```

The core pipeline is offline after retrieval. Detailed investigation retrieval is a separate network step and preserves its own context snapshot. Subsequent reconciliation and queue generation are offline. The insight-note builder uses ReportLab from `requirements.txt`. The editable presentation builder uses the Codex bundled `@oai/artifact-tool`; the checked-in PPTX/PDF can be reviewed without that authoring runtime. Node Power BI generators use built-in modules; Microsoft report-authoring validation requires the separately documented official tooling in `SETUP_REPORT.md`.

For the retained reference snapshot, replace the placeholder with `20260909T163243Z-dc4f225d`. To reproduce the independent rebuild without changing canonical outputs:

```sh
.venv/bin/python -m src.pipeline --manifest data/raw/20260909T170020Z-a1f525b9/manifest.json --output tmp/reproduction/processed
```

Raw and processed data are not committed by default. A fresh checkout must fetch them; the named retained snapshots are local review evidence, not a promise that those directories exist in every clone. See `data/README.md` for files and provenance.

## Repository map

```text
src/ingest/       Bounded public API retrieval and immutable receipts
src/validate/     Core calendar/schema/value controls and source/run status
src/transform/    Source-preserving deterministic mappings
src/analysis/     Descriptive screening and evidence-led investigation
sql/             Independent aggregations, rankings and exception selection
data/            Separate raw, processed and quality layers
powerbi/         Model/report generators, PBIP/PBIR and measure catalogue
reports/         Insight note, presentation and verification records
tests/           Executable regression controls
research/        Official-source discovery and design benchmarks
```

## Boundaries and sources

This is one historical quarter and a latest-message snapshot, not a live availability monitor, final-settlement guarantee, annual seasonal study, price forecast or customer billing analysis. It does not establish original publication timeliness. SP49/50 occur only on the autumn clock-change day; period-index averages are not universal local clock-time averages. Detailed calculation and daily-price sources may have different vintages even if prices agree.

Market definitions follow [Elexon's imbalance-pricing guidance](https://www.elexon.co.uk/bsc/settlement/imbalance-pricing/) and [BSC guidance](https://bscdocs.elexon.co.uk/guidance-notes/imbalance-pricing-guidance). API discovery uses the [official Elexon developer catalogue](https://developer.data.elexon.co.uk/api-details#api=prod-insol-insights-api). Power BI authoring follows [Microsoft's official tooling](https://github.com/microsoft/skills-for-fabric). The full source register records research limitations and the distinction between domain authority and open-source design benchmarks.
