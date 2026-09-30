# AGENTS.md

Guidance for coding agents working on this repository.

## What this repository is

A set of Spec Kit building blocks, not a project that uses Spec Kit. There is no `.specify/` directory and no `.claude/skills/` at the root: those are created by the `specify` CLI in the *workspaces* that people create from this repository. Do not add them here.

| Directory | Contents |
| --- | --- |
| `extensions/<id>/` | One Spec Kit extension each: `extension.yml`, `commands/`, `templates/`, plus docs, scripts and seed files the commands reference. |
| `presets/central-workspace/` | Overrides of the core commands and templates for the central workspace model. |
| `workflows/technical-solution/` | The workflow definition. |
| `bundles/central-workspace/` | The bundle manifest naming the full set. |
| `scripts/` | `bash/create-workspace.sh` and its PowerShell twin (the local bootstrap), `python/build-release-assets.py`, `python/check-consistency.py`. |
| `tests/` | Unit tests of the resolver. |
| `docs/` | Documentation. Canonical lifecycle and workflow contract live in `extensions/technical-solution/docs/` because they are installed with the extension; `docs/` links to them. |
| `upstream/` | Git submodules of github/spec-kit and spec-kit-sf. Reference only. Never edit. |

## Rules that keep the toolkit installable

- The `specify` CLI copies an extension directory to `.specify/extensions/<id>/` and generates one agent command per `provides.commands` entry from `commands/<cmd>.md`. There is no way to ship a pre-authored skill file, so command files must carry everything the agent needs.
- At install time the CLI rewrites a bare `templates/`, `scripts/`, `docs/` or `memory/` token at the start of a path in a command body to `.specify/extensions/<id>/<subdir>/` (only when that subdirectory exists in the extension). Write full paths and you never depend on that behaviour.
- Cross-extension references always use the installed path, for example `.specify/extensions/technical-solution/docs/workflow-contract.md`.
- Templates an extension ships are declared in `provides.templates` with `name` and `file: templates/<name>.md`; the preset overrides core templates by the same names.
- Keep `extension.yml`, `preset.yml`, `bundle.yml` and `workflow.yml` valid YAML and bump versions when behaviour changes. A command's description in the manifest, its frontmatter, the catalog entry and `docs/reference/commands.md` must agree, as must versions across manifests, catalogs and the bundle; `python scripts/python/check-consistency.py` checks all of it.
- Keep the resolver (`extensions/technical-solution/scripts/source_workspaces/`) free of platform-specific branches; new repository layouts are new adapters registered in `adapters.py`.

## Testing a change

Create a scratch workspace and read what the CLI generated:

```bash
scripts/bash/create-workspace.sh /tmp/ws-test --integration claude
cd /tmp/ws-test && specify extension list && ls .claude/skills
```

Then open the generated file for the command you touched and check every path resolves inside the workspace. Before committing, run `python scripts/python/check-consistency.py` and `python -m unittest discover -s tests`. See `CONTRIBUTING.md` for the full checklist.

## Content rules

English only. No organisation names, remotes, hosts, tracker keys, environment names or quality thresholds in prompts or templates; those go into optional profiles. Evidence labels and lifecycle states are fixed vocabularies (see `extensions/technical-solution/docs/workflow-contract.md`). Never edit the vendored files under `extensions/sf-workspace/prompts/`, `sf-templates/` and `docs/`.
