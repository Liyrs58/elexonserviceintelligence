"""Build the deterministic, privacy-safe Power BI reviewer ZIP."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "reports" / "elexon-powerbi-review-package.zip"
PACKAGE_ROOT = "elexon-powerbi-review"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

FILES = (
    "powerbi/project/Settlement.pbip",
    "powerbi/measure-catalog.json",
    "data/processed/dates.csv",
    "data/processed/periods.csv",
    "data/processed/settlement.csv",
    "data/processed/investigation_queue.csv",
    "data/quality/daily_controls.csv",
    "data/quality/source_controls.csv",
    "reports/powerbi-reviewer-handoff.md",
    "reports/powerbi-live-verification-checklist.md",
    "reports/powerbi-definition-qa.md",
    "reports/powerbi-static-preview-qa.md",
    "screenshots/README.md",
    "screenshots/powerbi-static-preview-01-monitor.png",
    "screenshots/powerbi-static-preview-02-analysis.png",
    "screenshots/powerbi-static-preview-03-investigation.png",
    "screenshots/powerbi-static-preview-04-controls.png",
)

DIRECTORIES = (
    "powerbi/project/Settlement.Report",
    "powerbi/project/Settlement.SemanticModel",
)

TREE_FILE_SUFFIXES = {".json", ".pbir", ".pbism", ".tmdl"}
TREE_FILE_NAMES = {".platform"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_inputs(destination: Path) -> None:
    for relative in FILES:
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for relative in DIRECTORIES:
        source_root = ROOT / relative
        for source in sorted(p for p in source_root.rglob("*") if p.is_file()):
            if source.suffix not in TREE_FILE_SUFFIXES and source.name not in TREE_FILE_NAMES:
                continue
            target = destination / relative / source.relative_to(source_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def write_sanitized_run_receipt(destination: Path) -> None:
    source = ROOT / "data" / "processed" / "run.json"
    run = json.loads(source.read_text(encoding="utf-8"))
    if run.get("status") != "success":
        raise RuntimeError("Reviewer package requires a successful canonical pipeline run")
    manifest_path = Path(run.get("manifest", "unknown"))
    manifest_id = manifest_path.parent.name if manifest_path.name == "manifest.json" else "unknown"
    run["manifest"] = f"data/raw/{manifest_id}/manifest.json (not bundled)"
    run["package_note"] = "Raw API responses are intentionally excluded; provenance is retained by manifest_sha256."
    target = destination / "data" / "processed" / "run.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")


def write_reviewer_readme(destination: Path) -> None:
    source = destination / "reports" / "powerbi-reviewer-handoff.md"
    shutil.copy2(source, destination / "README_FOR_POWER_BI_REVIEWER.md")


def assert_portable(destination: Path) -> None:
    for path in (p for p in destination.rglob("*") if p.is_file()):
        content = path.read_bytes()
        if b"/Users/" in content or b"/home/" in content:
            raise RuntimeError(f"Machine-specific home path remains in package input: {path}")


def write_manifest(destination: Path) -> None:
    rows = []
    for path in sorted(p for p in destination.rglob("*") if p.is_file()):
        relative = path.relative_to(destination).as_posix()
        rows.append(f"{sha256(path)}  ./{relative}")
    (destination / "MANIFEST.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_zip(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            relative = Path(PACKAGE_ROOT) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="elexon-powerbi-review-") as temp:
        staged = Path(temp) / PACKAGE_ROOT
        staged.mkdir()
        copy_inputs(staged)
        write_sanitized_run_receipt(staged)
        write_reviewer_readme(staged)
        assert_portable(staged)
        write_manifest(staged)
        write_zip(staged, OUTPUT)
    print(json.dumps({"path": str(OUTPUT), "sha256": sha256(OUTPUT), "bytes": OUTPUT.stat().st_size}))


if __name__ == "__main__":
    main()
