"""Tests for the application-repository resolver shipped by the technical-solution extension.

Run from the toolkit root: `python -m unittest discover -s tests`. Needs `git` on PATH; every
repository used here is created in a temporary directory.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[1]
EXTENSION = TOOLKIT / "extensions" / "technical-solution"
# The extension directory is copied into workspaces as it is: keep bytecode out of it.
sys.dont_write_bytecode = True
sys.path.insert(0, str(EXTENSION / "scripts" / "source_workspaces"))

from adapters import ResolutionError, remote_identity, sanitized_remote  # noqa: E402
from registry import list_sources, resolve_explicit_root, resolve_source  # noqa: E402


def make_repository(path: Path, remote: str | None = None) -> Path:
    path.mkdir(parents=True)
    git = ["git", "-C", str(path), "-c", "user.name=test", "-c", "user.email=test@example.com"]
    subprocess.run([*git, "init", "--quiet"], check=True)
    subprocess.run([*git, "commit", "--quiet", "--allow-empty", "-m", "init"], check=True)
    if remote:
        subprocess.run([*git, "remote", "add", "origin", remote], check=True)
    return path


class ResolverTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        self.workspace = base / "workspace"
        self.workspace.mkdir()
        shutil.copy(EXTENSION / "workspace" / "spec-kit-workspace.json", self.workspace)

        self.crm = make_repository(base / "crm", "https://user:token@git.example.com/org/crm-app.git")
        catalog = base / "mule"
        make_repository(catalog / "experience" / "orders-xapi", "git@git.example.com:org/orders-xapi.git")
        make_repository(catalog / "process" / "orders-papi", "https://git.example.com/org/other.git")
        (catalog / "repos.conf").write_text(
            "# relative path, remote\n"
            "experience/orders-xapi  https://git.example.com/org/orders-xapi.git\n"
            "process/orders-papi     https://git.example.com/org/orders-papi.git\n"
            "system/not-cloned       git@git.example.com:org/not-cloned.git\n",
            encoding="utf-8",
        )
        self.catalog = catalog
        self.write_local_registry(
            {"id": "salesforce-app", "root": "../crm"},
            {"id": "mulesoft-catalog", "root": str(catalog)},
        )

    def write_local_registry(self, *roots: dict[str, str]) -> None:
        (self.workspace / "spec-kit-workspace.local.json").write_text(
            json.dumps({"schema_version": 1, "workspace_roots": list(roots)}), encoding="utf-8"
        )

    def test_list_reports_every_selection_without_resolving(self) -> None:
        selections = {item["selection"]: item for item in list_sources(self.workspace)}
        self.assertEqual(
            set(selections),
            {
                "salesforce-app",
                "mulesoft-catalog:experience/orders-xapi",
                "mulesoft-catalog:process/orders-papi",
                "mulesoft-catalog:system/not-cloned",
            },
        )
        self.assertTrue(selections["salesforce-app"]["checkout_present"])
        self.assertFalse(selections["mulesoft-catalog:system/not-cloned"]["checkout_present"])
        self.assertEqual([item["domain"] for item in list_sources(self.workspace, domain="salesforce")], ["salesforce"])

    def test_missing_local_registry_names_the_template(self) -> None:
        (self.workspace / "spec-kit-workspace.local.json").unlink()
        with self.assertRaisesRegex(ResolutionError, "spec-kit-workspace.local.json.template"):
            list_sources(self.workspace)

    def test_single_repository_reports_identity_without_credentials(self) -> None:
        result = resolve_source("salesforce-app", self.workspace)
        self.assertEqual(result["remote_identity"], "git.example.com/org/crm-app")
        self.assertEqual(Path(str(result["git_root"])), self.crm)
        self.assertFalse(result["dirty"])
        self.assertEqual(len(str(result["commit"])), 40)
        (self.crm / "untracked.txt").write_text("change", encoding="utf-8")
        self.assertTrue(resolve_source("salesforce-app", self.workspace)["dirty"])

    def test_single_repository_rejects_a_repository_suffix(self) -> None:
        with self.assertRaisesRegex(ResolutionError, "does not accept a repository suffix"):
            resolve_source("salesforce-app:anything", self.workspace)

    def test_catalog_matches_https_manifest_entry_against_ssh_origin(self) -> None:
        result = resolve_source("mulesoft-catalog:experience/orders-xapi", self.workspace)
        self.assertEqual(result["remote_identity"], "git.example.com/org/orders-xapi")
        self.assertEqual(result["source_workspace_id"], "mulesoft-catalog")

    def test_catalog_rejects_wrong_remote_missing_checkout_and_traversal(self) -> None:
        with self.assertRaisesRegex(ResolutionError, "does not match the registered repository"):
            resolve_source("mulesoft-catalog:process/orders-papi", self.workspace)
        with self.assertRaisesRegex(ResolutionError, "does not exist"):
            resolve_source("mulesoft-catalog:system/not-cloned", self.workspace)
        with self.assertRaisesRegex(ResolutionError, "absent or ambiguous"):
            resolve_source("mulesoft-catalog:../crm", self.workspace)
        with self.assertRaisesRegex(ResolutionError, "select a catalog repository"):
            resolve_source("mulesoft-catalog", self.workspace)

    def test_manifest_rejects_paths_that_escape_the_catalog(self) -> None:
        (self.catalog / "repos.conf").write_text("../crm https://git.example.com/org/crm-app.git\n", encoding="utf-8")
        with self.assertRaisesRegex(ResolutionError, "must be relative and stay under"):
            list_sources(self.workspace)

    def test_unknown_profile_and_unknown_local_root_are_errors(self) -> None:
        with self.assertRaisesRegex(ResolutionError, "not registered"):
            resolve_source("nope", self.workspace)
        self.write_local_registry({"id": "nope", "root": "../crm"})
        with self.assertRaisesRegex(ResolutionError, "unknown source workspace profile"):
            list_sources(self.workspace)

    def test_explicit_root_needs_a_domain_and_the_git_root(self) -> None:
        with self.assertRaisesRegex(ResolutionError, "--domain is required"):
            resolve_explicit_root(str(self.crm), "", self.workspace)
        with self.assertRaises(ResolutionError):
            resolve_explicit_root(str(self.catalog), "mulesoft", self.workspace)
        result = resolve_explicit_root("../crm", "salesforce", self.workspace)
        self.assertEqual(result["selection"], "explicit-root")

    def test_local_path_remote_resolves_without_a_portable_identity(self) -> None:
        local = make_repository(self.workspace.parent / "local-remote", "../somewhere.git")
        result = resolve_explicit_root(str(local), "mulesoft", self.workspace)
        self.assertIsNone(result["remote_identity"])
        no_remote = make_repository(self.workspace.parent / "no-remote")
        self.assertIsNone(resolve_explicit_root(str(no_remote), "mulesoft", self.workspace)["remote_identity"])

    def test_manifest_with_a_local_path_remote_says_what_is_wrong(self) -> None:
        (self.catalog / "repos.conf").write_text("experience/orders-xapi /srv/git/orders-xapi.git\n", encoding="utf-8")
        with self.assertRaisesRegex(ResolutionError, "not a host-based URL"):
            resolve_source("mulesoft-catalog:experience/orders-xapi", self.workspace)


class RemoteIdentityTest(unittest.TestCase):
    def test_equivalent_forms_share_one_identity(self) -> None:
        expected = ("git.example.com", "org/app")
        for remote in (
            "https://git.example.com/org/app.git",
            "https://user:token@git.example.com/org/app",
            "ssh://git@git.example.com/org/app.git",
            "git@git.example.com:org/app.git",
            "GIT.example.com:org/app/",
        ):
            self.assertEqual(remote_identity(remote), expected, remote)

    def test_sanitized_remote_never_returns_a_local_path(self) -> None:
        for remote in (None, "", "/srv/git/app.git", "../app.git"):
            self.assertIsNone(sanitized_remote(remote), remote)


if __name__ == "__main__":
    unittest.main()
