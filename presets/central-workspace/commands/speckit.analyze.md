---
description: Analyze selected scope and implementation tasks against application repositories and shared contracts.
argument-hint: <initiative-id> [domain]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Compare specification, plan and tasks for conflicts, missing dependencies, contract mismatch and scope gaps. If repository evidence is needed, use the shared resolver CLI from `source_resolution.entrypoint` with an exact source workspace selection or explicit root. Record only its verified Git root, branch, commit and dirty state; do not parse the local registry or catalog manifests in this command. Inspect only task-relevant files. Write findings to the selected initiative's `analyze.md`; don't modify application code or run tests in this analysis stage.
