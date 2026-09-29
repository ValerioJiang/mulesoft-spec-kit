---
description: Build a traceable task or story breakdown from an approved initiative plan.
argument-hint: <initiative-id> [common|salesforce|mulesoft|domain]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Read `spec.md`, `plan.md`, clarifications and the selected repository's contribution workflow if available. Create `tasks.md` under the chosen initiative domain using the resolved `tasks-template` (run `specify preset resolve tasks-template`; this preset overrides it). Every task must trace to a requirement or decision, declare dependencies and identify its verification evidence. Use Salesforce stories only when the selected project's process requires them. Do not create external tracker issues.
