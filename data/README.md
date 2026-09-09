# Data layers and provenance

Raw, processed and quality directories have different responsibilities. Do not edit source observations to make a control pass. Data outputs are excluded from version control by default and can be reproduced using the project README.

## Raw: authoritative response bytes

`raw/<timestamp>-<id>/` is a unique retrieval snapshot. Daily system-price retrieval preserves response bytes, per-request receipts and a terminal manifest containing URL, retrieval timestamp, status and SHA-256 hash. Only a successful manifest is eligible for analysis; a directory alone is not success evidence.

Canonical core snapshot: `raw/20260909T163243Z-dc4f225d/manifest.json`. It contains 92 successful daily responses for 1 October–31 December 2025 and 4,418 observations. Source basis is DISEBSP's latest settlement-run message, not necessarily final settlement.

Independent fresh snapshot: `raw/20260909T170020Z-a1f525b9/manifest.json`. All 92 response hashes matched the earlier snapshot. Different request/retrieval metadata is expected.

Detailed context snapshot: `raw/20260909T163543Z-context-afc7db2e/manifest.json`. Nine responses cover summary, bid stack and offer stack for three selected periods. Reconciliation verifies all manifest hashes and requires all three case files before using any evidence. Core and context source vintages remain distinct.

These names document retained local evidence. They are not included automatically in a fresh clone; a new fetch creates a new name. Preserve response files and manifests unchanged. If Elexon revises a response, retrieve a new snapshot rather than replacing an old one.

## Processed: deterministic analytical outputs

- `settlement.csv` / `settlement.parquet`: validated period-grain table; original source fields plus derived aliases, system length, absolute NIV, offset-aware local time, percentiles and flags.
- `dates.csv` / `periods.csv`: dimensions; date expectations are London-calendar-aware.
- `summary.json`, `thresholds.json`, `descriptive_statistics.csv`: numerical summaries and explicitly retrospective screening thresholds.
- `daily_summary.csv`, `period_summary.csv`, `length_summary.csv`: DuckDB aggregations.
- `price_distribution.csv`, `niv_distribution.csv`: display-bin counts, not exception thresholds.
- `extreme_periods.csv`, `exception_queue.csv`: ranked extremes and flagged period records.
- `field_provenance.csv`: field-level OBSERVED/DERIVED/FLAG metadata.
- `investigations.json` / `.csv`, `price_reconciliation.csv`: three selected investigations and saved-stack calculation checks.
- `investigation_queue.csv`: all 130 flags; only three claim detailed reviewed evidence.
- `run.json`: current build state and input manifest identity. Consumers must require `status: success` before reading exports. A failed refresh preserves previous files for recovery but invalidates their use as current successful output.

The core pipeline does not automatically refetch investigation context. When rebuilding from a different core vintage, rerun the investigation sequence in the project README before treating the combined output as a consistent review package.

## Quality: audit evidence

`exceptions.csv` and `.json` contain core control exceptions, including missing keys. `source_controls.csv` records retrieval/schema/source-time/revision-review statuses. `daily_controls.csv` summarises the validated successful snapshot; its zero-defect values must not be interpreted as the history of all attempted refreshes. `cross_system_validation.csv` contains nine independent Python/SQL numerical checks.

Expected coverage is 46/48/50 periods according to consecutive local midnights in UTC. The Q4 window contains the 50-period day on 26 October 2025; the 46-period spring case is separately tested.

A 30-day snapshot-age review is an analyst maintenance choice, not an Elexon service target. Historical source observations are not rejected merely because their settlement dates are old. API failure, analytical outlier and service incident are different concepts.

## Units and interpretation

Price is GBP/MWh; signed NIV is MWh. Positive NIV is short, negative is long and exact zero is labelled balanced. One System Price is used only after source buy/sell equality is verified. Source precision is retained; presentation rounding does not alter calculation inputs. No observations are imputed, clipped, silently deduplicated or removed as outliers.

The latest snapshot passing controls supports analysis of those observations. It does not establish original publication timeliness, finality, market cause or current Elexon service availability.
