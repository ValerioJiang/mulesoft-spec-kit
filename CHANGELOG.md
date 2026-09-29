# Changelog

All notable changes to this repository are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased] - 2026-09-29

### Changed

- Restructured as a Spec Kit toolkit (`extensions/`, `presets/`, `workflows/`, `bundles/`, `docs/`, `scripts/`) in the style of [github/spec-kit](https://github.com/github/spec-kit). The repository is no longer a pre-initialised workspace: workspaces are created with the `specify` CLI, and agent commands are generated from `commands/*.md` at install time.
- Removed every organisation-specific name, remote, profile and rule. Organisation conventions are now optional profiles seeded by `/speckit-technical-solution-setup`.
- Translated all documentation, templates, constitution and command prompts to English.
- The extension formerly installed as `sf` is now `sf-workspace`; its commands are `/speckit-sf-workspace-<stage>` and the vendored SFSpeckit prompts live under `prompts/`.
- The source-repository resolver now discovers the workspace root by walking up to `spec-kit-workspace.json` and is shipped by the `technical-solution` extension.

### Added

- `speckit.technical-solution.setup`: creates the workspace files without overwriting anything.
- `presets/central-workspace`: core `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement` and `converge` overrides plus `review`, `verify` and `release`, and the workspace-aware plan, tasks, checklist and constitution templates.
- `bundles/central-workspace`, `extensions/catalog.json` and `scripts/bash/create-workspace.sh`.
- MIT license.

## Earlier history

The lineage before this release (a client-specific central workspace mounted as a submodule of a programme repository) is preserved in the Git history.
