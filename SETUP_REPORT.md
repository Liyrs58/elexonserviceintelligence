# Power BI environment and verification boundary

Verified on 9 September 2026 on macOS 13.4 (`arm64`). This file records the current state; earlier setup probes are superseded.

## Available locally

- Node.js 24.14 and Python 3.14.6.
- Official Microsoft `skills-for-fabric` checkout pinned in `SETUP_SOURCES.md` under ignored local tooling.
- Microsoft semantic-model, report-design, report-authoring and report-management skills exposed locally.
- `powerbi-report-author` CLI 0.1.4.
- Official Power BI Modeling MCP registered locally. No callable modeling operations were exposed in this task, so no engine-level result is claimed.
- In-app browser/computer use works and can reach Power BI Service.

## Current report evidence

`powerbi/project/Settlement.pbip` links a generated TMDL semantic model and four-page PBIR report. The official report-authoring validator completed with zero errors and zero warnings, including Microsoft JSON-schema validation. This proves file structure, field bindings and supported report metadata. It does not execute M or DAX.

The semantic model contains six tables, four one-direction relationships and 19 explicit measures. Every import query reads `data/processed/run.json` first and rejects preserved exports unless the latest run status is `success`. The model parameter `DataFolder` must point to the local project `data` directory before refresh.

## External runtime result

- Power BI Service is reachable in the in-app browser, but the session is at Microsoft sign-in.
- The available Azure identity returned `UserNotLicensed` for Fabric workspace discovery.
- Power BI Desktop and its bridge are not available natively on this Mac.
- Therefore the report has not been loaded into a licensed engine. M refresh, DAX results, slicers, visual rendering, accessibility in the rendered report and performance remain unverified.

## Exact local validation

```sh
node powerbi/build_model.mjs
node powerbi/build_report.mjs
.tools/powerbi-cli/node_modules/.bin/powerbi-report-author validate powerbi/project/Settlement.Report
```

The first two commands are deterministic generators. The third requires the locally installed official Microsoft CLI. It reported `0 error(s), 0 warning(s); result=succeeded` on the current report.

## Smallest action to finish live verification

Open `powerbi/project/Settlement.pbip` in a licensed Power BI Desktop environment, set `DataFolder` to the project `data` directory, refresh, and capture all four pages after confirming the 19 measures and slicers. Alternatively, sign in to a licensed Fabric/Power BI Service workspace that supports this local-file model. Do not describe the report as runtime-verified or use a dashboard screenshot until those checks pass.
