# Methodology

## Scope and analytical purpose

This independent portfolio study examines GB Settlement Period observations for 1 October–31 December 2025. It demonstrates CONTROL → DETECT → INVESTIGATE → COMMUNICATE → RECOMMEND. A historical snapshot does not establish present service availability, original publication timeliness, or deployment of an operational monitor.

## Sources and definitions

Elexon administers the Balancing and Settlement Code arrangements. Imbalance settlement accounts for differences between contracted and actual energy positions. System Buy/Sell Prices are imbalance (cash-out) prices, not domestic tariffs. Refer to SOURCES.md E1–E4 and the official BSC guidance for formal definitions and the full calculation.

Observed prices are GBP/MWh and NIV is MWh. Positive NIV means system short, negative NIV means system long (E1). Exact zero is classified Balanced for this analysis. This is system-level classification, not a statement about an individual party's imbalance.

The chosen DISEBSP API publishes the latest settlement-run message per period. It differs from the indicative price feed, whose initial/D+1 publication behaviour must not be attributed to DISEBSP. No final-settlement or historical-vintage guarantee is inferred. Source creation and retrieval timestamps are retained separately.

## Evidence classes

OBSERVED means original authoritative source fields, including buy/sell prices, NIV and stack values. DERIVED means deterministic calculations such as absolute NIV, averages, system length and price reconciliation. FLAG means percentile screening and quality-control exceptions. HYPOTHESIS means an explanation not established by the available observations. The raw source fields remain in the processed table alongside derived fields. Model metadata and investigation records must preserve these distinctions.

## Time and coverage

A Settlement Day follows Europe/London local time. Expected periods are calculated from the elapsed UTC time between consecutive local midnights divided by 30 minutes. This yields 46, 48 or 50; it is never hard-coded to 48. The natural key is Settlement Date × Settlement Period. UTC start timestamps are compared with an independently generated calendar. Local display timestamps include offsets, so repeated autumn 01:00 times are distinguishable.

Q4 has 4,418 expected periods, including 50 on 26 October. The spring transition is outside the window and is covered by a separate test. Intraday summaries by period index include unequal sample counts for SP49/50; do not treat these as quarter-wide clock-time averages. Normal-day clock-time comparisons should exclude the clock-change day or use explicit offset-aware local time.

## Raw and processed layers

Each retrieval creates a unique directory. Response bytes are written exclusively to new files, and SHA-256 hashes are recorded in the manifest. Rebuilding checks hashes before parsing. Transformations copy records without changing raw files. No imputation, deduplication, clipping or outlier removal is performed. Core control errors stop analysis and leave machine-readable exceptions.

Both source buy and sell prices are preserved. A single System Price is exposed only after equality is verified. Negative prices and optional context nulls are legitimate; neither is automatically a core-data defect. Original precision is retained through Python/CSV/Parquet. Display rounding is separate from calculations.

## Screening methodology

Price tails are at or below the full-window 1st percentile or at or above the 99th percentile. Absolute NIV is flagged at or above its 99th percentile. Quantiles use linear interpolation. These percentile levels are an explicit analytical review-workload choice, not official BSC thresholds. Inclusive ties remain together, so the population can exceed a nominal tail share. Constant data generates no tail flags.

This is retrospective screening: the observation contributes to its own reference distribution. It is not an out-of-sample detector. A future monitoring implementation should freeze a prior-window reference and evaluate workload/stability. Flags indicate unusual values, not errors, incidents or probability of harm.

Empirical percentiles use rank(method=max)/N, placing ties at the upper rank. A descriptive robust price score uses (price−median)/(1.4826×MAD); if MAD is zero the implementation returns zero and does not use this score as a flag. Pearson and Spearman correlations describe association, never causation. No inference assumes independent half-hours or supplies misleading significance tests for serial data.

## Investigation method

Three deliberate cases cover maximum price, minimum price and largest absolute NIV. First check the core controls and rankings. Then inspect available accepted/adjustment volume context. Finally retrieve official summary and both bid/offer stacks for the exact date/period. Preserve their creation times and retrieval snapshots.

Price reconciliation sums transmission-loss-adjusted cost and volume over rows with non-zero PAR-adjusted volume on the relevant side, divides cost by volume, adds the reported adjuster, and compares to the source price within GBP0.005/MWh. This tolerance tests agreement at penny display precision, not exact binary floating-point identity. The stack and summary timestamps are checked for alignment. Reconciliation supports the published price mechanism; it does not prove the underlying cause of the market condition. DISEBSP and detailed calculations may represent different vintages even when their rounded prices agree.

## Controls and independent checks

Executable controls cover required schema, core null/type/nonfinite values, duplicate rows/keys, expected coverage, date-window membership, period range, aware UTC timestamps and calendar agreement. Ingestion bounds retries for HTTP429/5xx and connection/timeouts, rejects empty/malformed envelopes and missing source fields, and preserves successful response bytes before parsing. Optional source fields are not required to be non-null.

SQL independently computes record count, average/median/minimum/maximum price, maximum absolute NIV, short/long counts and exception count. Differences greater than 1e-8 stop the pipeline. DAX execution and visual/filter verification remain required separately and cannot be established by a Python/SQL pass.

## Limitations and unfinished controls

Only one quarter and one retrieval vintage are analysed. Results are not annual seasonality, forecasts, customer billing impacts or service-availability statistics. No incident attribution is established. The official status site was inaccessible to the research fetch; that is not proof of an outage. Power BI Service returned UserNotLicensed with the existing Azure identity; live model/report verification is pending.

Source audit compares field signatures across daily responses, validates creation/retrieval timestamps and marks snapshots older than 30 days for revision review. The 30-day period is a documented portfolio review policy, not an Elexon SLA. Source dates are historical by design. Interrupted retrieval preserves a terminal manifest; per-request receipts survive interruption between requests. A hard operating-system kill can still prevent finalisation, so snapshots without a success manifest are never eligible for analysis.
