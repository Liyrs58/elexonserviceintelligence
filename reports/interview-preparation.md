# Interview preparation

All figures below refer only to the canonical Q4 2025 project: 1 October–31 December, 4,418 periods and 130 analytical flags.

## 30-second explanation

I built an independent service-intelligence project using public Elexon Settlement Period data. I validated all 4,418 expected Q4 2025 periods with Python and SQL, including the 50-period autumn clock-change day, then created an explainable review queue for 130 unusual System Price or Net Imbalance Volume periods. The four-page Power BI definition moves from controls to detection and investigation, while keeping observed facts, calculations and unproven explanations separate. Its definitions are structurally validated; live Power BI execution still needs a licensed environment.

## 90-second explanation

I built the project to demonstrate the work pattern behind a Settlement and Insight service role, not simply to make a price dashboard. The workflow is control, detect, investigate, communicate and recommend. I retrieved a hash-audited Q4 2025 snapshot from Elexon's public Insights API and validated schema, nulls, duplicates, timestamps, date-period keys and expected daily coverage. The calendar logic handles 46, 48 and 50-period days; the actual quarter contained 4,418 of 4,418 expected records and no core validation exceptions.

I then used transparent retrospective screening: the full-window 1st and 99th System Price percentiles and the 99th percentile of absolute NIV. That produced 130 distinct review flags—92 price flags and 45 NIV flags with seven overlaps. These are review rules, not BSC limits or incidents. Python and DuckDB independently agree on the core aggregates.

For three selected cases I retained official summary and bid/offer stack evidence and reconstructed the published price to penny precision. That validates the available calculation evidence, but it does not prove why the actions occurred or that a service incident happened. I translated this into a four-page Power BI project, a one-page service note and an eight-slide presentation. The PBIR and semantic model parse successfully with official Microsoft tools; I would use licensed Power BI Desktop next to refresh the model, execute DAX, test interactions and capture genuine runtime screenshots.

## Likely questions and defensible answer points

1. **Why did you build this?** To demonstrate analytical investigation, data controls, SQL, Power BI and cautious stakeholder communication using Elexon's own public data.
2. **What does Elexon do?** It administers the Balancing and Settlement Code arrangements and provides data/services supporting GB electricity balancing and settlement. Use the formal wording in `SOURCES.md` rather than claiming operational experience.
3. **What is a Settlement Period?** A half-hour settlement interval. Most Settlement Days contain 48, while clock changes can produce 46 or 50.
4. **What is System Price?** The imbalance cash-out price used in settlement; it is not a domestic electricity tariff.
5. **What is NIV?** Net Imbalance Volume in MWh. In this project, positive means system short, negative means system long and exact zero is classified as balanced.
6. **How did you validate the data?** Required-schema, null/type/nonfinite, duplicate row/key, coverage, date-range, period-range, UTC timestamp, source-signature, receipt/hash and run-status controls.
7. **Why are there 4,418 rather than 4,416 records?** Ninety-two ordinary days would imply 4,416, but 26 October is the autumn clock-change day with 50 rather than 48 periods, adding two.
8. **Why those exception thresholds?** They create a transparent retrospective review workload: price at or beyond the 1st/99th percentiles and absolute NIV at or beyond the 99th. They are not official thresholds; inclusive ties are retained.
9. **Why 130 rather than 124?** The report uses Q4. The 124 result belongs to August–October. The unchanged full-window method produces different empirical cut-offs and overlaps for the different population; `version-reconciliation.md` closes the arithmetic exactly.
10. **What did the selected investigation prove?** For three deliberately selected extremes, the retained detailed evidence reconstructs the published price to penny precision. It did not prove the underlying market cause or a service incident.
11. **Why does correlation not prove causation?** Q4 signed NIV and price are associated, but other balancing actions, system conditions, timing and common drivers are not controlled. The project reports Pearson and Spearman descriptively only.
12. **Where did SQL add value?** DuckDB independently recomputed nine material aggregates and generated daily, period, length, ranking, exception and duplicate views; mismatches beyond 1e-8 stop the pipeline.
13. **What is in the Power BI model?** Six tables, four single-direction relationships, 19 explicit measures and four report pages supporting monitoring, market analysis, investigation and controls.
14. **What remains unverified in Power BI?** Live M refresh, DAX execution, slicer/filter behaviour, accessibility, performance and genuine runtime rendering because Power BI Desktop is not native to this Mac and the available service identity is unlicensed.
15. **What would you build next?** Freeze a prior reference window for prospective monitoring, test workload stability over more seasons, align additional source vintages and complete licensed Power BI runtime QA before making any operational claim.

## Do not overclaim

Say “portfolio project”, “historical snapshot”, “analytical flags”, “structurally validated Power BI definitions” and “recommended next checks”. Do not say “production system”, “real-time monitor”, “root cause identified”, “incident detected”, “official Elexon dashboard” or “Power BI runtime verified”.
