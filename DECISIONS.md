# Decisions

## 9 September 2026

- Use Q4 2025 (1 October–31 December), a complete historical quarter with 92 days and the autumn clock change. Live full-window retrieval proves 4,418 records. This window supports descriptive comparisons, not annual seasonality or current service availability.
- Use the documented DISEBSP daily system-prices endpoint. Preserve latest settlement-run responses, both buy/sell prices, source timestamps, request timestamps, URLs and SHA-256 hashes. Do not describe a latest-message snapshot as final settlement.
- Derive one System Price only when buy and sell source prices agree. NIV remains signed MWh, with exact zero classified separately.
- Screen retrospectively with full-window 1st/99th price percentiles and 99th absolute-NIV percentile, linear interpolation and inclusive ties. These are transparent review-workload choices, not BSC limits or predictive anomaly probabilities. Ties mean flagged populations can exceed exact 1% tails. Constant series produce no tail flags.
- Use DuckDB in memory for independent SQL aggregation and CSV/Parquet for reproducible local outputs. No server infrastructure is needed.
- Investigate maximum price, minimum price and maximum absolute NIV as distinct cases. Price severity and imbalance magnitude are different investigation questions.
- Power BI browser is available but at sign-in. Existing Azure-authenticated Fabric workspace discovery returned UserNotLicensed on 9 September. Continue local PBIP/PBIR authoring; live DAX/rendering requires a licensed environment. Do not claim screenshots or runtime verification before obtaining them.
- Current subagents stopped at an account usage limit. Root continues from saved files.
- Semantic model uses six tables: Date and Settlement Period dimensions, Settlement and Daily Controls facts, an Investigation fact with all 130 flagged cases, and a disconnected whole-snapshot Source Controls audit table. Daily completeness responds to dates, not market-length filters. Only three investigation records claim detailed price evidence.
- Retain binary-double source precision for price/NIV model columns instead of fixed four-decimal currency storage, because some original values have more than four decimal places. This is a deliberate exception to the skill's fixed-decimal preference; display formatting uses sensible units/precision and independent checks allow 1e-8 aggregate tolerance. Live DAX execution remains unverified.
- Snapshot age review at 30 days is an analyst-maintenance policy, not evidence that the historical observations became wrong or an Elexon service target.
