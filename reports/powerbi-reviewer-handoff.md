# Power BI reviewer handoff

Use this guide on a Windows machine with a current licensed Power BI Desktop installation. The package is self-contained for report review; no Elexon API call or secret is required.

## Open and refresh

1. Extract `elexon-powerbi-review-package.zip` to a short local path, for example `C:\elexon-review`.
2. Verify `MANIFEST.sha256` if your organisation's tooling supports SHA-256 checks.
3. Open `powerbi\project\Settlement.pbip` in Power BI Desktop.
4. In **Transform data → Edit parameters**, replace the deliberate `REPLACE_WITH_ABSOLUTE_PATH_TO_PROJECT_DATA` placeholder with the extracted `data` folder, for example `C:\elexon-review\data`.
5. Apply changes and refresh. Do not publish or enter credentials; every model source is a local CSV in the package.
6. Follow `reports\powerbi-live-verification-checklist.md` in full. It records all 19 expected measure values, filter-context checks, page checks, performance requirements and required screenshot names.

## Already verified before handoff

- Python/DuckDB analysis and 38 tests pass.
- Microsoft's report validator reports zero errors and zero warnings across four PBIR pages and 39 visuals.
- Microsoft's Modeling MCP imports six tables, four relationships and all 19 measures in ready state.
- The four included `screenshots\powerbi-static-preview-*.png` files are visually inspected design previews built from the retained data. They are not runtime screenshots and must not be used to sign off the checklist.
- Machine-specific absolute paths are removed from the package. The run receipt retains the authoritative source-manifest hash while noting that raw API responses are intentionally excluded.

## Return evidence

Please return the four genuine page screenshots named by the checklist, the Power BI Desktop version, refresh result, all 19 measure comparisons, interaction/accessibility notes, and Performance Analyzer evidence. Record any mismatch without editing the expected values. With that evidence, the remaining runtime gate can be closed or a targeted correction can be made.
