# Project sources

Sources retrieved 9 September 2026. Research details and retrieval limitations are retained in research/domain-research.md and research/api-discovery.md. Setup references are in SETUP_SOURCES.md.

| ID | Source | Project use |
|---|---|---|
| E1 | https://www.elexon.co.uk/bsc/settlement/imbalance-pricing/ | NIV units/sign, imbalance-price context; indexed official text verified |
| E2 | https://www.elexon.co.uk/bsc/settlement/ | Settlement Day and Period definitions; official research |
| E3 | https://bscdocs.elexon.co.uk/guidance-notes/imbalance-pricing-guidance | Formal price-mechanism reference |
| E4 | https://developer.data.elexon.co.uk/api-details#api=prod-insol-insights-api | Current API schema catalogue |
| E5 | https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2025-10-26?format=json | Live DISEBSP response, 50 periods; all request URLs in raw manifest |
| E6 | https://www.elexon.co.uk/bsc/data/system-prices-analysis-report/ | Baseline analytical benchmark, discontinued September 2025 report; not a numeric reconciliation target |
| E7 | https://bmrs.elexon.co.uk/detailed-system-prices | Indicative/D+1 data context, distinct from latest settled DISEBSP |
| E8 | https://www.elexon.co.uk/what-we-do/about-our-services/about-service-status-dashboard/ | Official service-status scope |
| E9 | https://status.elexon.co.uk/ | Live incident status not established; research retrieval returned 403 |
| E10 | https://github.com/elexon-data/insights-issues | Official API issues and maintenance context, no coincident incident established |
| B1 | https://github.com/lptva/gb-power-dashboard | Provenance/methodology benchmark only, no copied code or market definitions |
| B2 | https://github.com/andrewlyden/PyPSA-GB | Reproducible configuration/source distinction benchmark only |
| M1 | https://github.com/microsoft/skills-for-fabric | Official semantic-model and report authoring/design guidance |

Every numerical project result derives from the manifest-named raw snapshot, then src/pipeline.py and sql/analysis.sql. Statistics are derived, source records observed, thresholds flags, and untested explanations hypotheses.
