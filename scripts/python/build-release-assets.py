#!/usr/bin/env python3
"""Build the release archives the catalogs point at.

Each extension and the preset is zipped as `<id>-<version>.zip` with the component directory as
the single top-level folder, which is the layout the specify CLI expects when it downloads a
catalog entry. Files matched by a component's `.extensionignore` are left out, as they are when
the CLI installs from a directory. The archives land in `dist/<tag>/` (ignored by Git), where
`<tag>` is the release tag named by the `download_url` entries of `extensions/catalog.json` and
`presets/catalog.json`, so archives of an earlier release are never picked up by mistake:

    python scripts/python/build-release-assets.py
    gh release create <tag> dist/<tag>/*.zip --title "MuleSoft Spec Kit <version>" --notes "<changelog section>"

The script stops when a catalog entry names an archive it did not build. Python 3.11+ standard
library only.
"""
from __future__ import annotations

import fnmatch
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDED_DIRS = {"__pycache__", ".git", ".specify-dev"}
EXCLUDED_SUFFIXES = {".pyc"}


def manifest_version(manifest: Path) -> str:
    match = re.search(r'^\s+version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', manifest.read_text(encoding="utf-8"), re.M)
    if not match:
        raise SystemExit(f"no version found in {manifest}")
    return match.group(1)


def ignore_patterns(source: Path) -> list[str]:
    ignore_file = source / ".extensionignore"
    if not ignore_file.is_file():
        return []
    lines = (line.strip() for line in ignore_file.read_text(encoding="utf-8").splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def is_ignored(relative: str, patterns: list[str]) -> bool:
    """Match the subset of .gitignore syntax the components here use: names, paths and `dir/`."""
    for pattern in patterns:
        if pattern.endswith("/"):
            if relative.startswith(pattern) or f"/{pattern}" in f"/{relative}":
                return True
        elif "/" in pattern:
            if fnmatch.fnmatchcase(relative, pattern.lstrip("/")):
                return True
        elif fnmatch.fnmatchcase(relative.rsplit("/", 1)[-1], pattern):
            return True
    return False


def add_tree(archive: zipfile.ZipFile, source: Path, top_level: str) -> int:
    patterns = ignore_patterns(source)
    count = 0
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part in EXCLUDED_DIRS for part in relative.parts) or path.suffix in EXCLUDED_SUFFIXES:
            continue
        if path.name == ".extensionignore" or is_ignored(relative.as_posix(), patterns):
            continue
        if path.is_file():
            archive.write(path, f"{top_level}/{relative.as_posix()}")
            count += 1
    return count


def build(dist: Path, source: Path, asset_name: str, top_level: str) -> None:
    target = dist / asset_name
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        files = add_tree(archive, source, top_level)
    print(f"{target.relative_to(ROOT).as_posix()}  ({files} files)")


def catalog_assets() -> dict[str, str]:
    """Map every archive name the catalogs reference to its release tag."""
    assets: dict[str, str] = {}
    for catalog, key in (("extensions/catalog.json", "extensions"), ("presets/catalog.json", "presets")):
        entries = json.loads((ROOT / catalog).read_text(encoding="utf-8"))[key]
        for entry in entries.values():
            match = re.search(r"/releases/download/([^/]+)/([^/]+)$", entry["download_url"])
            if not match:
                raise SystemExit(f"{catalog}: {entry['id']} has no release download_url")
            assets[match.group(2)] = match.group(1)
    return assets


def main() -> int:
    expected = catalog_assets()
    tags = set(expected.values())
    if len(tags) != 1:
        raise SystemExit(f"the catalogs point at more than one release tag: {sorted(tags)}")
    tag = tags.pop()
    dist = ROOT / "dist" / tag
    dist.mkdir(parents=True, exist_ok=True)

    built: set[str] = set()
    for ext_dir in sorted((ROOT / "extensions").iterdir()):
        manifest = ext_dir / "extension.yml"
        if manifest.is_file():
            name = f"{ext_dir.name}-{manifest_version(manifest)}.zip"
            build(dist, ext_dir, name, ext_dir.name)
            built.add(name)
    preset_dir = ROOT / "presets" / "central-workspace"
    name = f"central-workspace-preset-{manifest_version(preset_dir / 'preset.yml')}.zip"
    build(dist, preset_dir, name, "central-workspace")
    built.add(name)

    if built != set(expected):
        raise SystemExit(
            "the catalogs and the manifests disagree on archive names: "
            f"catalogs only {sorted(set(expected) - built)}, built only {sorted(built - set(expected))}"
        )
    print(f"Attach these to release {tag}: gh release create {tag} dist/{tag}/*.zip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
