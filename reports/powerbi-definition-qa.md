# Power BI definition QA

Verified 9 September 2026. This audit distinguishes valid project files from execution in a licensed Power BI engine.

## Static definition result

The official Microsoft `powerbi-report-author` validator completed online schema validation with `0 error(s), 0 warning(s); result=succeeded` against `powerbi/project/Settlement.Report`.

CLI inventory confirms four 1920 × 1080 pages and 39 visuals:

| Page | Visuals | Purpose |
|---|---:|---|
| Settlement Service Monitor | 8 | status, aligned price/NIV trends and flagged-period queue |
| Market & Settlement Analysis | 12 | length comparison, distributions, intraday pattern and NIV/price association |
| Exception Investigation | 11 | one-event evidence record with known/not-established separation |
| Data Quality & Controls | 8 | whole-snapshot and daily validation evidence |

The monitor queue has one categorical visual filter for `Settlement[Exception] = true`. Its bound columns include event/date-period key, system length, price, NIV, flag reason, severity and quality status. Slicers exist for date, month, system length and investigation event; their runtime behaviour remains untested.

## Semantic-model definition

- Six tables: Date, Settlement Period, Settlement, Daily Controls, Source Controls and Investigation.
- Four single-direction relationships: Date to three facts and Settlement Period to Settlement.
- Nineteen explicit measures: 13 Settlement, five Daily Controls and one Date measure.
- All six import partitions check `processed/run.json` and raise an M error unless its status is `success`.
- Units, formats, descriptions and evidence-class annotations are present in TMDL and `powerbi/measure-catalog.json`.

The official Power BI Modeling MCP imported the current TMDL folder successfully and reported six loaded tables, 19 loaded measures and four loaded relationships. Model inventory confirmed Import storage, `en-GB`, `PowerBI_V3`, implicit measures discouraged, active many-to-one relationships and one-direction filtering. A batch retrieval of all 19 measures succeeded with zero failures; every measure returned `state = Ready`, an empty error message, and the intended expression, format, description and `EvidenceClass = DERIVED` annotation.

This MCP check initially failed on invalid TMDL indentation/property sequencing in date columns. The generator was corrected to emit ordinary format/sort properties before annotations, regenerated, and then loaded successfully. This is the material model-definition defect found during final validation.

Python and DuckDB independently agree on record count, average/median/min/max price, maximum absolute NIV, short/long counts and distinct exception count within `1e-8`; the current results are 4,418 rows, £75.7241020665 mean, £74.705 median, £487 maximum, -£30 minimum, 1,563.3382684622 MWh maximum absolute NIV, 2,076 short, 2,340 long and 130 flagged periods. These checks validate the intended measure results, not execution of the DAX expressions.

## Runtime boundary

The Modeling MCP connection is offline and rejects DAX query execution; it validates parsable object state but not calculated values. The report has not been refreshed or rendered in a licensed Power BI engine. The available Fabric identity returned `UserNotLicensed`, the browser requires Microsoft sign-in, the browser-control service was unavailable on the final continuation, and Power BI Desktop is unavailable on this Mac. Therefore M evaluation, DAX execution, filter/slicer interactions, accessibility in rendered visuals, empty states, visual clipping and performance remain **PENDING**. No dashboard screenshot is supplied or implied.
