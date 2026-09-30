"""Registered source workspace resolvers shared by all Spec Kit skills."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


class ResolutionError(ValueError):
    """Raised when a source workspace cannot be resolved unambiguously."""


def workspace_path(workspace_root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (workspace_root / path).resolve()


def catalog_manifest_path(catalog_root: Path, value: str) -> Path:
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or "\\" in value:
        raise ResolutionError(f"catalog manifest path must stay under its workspace root: {value}")
    candidate = (catalog_root / Path(*relative.parts)).resolve()
    if not candidate.is_relative_to(catalog_root.resolve()):
        raise ResolutionError(f"catalog manifest path escapes its workspace root: {value}")
    return candidate


def catalog_repository_path(catalog_root: Path, value: str) -> Path:
    relative = PurePosixPath(value)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts or "\\" in value:
        raise ResolutionError(f"catalog repository path must be relative and stay under its workspace root: {value}")
    candidate = (catalog_root / Path(*relative.parts)).resolve()
    if not candidate.is_relative_to(catalog_root.resolve()):
        raise ResolutionError(f"catalog repository path escapes its workspace root: {value}")
    return candidate


def read_path_remote_manifest(catalog_root: Path, manifest_value: str) -> list[dict[str, str]]:
    manifest_path = catalog_manifest_path(catalog_root, manifest_value)
    if not manifest_path.is_file():
        raise ResolutionError(f"source catalog manifest not found: {manifest_value}")

    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for line_number, raw_line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        fields = re.split(r"\s+", line, maxsplit=1)
        if len(fields) != 2 or not fields[1] or re.search(r"\s", fields[1]):
            raise ResolutionError(f"invalid path/remote entry in {manifest_value} at line {line_number}")
        relative_path, remote = fields
        catalog_repository_path(catalog_root, relative_path)
        if relative_path in seen:
            raise ResolutionError(f"duplicate repository path in {manifest_value}: {relative_path}")
        seen.add(relative_path)
        entries.append({"relative_path": relative_path, "remote": remote})
    return entries


def remote_identity(value: str) -> tuple[str, str]:
    candidate = value.strip()
    parsed = urlparse(candidate)
    if parsed.netloc:
        host, path = parsed.hostname or "", parsed.path.lstrip("/")
    else:
        scp_match = re.fullmatch(r"(?:[^@/]+@)?([^:/]+):(.+)", candidate)
        if not scp_match:
            raise ResolutionError("repository remote has an unsupported format")
        host, path = scp_match.groups()
    if not host or not path or re.search(r"\s", path):
        raise ResolutionError("repository remote has an unsupported format")
    return host.lower(), path.removesuffix(".git").rstrip("/")


def sanitized_remote(value: str | None) -> str | None:
    """Return `host/path` for a network remote, or None when there is no portable identity.

    A remote that is a filesystem path identifies nothing outside this machine, and reporting
    it would leak a local path into the initiative artifacts.
    """
    if not value:
        return None
    try:
        host, path = remote_identity(value)
    except ResolutionError:
        return None
    return f"{host}/{path}"


def run_git(repository_path: Path, *arguments: str, required: bool = True) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repository_path), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise ResolutionError("git executable not found on PATH; install Git or add it to PATH") from error
    if result.returncode != 0:
        if required:
            detail = result.stderr.strip() or "git command failed"
            raise ResolutionError(f"cannot inspect selected Git repository: {detail}")
        return None
    return result.stdout.strip()


def inspect_git_root(
    repository_path: Path,
    *,
    selection: str,
    workspace_id: str,
    domain: str,
    expected_remote: str | None = None,
) -> dict[str, object]:
    if not repository_path.is_dir():
        raise ResolutionError(f"selected repository path does not exist: {selection}")

    actual_root_text = run_git(repository_path, "rev-parse", "--show-toplevel")
    actual_root = Path(actual_root_text or "").resolve()
    expected_root = repository_path.resolve()
    if actual_root != expected_root:
        raise ResolutionError(f"selected path is not the Git root for {selection}")

    remote = run_git(repository_path, "remote", "get-url", "origin", required=False)
    if expected_remote:
        try:
            expected_identity = remote_identity(expected_remote)
        except ResolutionError as error:
            raise ResolutionError(
                f"registered remote for {selection} is not a host-based URL (https://host/path or host:path)"
            ) from error
        if sanitized_remote(remote) != "/".join(expected_identity):
            raise ResolutionError(f"origin remote does not match the registered repository for {selection}")

    branch = run_git(repository_path, "branch", "--show-current") or "DETACHED"
    commit = run_git(repository_path, "rev-parse", "HEAD")
    porcelain = run_git(repository_path, "status", "--porcelain=v1", "--untracked-files=normal")
    return {
        "selection": selection,
        "workspace_id": workspace_id,
        "domain": domain,
        "repository_path": str(expected_root),
        "git_root": str(actual_root),
        "remote_identity": sanitized_remote(remote),
        "branch": branch,
        "commit": commit,
        "dirty": bool(porcelain),
    }


def _configured_root(workspace_root: Path, local_entry: dict[str, str] | None) -> Path | None:
    if local_entry is None:
        return None
    return workspace_path(workspace_root, local_entry["root"])


def _list_git_root(
    workspace_root: Path,
    profile: dict[str, str],
    local_entry: dict[str, str] | None,
) -> list[dict[str, object]]:
    source_root = _configured_root(workspace_root, local_entry)
    return [{
        "selection": profile["id"],
        "domain": profile["domain"],
        "resolver": profile["resolver"],
        "root_configured": source_root is not None,
        "checkout_present": source_root.is_dir() if source_root else False,
    }]


def _resolve_git_root(
    workspace_root: Path,
    profile: dict[str, str],
    local_entry: dict[str, str] | None,
    selection: str,
) -> dict[str, object]:
    if selection != profile["id"]:
        raise ResolutionError(f"single-repository workspace does not accept a repository suffix: {profile['id']}")
    source_root = _configured_root(workspace_root, local_entry)
    if source_root is None:
        raise ResolutionError(f"local root is not configured for source workspace profile: {profile['id']}")
    return inspect_git_root(
        source_root,
        selection=selection,
        workspace_id=profile["id"],
        domain=profile["domain"],
        expected_remote=profile.get("expected_remote"),
    )


def _list_path_remote_manifest(
    workspace_root: Path,
    profile: dict[str, str],
    local_entry: dict[str, str] | None,
) -> list[dict[str, object]]:
    source_root = _configured_root(workspace_root, local_entry)
    if source_root is None or not source_root.is_dir():
        return [{
            "selection": f"{profile['id']}:<repository-path>",
            "domain": profile["domain"],
            "resolver": profile["resolver"],
            "root_configured": source_root is not None,
            "checkout_present": False,
        }]

    results: list[dict[str, object]] = []
    for entry in read_path_remote_manifest(source_root, profile["manifest"]):
        repository_path = catalog_repository_path(source_root, entry["relative_path"])
        results.append({
            "selection": f"{profile['id']}:{entry['relative_path']}",
            "domain": profile["domain"],
            "resolver": profile["resolver"],
            "root_configured": True,
            "checkout_present": repository_path.is_dir(),
        })
    return results


def _resolve_path_remote_manifest(
    workspace_root: Path,
    profile: dict[str, str],
    local_entry: dict[str, str] | None,
    selection: str,
) -> dict[str, object]:
    prefix = f"{profile['id']}:"
    if not selection.startswith(prefix) or not selection[len(prefix):]:
        raise ResolutionError(f"select a catalog repository as {profile['id']}:<relative-repository-path>")
    source_root = _configured_root(workspace_root, local_entry)
    if source_root is None:
        raise ResolutionError(f"local root is not configured for source workspace profile: {profile['id']}")

    relative_path = selection[len(prefix):]
    entries = read_path_remote_manifest(source_root, profile["manifest"])
    matches = [entry for entry in entries if entry["relative_path"] == relative_path]
    if len(matches) != 1:
        raise ResolutionError(f"manifest selection is absent or ambiguous: {selection}")
    selected_path = catalog_repository_path(source_root, relative_path)
    return inspect_git_root(
        selected_path,
        selection=selection,
        workspace_id=profile["id"],
        domain=profile["domain"],
        expected_remote=matches[0]["remote"],
    )


RESOLVERS = {
    "git-root": {
        "list": _list_git_root,
        "resolve": _resolve_git_root,
    },
    "path-remote-manifest": {
        "list": _list_path_remote_manifest,
        "resolve": _resolve_path_remote_manifest,
    },
}
