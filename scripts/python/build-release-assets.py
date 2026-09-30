#!/usr/bin/env python3
"""Build the release archives the catalogs point at.

Each extension and the preset is zipped as `<id>-<version>.zip` with the component directory as
the single top-level folder, which is the layout the specify CLI expects when it downloads a
catalog entry. The archives land in `dist/` (ignored by Git). Attach them to the GitHub release
whose tag matches the `download_url` entries in `extensions/catalog.json` and `presets/catalog.json`
(currently `v0.1.0`):

    python scripts/python/build-release-assets.py
    gh release create v0.1.0 dist/*.zip --title "MuleSoft Spec Kit 0.1.0" --notes-file CHANGELOG.md

Python 3.11+ standard library only.
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
EXCLUDED_DIRS = {"__pycache__", ".git"}
EXCLUDED_SUFFIXES = {".pyc"}


def manifest_version(manifest: Path) -> str:
    match = re.search(r'^\s+version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', manifest.read_text(encoding="utf-8"), re.M)
    if not match:
        raise SystemExit(f"no version found in {manifest}")
    return match.group(1)


def add_tree(archive: zipfile.ZipFile, source: Path, top_level: str) -> int:
    count = 0
    for path in sorted(source.rglob("*")):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(source).parts) or path.suffix in EXCLUDED_SUFFIXES:
            continue
        if path.is_file():
            archive.write(path, f"{top_level}/{path.relative_to(source).as_posix()}")
            count += 1
    return count


def build(source: Path, asset_name: str, top_level: str) -> None:
    target = DIST / asset_name
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        files = add_tree(archive, source, top_level)
    print(f"{target.relative_to(ROOT)}  ({files} files)")


def main() -> int:
    DIST.mkdir(exist_ok=True)
    for ext_dir in sorted((ROOT / "extensions").iterdir()):
        manifest = ext_dir / "extension.yml"
        if manifest.is_file():
            version = manifest_version(manifest)
            build(ext_dir, f"{ext_dir.name}-{version}.zip", ext_dir.name)
    preset_dir = ROOT / "presets" / "central-workspace"
    version = manifest_version(preset_dir / "preset.yml")
    build(preset_dir, f"central-workspace-preset-{version}.zip", "central-workspace")
    print("Attach these to the release named in the catalogs' download_url entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
