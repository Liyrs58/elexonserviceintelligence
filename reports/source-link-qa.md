# Source-link QA

Checked 9 September 2026 using the URLs in `SOURCES.md`.

| Sources | Result |
|---|---|
| E3 Digital BSC guidance | Accessible; current page identifies Imbalance Pricing Guidance V16.0 as live from 14 July 2025. |
| E4 API developer catalogue | Accessible shell; endpoint content is loaded through the portal. Live API retrieval is independently evidenced by the two successful raw manifests. |
| E5 dated system-price API | Live retrieval succeeded for both immutable snapshots; the generic web reader would not open the query URL. |
| E7 detailed-system-prices | Accessible JavaScript application shell. |
| E10 official Insights issues | Accessible; describes official issue, announcement and incident scope. No coincident incident was established for the selected cases. |
| B1, B2 and M1 | Accessible public GitHub repositories. Used only for benchmarking/tool guidance. |
| T1-T5 | Accessible primary pandas, DuckDB, Requests, pytest and ReportLab documentation. |
| E1, E2, E6, E8 and E9 | Automated fetch returned HTTP 403. They remain official URLs, but the project does not treat inaccessible status content as proof of an incident or outage. Indexed text/research notes and Digital BSC are used where applicable. |

No source URL was silently replaced with a secondary market-definition source. Material domain claims retain official Elexon/BSC precedence.
