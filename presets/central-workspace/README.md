# Central Workspace

A preset that makes the core Spec Kit commands work in a central, multi-repository workspace — artifacts live under `initiatives/<id>/<domain>/` instead of `specs/NNN-feature/`, and application code stays in source repositories selected per initiative.

## When to Use

Use it in a workspace created for the `technical-solution` extension from this repository. The preset requires that extension: its commands read `spec-kit-workspace.json`, the workflow contract and the templates that the extension installs. The preset must be installed in every workspace that uses the `technical-solution`, `mulesoft`, `salesforce` or `sf-workspace` extensions: their commands route to `/speckit-review`, `/speckit-verify` and `/speckit-release` and expect the workspace-aware core commands, and without the preset the core `/speckit-specify`, `/speckit-plan` and `/speckit-tasks` write to `specs/` instead of `initiatives/<id>/<domain>/`.

## Commands Included

| Command | Output | Description |
|---------|--------|-------------|
| `/speckit-specify` | `common/initiative.md` or `<domain>/spec.md` | Create or refine traceable initiative requirements under the selected domain |
| `/speckit-clarify` | `clarification-report.md` | Record focused questions with impact, owner and evidence needed |
| `/speckit-plan` | `plan.md` | Produce an implementation-ready technical plan for the selected domain |
| `/speckit-tasks` | `tasks.md` | Build a traceable task or story breakdown from the approved plan |
| `/speckit-analyze` | `analyze.md` | Check spec, plan and tasks for conflicts, gaps and contract mismatch |
| `/speckit-implement` | *(code)* + `implementation-log.md` | Implement explicitly selected tasks in the resolved source repository |
| `/speckit-converge` | `tasks.md` | Append a convergence phase for remaining gaps without rewriting approved work |
| `/speckit-review` | review record | Review artifacts or an application diff against approved scope and evidence |
| `/speckit-verify` | `verification/` | Run only the relevant checks and record exact evidence |
| `/speckit-release` | `release.md` | Prepare a release record; deploy only on an explicit request with a named target |

## What It Replaces

The preset replaces the core `speckit.specify`, `speckit.clarify`, `speckit.plan`, `speckit.tasks`, `speckit.analyze`, `speckit.implement` and `speckit.converge` commands with central-workspace versions, and adds `speckit.review`, `speckit.verify` and `speckit.release`. It also overrides the `plan-template`, `tasks-template`, `checklist-template` and `constitution-template` templates with workspace-aware ones; commands resolve them by name, so the override is picked up through the normal template stack.

## Installation

```bash
# From an existing workspace
specify preset add --dev ./presets/central-workspace

# Or while creating the workspace
specify init my-workspace --integration claude --preset /path/to/presets/central-workspace
```

The preset is stackable with priority like any other preset: `specify preset set-priority central-workspace <n>` orders it against other installed presets, and `specify preset resolve speckit.specify` shows which command wins.

## License

MIT
