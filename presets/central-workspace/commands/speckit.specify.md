---
description: Create or refine traceable initiative requirements in the central Spec Kit workspace.
argument-hint: <initiative-id> [common|salesforce|mulesoft|domain] [source]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Read `.specify/extensions/technical-solution/templates/domain-spec-template.md` (or `.specify/extensions/technical-solution/templates/common-initiative-template.md` for `common/`). Write only `<initiative-root>/<domain>/spec.md`, defaulting to `common/` when no domain is selected. Preserve source references and separate requirements from assumptions. Domain scopes must follow their adapter under `.specify/extensions/`. Do not require or inspect an application repository unless a requirement needs technical evidence.
