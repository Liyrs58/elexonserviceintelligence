# Power BI reviewer-package QA

Reviewed 10 September 2026 against `reports/elexon-powerbi-review-package.zip`.

## Result

- SHA-256: `b3850b4fc6c52e0b17f401d8064e3576d13b4afa6b18675fa0887fa1d8df6f3c`.
- Size: 1,235,800 bytes.
- Determinism: two consecutive builds produced the same archive hash.
- Archive integrity: ZIP test passed; 79 files are present, with 78 non-manifest files covered by `MANIFEST.sha256`.
- Fresh extraction: Microsoft's report validator returned zero errors and zero warnings.
- Fresh extraction: Microsoft's Modeling MCP loaded six tables, 19 measures and four relationships from the bundled TMDL folder.
- Data coverage: 92 Date rows, 50 Settlement Period rows, 4,418 settlement rows, 130 investigation rows, 92 daily-control rows and seven source-control rows, excluding CSV headers.
- Privacy/portability: no `/Users/rudra` path remains in the extracted package. `DataFolder` is a deliberate placeholder; the run receipt uses a relative manifest identifier and retains the authoritative manifest SHA-256.
- Exclusions confirmed: no raw API payloads, credentials, `.env`, private keys, Git metadata, local Power BI caches, virtual environments or Node package directories.

## Rebuild

Run `.venv/bin/python src/reporting/build_powerbi_review_package.py` after the canonical run marker is `success`. The builder copies an allowlist of report/model/data/reviewer files, sanitises machine-specific provenance paths, writes the internal manifest and emits a deterministic ZIP.

## Remaining boundary

Archive and definition checks do not execute M or DAX. A licensed Windows reviewer must still refresh, reconcile the 19 measures, test interactions/accessibility and capture Performance Analyzer evidence plus genuine report screenshots.
