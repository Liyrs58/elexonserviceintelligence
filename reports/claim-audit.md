# Final claim audit

Reviewed 10 September 2026 across README, METHODOLOGY, Power BI definitions, insight note, presentation, version reconciliation, recruiter site, interview preparation and CV bullets.

## Supported and derived claims

| Claim | Class | Evidence |
|---|---|---|
| Q4 2025 contains 4,418 expected and received periods with zero core validation exceptions | DERIVED | `summary.json`, `daily_controls.csv`, `exceptions.csv`, calendar tests |
| 26 October has 50 periods; clock-day expectations are 46/48/50 | DERIVED | UTC elapsed-time calendar logic and spring/autumn tests |
| Mean/median/max/min price are 75.7241020665 / 74.705 / 487 / -30 GBP/MWh | DERIVED | Python summary and independent DuckDB cross-check |
| Maximum absolute NIV is 1,563.3382684622 MWh | DERIVED | Python summary and DuckDB cross-check |
| 2,076 short, 2,340 long and two balanced periods | DERIVED | sign classification, `length_summary.csv`, SQL cross-check |
| Short mean price 101.2391 versus long 53.0677 GBP/MWh | DERIVED | `length_summary.csv`; presented as a quarterly comparison, not cause |
| Pearson 0.6236 and Spearman 0.7631 association | DERIVED | `summary.json`; all narrative explicitly rejects causal interpretation |
| 130 distinct flags: 92 price, 45 imbalance, seven overlap | FLAG | fixed full-quarter threshold columns and independent exception count |
| Price thresholds -11.22 / 153.8997 and absolute-NIV threshold 876.0417 | FLAG | `thresholds.json`; labelled retrospective choices rather than BSC/SLA limits |
| 13 October SP26 price 487 and NIV +184.9225 | OBSERVED | hash-verified DISEBSP response and retained source fields |
| Three retained offer rows reconstruct £487/MWh; all three selected cases reconcile | DERIVED | hash-verified summary/stacks and `price_reconciliation.csv` |
| Two fresh daily snapshots match 92/92 response hashes and analytical outputs | SUPPORTED | `reports/reproducibility-qa.md` and isolated rebuild |
| Four PBIR pages, 39 visuals, six model tables and 19 ready-state measures exist | SUPPORTED | official CLI inventory, Modeling MCP parse and current PBIP/TMDL files |
| Four 1920 × 1080 static design previews reflect retained values and intended page layouts | SUPPORTED, NON-RUNTIME | canonical CSVs, official PBIR inventories, generator and visual QA record |
| Insight note is one reviewed page; presentation is eight reviewed pages/slides | SUPPORTED | rendered PDFs, presentation finalizer and PNG inspection records |
| Q4 is the current canonical report population; August–October's 124 is a separate-window result | SUPPORTED / FLAG | PBIR/TMDL bindings, current run receipt, Git history and isolated unchanged-pipeline reproduction documented in `version-reconciliation.md` |

## Domain claims

NIV sign/units and imbalance-price terminology use Elexon/BSC sources E1-E3. API schema and calculation context use E4-E5. Latest-message, vintage and indicative/final distinctions are stated as limitations. The project does not infer a service incident from a market extreme, failed web fetch or analytical flag.

## Hypotheses retained as hypotheses

The suggestion that retained action prices may explain price severity better than NIV magnitude remains explicitly labelled **HYPOTHESIS**. Demand, generation, action-acceptance and incident causes remain not established. The proposed evidence ladder is described as portfolio practice, not Elexon's official internal procedure.

## Unsupported-claim check

No output claims production-grade operation, real-time monitoring, automated root-cause analysis, official Elexon status, operational deployment, causal proof, Power BI DAX execution or a published Fabric report. The README and recruiter site's four images are prominently labelled static design previews, not genuine rendered Power BI screenshots. Career wording describes the report as built and structurally validated, not runtime-verified. No material unsupported claim remains in the reviewed deliverables.
