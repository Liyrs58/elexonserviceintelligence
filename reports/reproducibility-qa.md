# Reproducibility and fail-closed QA

Verified 9 September 2026. This is local Python/SQL evidence, not Power BI runtime verification.

## Fresh retrieval rebuild

Rebuilt the independently retrieved snapshot `data/raw/20260909T170020Z-a1f525b9/manifest.json` into the isolated `tmp/reproduction/processed` directory. Canonical processed files and raw snapshots were not modified.

```sh
.venv/bin/python -m src.pipeline --manifest data/raw/20260909T170020Z-a1f525b9/manifest.json --output tmp/reproduction/processed
.venv/bin/python -m pytest -q
```

Both snapshots have 92 successful daily responses. All 92 corresponding response SHA-256 hashes agree exactly. The manifests differ as expected because they describe separate requests and retrieval times:

- Original manifest: `e2306fb3f865417ffb36d24d755199d3773ee9d5ac7763820556e326066f8555`.
- Fresh manifest: `28899cfb7eeff0d94c7933ea3a86e1df6daa87584b38ee9497a7334eaa9ab4c1`.

Exact pandas frame comparisons (`check_exact=True`) passed for all 13 pipeline CSV outputs: daily_summary, dates, descriptive_statistics, duplicate_keys, exception_queue, extreme_periods, field_provenance, length_summary, niv_distribution, period_summary, periods, price_distribution and settlement. Settlement comparison covered 4,418 rows × 43 columns after excluding only `retrieved_at`. All other CSV columns were compared.

Parquet was read through the installed DuckDB engine and compared exactly: the same 4,418 × 43 values agree, excluding only retrieval timestamps. Pandas' optional Parquet reader is not installed; this is not required by the pipeline, which writes and reads Parquet through DuckDB.

All 20 non-retrieval fields in summary.json and all six thresholds.json fields agree exactly. Quality comparisons agree exactly: zero exception rows, 92 daily controls, nine Python/SQL crosschecks. All seven source-control names/statuses agree; time-dependent snapshot-age detail was excluded.

Reproduced results: 4,418 observations/expected periods; mean price 75.72410206646799 GBP/MWh; median 74.705; maximum 487; minimum −30; maximum absolute NIV 1563.3382684622015 MWh; 130 distinct flagged periods; 2,076 short, 2,340 long and two balanced periods; completeness 1.0.

This establishes reproducibility for two retrievals on the same day, not permanent absence of future source revisions. It does not independently reretrieve the detailed investigation stacks.

## Regression evidence

Three initial regression tests failed before the fixes: altered context was not hash-rejected; repeated reconciliation changed the output; a failed refresh left a previous successful run marker. After fixes those tests pass.

Twelve additional tests initially failed because investigate, reconcile and investigation_queue did not reject missing/malformed/running/failed run markers before reading exports. A shared `require_successful_run` guard now rejects all twelve cases. Final suite at this audit: **38 passed**.

Context reconciliation now checks every receipt hash and requires the case's summary, bid and offer evidence in the manifest. Generated reconciliation text is replaced rather than appended; unsuccessful reconciliation resets prior success commentary/status. Pipeline refresh marks its run running before work and failed on exceptions. Previous exports are retained for recovery, but consumers must refuse them unless the current run marker says success.

Synthetic regression fixtures live in temporary directories. No real production source response was edited. Power BI imports require a matching guard; the root reviewer verifies that separately. Rendering, DAX evaluation, filter behaviour, report screenshots and licensed-runtime validation are outside this test's scope.
