# Changelog

All notable changes to this repository are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased] - 2026-09-29

### Changed

- Restructured as a Spec Kit toolkit (`extensions/`, `presets/`, `workflows/`, `bundles/`, `docs/`, `scripts/`) in the style of [github/spec-kit](https://github.com/github/spec-kit). The repository is no longer a pre-initialised workspace: workspaces are created with the `specify` CLI, and agent commands are generated from `commands/*.md` at install time.
- Removed every organisation-specific name, remote, profile and rule. Organisation conventions are now optional profiles seeded by `/speckit-technical-solution-setup`.
- Translated all documentation, templates, constitution and command prompts to English.
- The extension formerly installed as `sf` is now `sf-workspace`; its commands are `/speckit-sf-workspace-<stage>` and the vendored SFSpeckit prompts live under `prompts/`.
- The source-repository resolver now discovers the workspace root by walking up to `spec-kit-workspace.json` and is shipped by the `technical-solution` extension.

### Fixed (adversarial review of the restructure)

- `sf-workspace` is now an opt-in add-on with the 14 extended stages only; its `specify`, `clarify`, `plan`, `review` and `constitution` wrappers were removed because they overwrote the artifacts of the `salesforce` extension and the workspace constitution. Its vendored templates moved to `sf-templates/` so they no longer shadow core and workspace templates by name, `requires.tools` (sf, gh) is declared again, every wrapper carries an execution gate for the deploy, login and test commands in the prompts, and upstream's changelog is no longer installed.
- The `salesforce` adapter no longer requires `sf-workspace`; the extended stages read it only when installed and extend its artifacts instead of replacing them.
- The preset is documented and checked as mandatory (`run` and `setup` stop without it); the preset's plan and tasks templates describe the workspace layout instead of `specs/[###-feature]/` and `research.md`; `/speckit-specify` writes `common/initiative.md`, the name every template and manifest already used.
- Domain commands honour `artifact_layout` from `spec-kit-workspace.json` instead of hard-coding `initiatives/<id>/`; the orchestrator now owns `initiative.yml.state`, derives filesystem-safe IDs and refuses to edit a dirty repository without confirmation.
- `create-workspace.sh` refuses to run inside the toolkit or on an existing workspace (use `--update`), verifies every component (the CLI returns 0 on failed installs), seeds `.gitignore`, defaults to `--script sh` (the PowerShell resolver needs `python3`, absent on Windows), makes `sf-workspace` opt-in, and has a PowerShell twin. The resolver reports a missing `git` executable cleanly. Docs say `python3` on Linux/macOS and `python` on Windows.
- The workflow takes an `integration` input (default `auto`) instead of being pinned to Claude; preset, workflow and bundle catalogs were added next to the extension catalog with the publishing steps the bundle needs; `.gitattributes` normalises line endings; a smoke workflow for CI creates a workspace and checks the generated commands.

### Added

- `speckit.technical-solution.setup`: creates the workspace files without overwriting anything.
- `presets/central-workspace`: core `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement` and `converge` overrides plus `review`, `verify` and `release`, and the workspace-aware plan, tasks, checklist and constitution templates.
- `bundles/central-workspace`, `extensions/catalog.json` and `scripts/bash/create-workspace.sh`.
- MIT license.

## Earlier history

The lineage before this release (a client-specific central workspace mounted as a submodule of a programme repository) is preserved in the Git history.
