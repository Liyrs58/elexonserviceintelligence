# Elexon domain research and benchmark evidence

Research date: 9 September 2026. Official Elexon/BSC sources and the Elexon-maintained GitHub repository only. This document contains definitions and published reference facts, not results calculated from the project dataset.

## Definitions to implement

System Buy Price (SBP) and System Sell Price (SSP) are energy imbalance or cash-out prices for each half-hour trading period, associated with accepted balancing actions. Net Imbalance Volume (NIV) is measured in **MWh**, obtained by netting buy and sell balancing actions. **NIV > 0 means the system is short; NIV < 0 means the system is long.** Positive NIV ordinarily corresponds to offers that increase generation or decrease consumption; negative NIV to bids that decrease generation or increase consumption. Source: [Elexon imbalance pricing](https://www.elexon.co.uk/bsc/settlement/imbalance-pricing/).

Implementation decisions: classify exact zero separately as `Balanced (NIV = 0)`, retain null as `Unknown`, and never use the price sign as the system-length classifier. Keep SBP and SSP source fields and test their equality before exposing a single System Price field. Price unit is **GBP/MWh**. Negative System Prices are valid observations, not automatic data errors. Do not label System Price as a domestic tariff or a general wholesale market price. These are analytical safeguards, not additional claims about the official pricing algorithm.

Detailed formal price calculation guidance is available in [Digital BSC Imbalance Pricing Guidance](https://bscdocs.elexon.co.uk/guidance-notes/imbalance-pricing-guidance). The project should use published price outputs rather than claim to reproduce the full BSC algorithm from only price and NIV data.

## Settlement dates, UTC and daylight saving

Settlement Periods are half-hour intervals numbered within the **local** Settlement Day. Period 1 starts at local midnight. Ordinary days contain 48 periods; the spring clock-change day contains 46; the autumn clock-change day contains 50. Source: [Elexon Settlement, Settlement Periods](https://www.elexon.co.uk/bsc/settlement/).

The autumn repeat hour is explicitly demonstrated by Elexon: SP3 and SP4 start at 01:00 and 01:30 BST; SP5 and SP6 start at 01:00 and 01:30 GMT. Source: [Elexon clock-change explanation](https://www.elexon.co.uk/bsc/event/treatment-volume-notification-clock-change-day-28-october/).

Implementation: derive the expected calendar from consecutive Europe/London local midnights converted to UTC; step in 30-minute UTC intervals, then number those intervals. Use `(settlement_date, settlement_period)` as the business key and retain an unambiguous UTC start timestamp. Do not construct all local starts by adding `(SP-1)*30 minutes` to a naive local midnight, and do not assume every day has 48 observations. Repeated local clock labels require a timezone offset or UTC counterpart. A missing expected key is missing data, not a zero price.

## Indicative values and revisions

The official detailed-system-prices description says the indicative calculation is published 15 minutes after the effective Settlement Period using parameters available when it ran, and refreshed at D+1 for late or changed System Operator actions. Source: [Insights detailed system prices](https://bmrs.elexon.co.uk/detailed-system-prices). The Elexon launch notice describes the timing as approximately 15 minutes and explains that earlier output would omit relevant bid/offer and balancing-service information: [Indicative Settlement Price release notice](https://www.elexon.co.uk/bsc/article/indicative-settlement-price-data-now-available-on-the-insights-solution/).

Implementation: display extraction timestamp and source basis. Do not relabel a current API snapshot as final settlement. Publication-time lag, retrieval time and price revision are separate concepts. A historical snapshot alone does not prove the timeliness of original publication. Preserve source payloads and version/publish timestamps where supplied; only apply deduplication rules supported by the actual endpoint schema. Reconciliation against a report needs aligned settlement run and extraction basis.

## SPAR baseline and improvement opportunity

The [System Prices Analysis Report landing page](https://www.elexon.co.uk/bsc/data/system-prices-analysis-report/) was indexed as **September 2025**, with an explicit notice that the page is no longer updated and that current data is available through Insights. It describes a combination of II and SF Settlement Runs. Its established coverage includes long/short price summaries, distributions, daily and period averages, system length, accepted volumes, pricing parameters and a NIV-price scatter. This is a historical report-design benchmark, not a verified current operational feed.

Published September 2025 reference facts: 188 negative-price periods; maximum price GBP179.20/MWh; minimum GBP-89.87/MWh; 57% long periods. These must remain attributed reference facts unless independently reproduced using aligned data. The page has an apparent internal inconsistency: its headline means (long 36.30, short 102.70) differ from its later monthly-comparison paragraph (46.12 and 105.11). Do not use the latter paragraph as an automated numeric truth test.

Project opportunity (analyst assessment): complement the existing market analysis with explicit data coverage, extraction provenance, validation exceptions, clear business questions, accessible navigation and service-incident context. Avoid claiming that Elexon's own report lacks capabilities that were not directly inspected.

## Service and incident evidence

Elexon's [Service Status Dashboard explanation](https://www.elexon.co.uk/what-we-do/about-our-services/about-service-status-dashboard/) says the service covers Insights and other BSC platforms, including current availability and planned maintenance. It also distinguishes the dashboard from Circulars, which give fuller incident impact and advice. The candidate dashboard URL [status.elexon.co.uk](https://status.elexon.co.uk/) returned HTTP 403 to the research browser. **No current availability or outage claim is established by that access failure.**

The [Elexon Insights issues repository](https://github.com/elexon-data/insights-issues) covers website, API and IRIS issues plus announcements and planned outages. Its [issue list](https://github.com/elexon-data/insights-issues/issues) is accessible. Example: [issue 8](https://github.com/elexon-data/insights-issues/issues/8), opened 26 May 2023, describes large-range stream requests returning HTTP 500 and carries `confirmed`, `api` and `performance` labels. This is historical issue evidence; it does not prove a present failure, its duration, or an outage in the project extraction window.

Implementation: keep an incident/source register with source URL, observed date, issue/event date where known, affected service, source status and project relevance. Do not turn an issue count into service availability, infer incident durations from open/closed timestamps, or infer causation between an issue and a missing dataset record without matched evidence.

## Retrieval limitations

Several Elexon main-site opens returned 403/internal errors, while the web tool returned substantive indexed page extracts used above. Insights pages sometimes expose only a JavaScript shell on direct open. These limitations should be retained in the source log. The research establishes cited domain rules and historical reference content; it does not constitute a live UI inspection or endpoint payload validation. The [official API developer portal](https://developer.data.elexon.co.uk/) states APIs are public with no API key required, and provides schemas and parameter documentation for subsequent payload validation.
