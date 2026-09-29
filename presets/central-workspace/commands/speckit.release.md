---
description: Prepare or execute an explicitly requested release stage using a named target and verified evidence.
argument-hint: <initiative-id> <domain> [target]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Prepare a central release record from approved review, verification and release gates, using `.specify/extensions/technical-solution/templates/release-template.md`. If the user directly requests deployment, use the selected domain's deploy procedure and require the application and target to be explicit. Never infer an environment, publish an API contract, create a release ticket or announce a release as a side effect. Record deployment and UAT acceptance as separate evidence.
