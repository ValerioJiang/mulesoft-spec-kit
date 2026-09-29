# Presets

A [preset](https://github.com/github/spec-kit/blob/main/presets/README.md) is a stackable set of command and template overrides. Presets are installed into a project at `.specify/presets/<id>/` and resolved by priority above extensions and above the Spec Kit core.

| Preset | Purpose |
|---|---|
| [`central-workspace`](central-workspace/) | Replaces the core `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement` and `converge` commands with versions that write to `initiatives/<id>/<domain>/` and resolve application repositories through the workspace resolver; adds `review`, `verify` and `release`; overrides the plan, tasks, checklist and constitution templates. |

Install from a Spec Kit project with `specify preset add --dev /path/to/this-repo/presets/central-workspace`, or pass `--preset /path/to/this-repo/presets/central-workspace` to `specify init`.
