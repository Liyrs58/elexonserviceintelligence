# Canonical version and 130-versus-124 reconciliation

Reviewed 10 September 2026. No methodology, percentile level or dashboard design was changed.

## Decision

The canonical project is **Q4 2025: 1 October–31 December 2025**. It is the successful data run referenced by the current output receipt and the population used by the PBIR/PBIP report, semantic-model inputs, presentation, service note and static design previews.

The **1 August–31 October 2025** result is a separate Cursor-era rebuild reported outside this repository. It is analytically valid for its own 92-day population, but it is not present in any commit, branch, reflog, unreachable object, retained dataset or current deliverable. It must not be mixed into canonical claims.

## Traceability

| Version | Dataset and analysis output | Repository lineage | Downstream use |
|---|---|---|---|
| Q4 2025 / 130 | `data/raw/20260909T163243Z-dc4f225d/manifest.json`, manifest SHA-256 `e2306fb3f865417ffb36d24d755199d3773ee9d5ac7763820556e326066f8555`; current `data/processed/run.json`, `summary.json`, `thresholds.json` and `settlement.csv` | Results first documented at `d781e7f`; semantic model `de88558`; binding/integrity hardening `4159b5c`; PBIR, presentation and service note `3694f57`; static previews `2369e25` | Current PBIR/PBIP, presentation, service note, screenshots, reviewer package, README and application wording |
| Aug–Oct 2025 / 124 | No original Cursor dataset or output is retained in this repository. Independently reproduced on 10 September with the unchanged current pipeline against official daily responses in an isolated temporary directory; reproduction manifest SHA-256 `807f5fec0d558c35417e3b61e8431964716055db64b8e293e3f2b92d4dd90000`, summary SHA-256 `a879dd953c24ffccec654410a366e244498eef9bb48ea62ee401d343413f6e7c`, thresholds SHA-256 `fcb2d17a7d7b0ef8bf3dbe4f8e5aa2cb7652b5513dbaa306c4e4b0cae84ce4e7` | No commit or Git object | Reconciliation evidence only; excluded from recruiter claims |

Raw and processed datasets are intentionally Git-ignored, so the Q4 dataset itself has no data commit. The table therefore distinguishes dataset provenance from the commits that introduced code and recruiter-facing outputs.

## Reproduced figures

| Measure | Aug–Oct | Q4 canonical |
|---|---:|---:|
| Records | 4,418 | 4,418 |
| Short / long / balanced | 1,971 / 2,445 / 2 | 2,076 / 2,340 / 2 |
| Price p01 / p99 | −£24.95 / £157 | −£11.22 / £153.8997 |
| Absolute-NIV p99 | 960.5836 MWh | 876.0417 MWh |
| Price flags | 95 | 92 |
| NIV flags | 45 | 45 |
| Joint flags | 16 | 7 |
| Distinct flags | 124 | 130 |

## Exact discrepancy

Both windows contain 4,418 periods because both cover 92 days and include the same 50-period autumn clock-change day. They do not contain the same observations: Q4 replaces August and September with November and December. The unchanged methodology estimates its percentiles over the complete selected window, so the reference distributions and cut-offs move when the population moves.

All 31 shared October response hashes match across the two independently retrieved snapshots, ruling out an October source-data revision. Under the August–October thresholds, October contains 38 flags. Under Q4's lower price/NIV cut-offs, those identical October observations contain 77 flags: the original 38 plus 39 additional cases. August–September contributes 86 flags; November–December contributes 53.

Therefore:

`Q4 130 = October 77 + November–December 53`

`Aug–Oct 124 = August–September 86 + October 38`

`130 − 124 = +39 reclassified October − 86 removed August–September + 53 added November–December = +6`

The set arithmetic also closes exactly:

- Q4: `92 price + 45 NIV − 7 joint = 130 distinct`.
- August–October: `95 price + 45 NIV − 16 joint = 124 distinct`.

The six-period difference is thus caused by a different analysis window, its different values and the resulting full-window empirical thresholds/overlaps. It is not threshold manipulation and not a contradiction within the current report.
