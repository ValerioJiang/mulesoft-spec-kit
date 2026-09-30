# technical-solution

The extension that makes a Spec Kit project a *central workspace*: one repository that holds the specifications, plans, tasks and evidence of every initiative under `initiatives/<id>/`, while application code stays in the repositories it belongs to. Every other extension in this repository depends on it, and the [`central-workspace` preset](../../presets/central-workspace/) adapts the core `speckit` commands to it.

## Commands

| Command | Purpose |
| --- | --- |
| `/speckit-technical-solution-setup [--with-claude-plugin]` | Creates `spec-kit-workspace.json`, `spec-kit-workspace.local.json.template`, `initiatives/README.md` and `.specify/profiles/` if missing, installs the workspace constitution if the default one is untouched and dates its ratification, and optionally copies the Claude Code plugin for parent repositories. Never overwrites. |
| `/speckit-technical-solution-run <stage|full> <initiative-id-or-source> [domain] [repository]` | Starts or resumes an initiative: creates the initiative folder, determines the impacted domains, routes each stage to the core commands or the domain extensions, enforces the gates and reports evidence and blockers. |
| `/speckit-technical-solution-review <initiative-id>` | Reviews traceability, evidence and cross-domain consistency (shared integration IDs) of an initiative and writes `common/review.md`. |

## What it ships

- `docs/lifecycle.md` and `docs/workflow-contract.md`: the directory contract, stages, evidence labels and states every command follows. Installed at `.specify/extensions/technical-solution/docs/`.
- `templates/`: common initiative, domain specification, integration matrix, decision log, clarification report, initiative README, implementation log, verification and release templates, plus `initiative.yml.template`. Declared in `provides.templates`, so `specify preset resolve <name>` finds them and presets can override them.
- `scripts/source_workspaces/`: the resolver CLI (`cli.py list|resolve`) that turns a workspace ID or `<source-workspace-id>:<relative-repository-path>` into a verified Git root with remote identity, branch, commit and dirty state. Two adapters are registered: `git-root` (one repository per root) and `path-remote-manifest` (a catalog of nested repositories listed in a manifest file). New repository layouts are new adapters in `adapters.py`; commands never parse local configuration themselves.
- `workspace/`: the seed files that `setup` copies into a workspace (`spec-kit-workspace.json`, the local registry template, the initiatives README, the profile README and example, and the Claude Code marketplace plugin).

## Requirements

- Spec Kit CLI 1.0 or later; the project must be initialised with `specify init`.
- The `central-workspace` preset from this repository, so that `/speckit-specify`, `/speckit-plan`, `/speckit-tasks` and the other core commands write under `initiatives/<id>/<domain>/`.
- Python 3.11 or later for the resolver CLI.

## Install

```bash
specify extension add --dev /path/to/this-repo/extensions/technical-solution
specify preset add --dev /path/to/this-repo/presets/central-workspace
```

or create a whole workspace with `scripts/bash/create-workspace.sh`. Then run `/speckit-technical-solution-setup` in the workspace.
