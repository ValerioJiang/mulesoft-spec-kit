#!/usr/bin/env python3
"""Check that manifests, command files, catalogs and the command reference agree.

The same fact lives in several files here (a command's description, a component's version, the
asset a catalog points at), and nothing in the specify CLI ties them together. This script does:

    python scripts/python/check-consistency.py

It exits 1 and lists every disagreement. Needs PyYAML (`pip install pyyaml`).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
# The one command of the Spec Kit core that the preset leaves as it is.
CORE_COMMANDS = {"/speckit-constitution"}
# One name per thing (docs/concepts/central-workspace.md, Vocabulary): these are the retired ones.
RETIRED_TERMS = {
    "source repositor": "application repository",
    "source-repository": "application-repository",
    "<workspace-id>": "<source-workspace-id>",
    "exact workspace id": "exact source workspace ID",
    "exact workspace selection": "exact source workspace selection",
}
PLUGIN_MANIFEST = ("extensions/technical-solution/workspace/claude-marketplace/plugins/"
                   "mulesoft-spec-kit/.claude-plugin/plugin.json")
# Vendored upstream files keep upstream's command names.
VENDORED = ("extensions/sf-workspace/prompts/", "extensions/sf-workspace/sf-templates/",
            "extensions/sf-workspace/docs/", "extensions/sf-workspace/CHANGELOG.md")
problems: list[str] = []


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        problems.append(f"{label}: {actual!r} != {expected!r}")


def frontmatter_description(path: Path) -> str | None:
    match = re.search(r"^description:\s*(.+)$", path.read_text(encoding="utf-8"), re.M)
    return match.group(1).strip().strip('"') if match else None


def skill_name(command: str) -> str:
    return "/" + command.replace(".", "-")


def check_command(owner: str, base: Path, name: str, file: str, description: str) -> None:
    path = base / file
    if not path.is_file():
        problems.append(f"{owner}: {name} points at a missing file {file}")
        return
    expect(f"{owner}: {name} description (frontmatter of {file} vs manifest)",
           frontmatter_description(path), description)


def main() -> int:
    descriptions: dict[str, str] = {}
    tags: set[str] = set()

    extension_catalog = load_json(ROOT / "extensions" / "catalog.json")["extensions"]
    extension_versions: dict[str, str] = {}
    for directory in sorted((ROOT / "extensions").iterdir()):
        manifest_path = directory / "extension.yml"
        if not manifest_path.is_file():
            continue
        manifest = load_yaml(manifest_path)
        meta, provides, ext_id = manifest["extension"], manifest["provides"], directory.name
        expect(f"{ext_id}: extension.id", meta["id"], ext_id)
        extension_versions[ext_id] = meta["version"]
        for command in provides["commands"]:
            check_command(ext_id, directory, command["name"], command["file"], command["description"])
            descriptions[skill_name(command["name"])] = command["description"]
        declared = {command["file"] for command in provides["commands"]}
        for path in sorted((directory / "commands").glob("*.md")):
            if f"commands/{path.name}" not in declared:
                problems.append(f"{ext_id}: commands/{path.name} is not declared in extension.yml")
        for item in provides.get("templates", []) + provides.get("scripts", []):
            if not (directory / item["file"]).is_file():
                problems.append(f"{ext_id}: declared file {item['file']} is missing")

        entry = extension_catalog.get(ext_id)
        if entry is None:
            problems.append(f"{ext_id}: no entry in extensions/catalog.json")
            continue
        for field in ("name", "version", "description", "author", "license"):
            expect(f"{ext_id}: catalog {field}", entry.get(field), meta.get(field))
        expect(f"{ext_id}: catalog command count", entry["provides"]["commands"], len(provides["commands"]))
        expect(f"{ext_id}: catalog speckit_version", entry["requires"]["speckit_version"],
               manifest["requires"]["speckit_version"])
        match = re.search(r"/releases/download/([^/]+)/([^/]+)$", entry["download_url"])
        expect(f"{ext_id}: catalog asset name", match and match.group(2), f"{ext_id}-{meta['version']}.zip")
        if match:
            tags.add(match.group(1))
    for ext_id in extension_catalog:
        if ext_id not in extension_versions:
            problems.append(f"extensions/catalog.json lists {ext_id}, which has no directory")

    preset_dir = ROOT / "presets" / "central-workspace"
    preset = load_yaml(preset_dir / "preset.yml")
    preset_commands = [item for item in preset["provides"]["templates"] if item["type"] == "command"]
    preset_templates = [item for item in preset["provides"]["templates"] if item["type"] == "template"]
    for item in preset_commands:
        check_command("preset", preset_dir, item["name"], item["file"], item["description"])
        descriptions[skill_name(item["name"])] = item["description"]
    for item in preset_templates:
        if not (preset_dir / item["file"]).is_file():
            problems.append(f"preset: declared file {item['file']} is missing")
    entry = load_json(ROOT / "presets" / "catalog.json")["presets"]["central-workspace"]
    for field in ("name", "version", "description", "author", "license"):
        expect(f"preset: catalog {field}", entry.get(field), preset["preset"].get(field))
    expect("preset: catalog counts", entry["provides"],
           {"commands": len(preset_commands), "templates": len(preset_templates)})
    match = re.search(r"/releases/download/([^/]+)/([^/]+)$", entry["download_url"])
    expect("preset: catalog asset name", match and match.group(2),
           f"central-workspace-preset-{preset['preset']['version']}.zip")
    if match:
        tags.add(match.group(1))
    if len(tags) != 1:
        problems.append(f"catalog download_url entries point at more than one release tag: {sorted(tags)}")

    workflow = load_yaml(ROOT / "workflows" / "technical-solution" / "workflow.yml")["workflow"]
    entry = load_json(ROOT / "workflows" / "catalog.json")["workflows"]["technical-solution"]
    for field in ("name", "version", "description", "author"):
        expect(f"workflow: catalog {field}", entry.get(field), workflow.get(field))

    bundle = load_yaml(ROOT / "bundles" / "central-workspace" / "bundle.yml")
    entry = load_json(ROOT / "bundles" / "catalog.json")["bundles"]["central-workspace"]
    for field in ("name", "version", "description", "author", "license", "role"):
        expect(f"bundle: catalog {field}", entry.get(field), bundle["bundle"].get(field))
    for item in bundle["provides"]["extensions"]:
        expect(f"bundle: version of extension {item['id']}", item["version"], extension_versions.get(item["id"]))
    for item in bundle["provides"]["presets"]:
        expect(f"bundle: version of preset {item['id']}", item["version"], preset["preset"]["version"])
    for item in bundle["provides"]["workflows"]:
        expect(f"bundle: version of workflow {item['id']}", item["version"], workflow["version"])
    expect("bundle: catalog extension count", entry["provides"]["extensions"], len(bundle["provides"]["extensions"]))

    reference = (ROOT / "docs" / "reference" / "commands.md").read_text(encoding="utf-8")
    rows = dict(re.findall(r"^\| `(/speckit-[a-z-]+)` \| (.*) \|$", reference, re.M))
    for command, description in descriptions.items():
        if command not in rows:
            problems.append(f"docs/reference/commands.md has no row for {command}")
        else:
            expect(f"docs/reference/commands.md: {command}", rows[command], description)

    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-s"], capture_output=True, text=True, check=True)
    known = set(descriptions) | CORE_COMMANDS
    for line in tracked.stdout.splitlines():
        mode, _, _, name = line.split(maxsplit=3)
        if name.startswith("scripts/bash/") and name.endswith(".sh") and mode != "100755":
            problems.append(f"{name} is not executable in Git (mode {mode}); run git update-index --chmod=+x")
        if name.startswith("upstream/") or name.startswith(VENDORED) or not name.endswith((".md", ".yml", ".json")):
            continue
        text = (ROOT / name).read_text(encoding="utf-8")
        for mention in sorted(set(re.findall(r"/speckit-[a-z][a-z-]*[a-z]", text))):
            # `/speckit-mulesoft-*` and `/speckit-salesforce-<stage>` name a family, not a command.
            if mention not in known and not any(command.startswith(mention + "-") for command in known):
                problems.append(f"{name} mentions {mention}, which is not a command of this toolkit")
        if name != "CHANGELOG.md":  # the changelog may name what was retired
            lowered = text.lower()
            for retired, current in RETIRED_TERMS.items():
                if retired in lowered:
                    problems.append(f"{name} uses the retired term '{retired}'; the term is '{current}'")

    expect("Claude plugin version (follows the technical-solution extension that ships it)",
           load_json(ROOT / PLUGIN_MANIFEST)["version"], extension_versions.get("technical-solution"))

    if problems:
        print(f"{len(problems)} inconsistencies:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"consistent: {len(descriptions)} commands, {len(extension_versions)} extensions, release tag {tags.pop()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
