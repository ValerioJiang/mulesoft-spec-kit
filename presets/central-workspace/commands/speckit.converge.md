---
description: Find remaining implementation gaps and append traceable work without rewriting approved artifacts.
argument-hint: <initiative-id> <domain>
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Compare current implementation with the initiative spec, plan, tasks and recorded verification. Bound inspection to the approved scope. If gaps remain, append a separately numbered convergence phase to central `tasks.md`; preserve all prior tasks and decisions. If complete, leave task files unchanged and report evidence. Do not fix source code in this stage.
