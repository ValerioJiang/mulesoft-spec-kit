"""Load versioned source profiles and machine-local workspace roots."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from adapters import (
    RESOLVERS,
    ResolutionError,
    inspect_git_root,
    workspace_path,
)


WORKSPACE_MANIFEST = "spec-kit-workspace.json"


def central_workspace_root() -> Path:
    """Return the nearest ancestor of this script that holds the workspace manifest.

    The resolver may be installed at `.specify/scripts/source_workspaces/` or inside an
    extension directory, so the root is discovered rather than assumed at a fixed depth.
    """
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / WORKSPACE_MANIFEST).is_file():
            return candidate
    raise ResolutionError(f"{WORKSPACE_MANIFEST} not found in any parent of {here.parent}")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ResolutionError(f"required workspace configuration not found: {path.name}") from error
    except json.JSONDecodeError as error:
        raise ResolutionError(f"invalid JSON in {path.name}: line {error.lineno}, column {error.colno}") from error
    if not isinstance(value, dict):
        raise ResolutionError(f"workspace configuration must be a JSON object: {path.name}")
    return value


def _validate_fields(entry: dict[str, Any], required: list[str], optional: list[str], label: str) -> None:
    missing = set(required) - entry.keys()
    if missing:
        raise ResolutionError(f"{label} is missing: {', '.join(sorted(missing))}")
    unknown = entry.keys() - (set(required) | set(optional))
    if unknown:
        raise ResolutionError(f"{label} has unknown fields: {', '.join(sorted(unknown))}")


def load_registry(
    root: Path | None = None,
) -> tuple[Path, dict[str, Any], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    workspace_root = (root or central_workspace_root()).resolve()
    manifest = _read_json(workspace_root / "spec-kit-workspace.json")
    if manifest.get("schema_version") != 1:
        raise ResolutionError("unsupported spec-kit-workspace.json schema_version")

    resolution = manifest.get("source_resolution")
    if not isinstance(resolution, dict):
        raise ResolutionError("source_resolution is missing from spec-kit-workspace.json")
    config_value = manifest.get("source_workspace_config")
    if not isinstance(config_value, str) or Path(config_value).is_absolute():
        raise ResolutionError("source_workspace_config must be a relative path in spec-kit-workspace.json")
    config_path = (workspace_root / config_value).resolve()
    if not config_path.is_relative_to(workspace_root):
        raise ResolutionError("source_workspace_config escapes the central workspace root")
    if not config_path.is_file():
        template = f"{config_value}.template"
        raise ResolutionError(f"local source registry missing; copy {template} to {config_value} and configure it")

    config = _read_json(config_path)
    if config.get("schema_version") != 1:
        raise ResolutionError("unsupported local source registry schema_version")

    profile_collection = resolution.get("profile_collection")
    local_collection = resolution.get("local_collection")
    if not isinstance(profile_collection, str) or profile_collection not in manifest:
        raise ResolutionError("source_resolution.profile_collection is invalid")
    if not isinstance(local_collection, str) or not local_collection:
        raise ResolutionError("source_resolution.local_collection is missing")

    profiles = manifest[profile_collection]
    local_entries = config.get(local_collection)
    if not isinstance(profiles, list) or not isinstance(local_entries, list):
        raise ResolutionError("source workspace profiles and local roots must be arrays")

    profile_fields = resolution.get("profile_fields", [])
    optional_profile_fields = resolution.get("optional_profile_fields", [])
    local_root_fields = resolution.get("local_root_fields", [])
    optional_local_root_fields = resolution.get("optional_local_root_fields", [])
    field_declarations = (profile_fields, optional_profile_fields, local_root_fields, optional_local_root_fields)
    if not all(isinstance(value, list) and all(isinstance(field, str) for field in value) for value in field_declarations):
        raise ResolutionError("source workspace field declarations must be arrays")

    declared_resolvers = resolution.get("resolvers")
    if not isinstance(declared_resolvers, dict):
        raise ResolutionError("source_resolution.resolvers must be an object")
    absolute_roots_allowed = resolution.get("absolute_roots_allowed", False)
    if not isinstance(absolute_roots_allowed, bool):
        raise ResolutionError("source_resolution.absolute_roots_allowed must be a boolean")

    profile_ids: set[str] = set()
    for index, profile in enumerate(profiles):
        if not isinstance(profile, dict):
            raise ResolutionError(f"{profile_collection}[{index}] must be an object")
        _validate_fields(profile, profile_fields, optional_profile_fields, f"{profile_collection}[{index}]")
        identifier = profile.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", identifier):
            raise ResolutionError(f"invalid source workspace profile ID at {profile_collection}[{index}]")
        if identifier in profile_ids:
            raise ResolutionError(f"duplicate source workspace profile ID: {identifier}")
        profile_ids.add(identifier)
        if not isinstance(profile.get("domain"), str) or not profile["domain"].strip():
            raise ResolutionError(f"invalid domain for source workspace profile {identifier}")
        resolver_id = profile.get("resolver")
        if not isinstance(resolver_id, str) or resolver_id not in RESOLVERS or resolver_id not in declared_resolvers:
            raise ResolutionError(f"unregistered resolver for source workspace profile {identifier}: {resolver_id}")
        resolver_spec = declared_resolvers[resolver_id]
        if not isinstance(resolver_spec, dict):
            raise ResolutionError(f"resolver declaration must be an object: {resolver_id}")
        resolver_fields = resolver_spec.get("required_profile_fields", [])
        if not isinstance(resolver_fields, list) or not all(isinstance(field, str) for field in resolver_fields):
            raise ResolutionError(f"required_profile_fields must be an array of strings: {resolver_id}")
        missing_resolver_fields = set(resolver_fields) - profile.keys()
        if missing_resolver_fields:
            raise ResolutionError(
                f"source workspace profile {identifier} is missing resolver fields: "
                f"{', '.join(sorted(missing_resolver_fields))}"
            )
        if "expected_remote" in profile and (
            not isinstance(profile["expected_remote"], str) or not profile["expected_remote"].strip()
        ):
            raise ResolutionError(f"expected_remote must be a non-empty string for source workspace profile {identifier}")

    local_roots: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(local_entries):
        if not isinstance(entry, dict):
            raise ResolutionError(f"{local_collection}[{index}] must be an object")
        _validate_fields(entry, local_root_fields, optional_local_root_fields, f"{local_collection}[{index}]")
        identifier = entry.get("id")
        if not isinstance(identifier, str) or identifier not in profile_ids:
            raise ResolutionError(f"local root references an unknown source workspace profile: {identifier}")
        if identifier in local_roots:
            raise ResolutionError(f"duplicate local root for source workspace profile: {identifier}")
        if not isinstance(entry.get("root"), str) or not entry["root"].strip():
            raise ResolutionError(f"invalid local root for source workspace profile {identifier}")
        if Path(entry["root"]).is_absolute() and not absolute_roots_allowed:
            raise ResolutionError(f"absolute local roots are not allowed for source workspace profile {identifier}")
        local_roots[identifier] = entry

    return workspace_root, manifest, profiles, local_roots


def list_sources(root: Path | None = None, domain: str | None = None) -> list[dict[str, object]]:
    workspace_root, _, profiles, local_roots = load_registry(root)
    results: list[dict[str, object]] = []
    for profile in profiles:
        if domain and profile["domain"] != domain:
            continue
        identifier = profile["id"]
        local_entry = local_roots.get(identifier)
        resolver_id = profile["resolver"]
        results.extend(RESOLVERS[resolver_id]["list"](workspace_root, profile, local_entry))
    return sorted(results, key=lambda item: (str(item["domain"]), str(item["selection"])))


def resolve_source(selection: str, root: Path | None = None) -> dict[str, object]:
    workspace_root, _, profiles, local_roots = load_registry(root)
    identifier = selection.partition(":")[0]
    profile = next((item for item in profiles if item["id"] == identifier), None)
    if profile is None:
        raise ResolutionError(f"source workspace profile is not registered: {identifier}")
    local_entry = local_roots.get(identifier)
    resolver_id = profile["resolver"]
    return RESOLVERS[resolver_id]["resolve"](workspace_root, profile, local_entry, selection)


def resolve_explicit_root(path_value: str, domain: str, root: Path | None = None) -> dict[str, object]:
    if not domain.strip():
        raise ResolutionError("--domain is required with --root")
    workspace_root = (root or central_workspace_root()).resolve()
    selected_path = workspace_path(workspace_root, path_value)
    return inspect_git_root(
        selected_path,
        selection="explicit-root",
        source_workspace_id="explicit-root",
        domain=domain,
    )
