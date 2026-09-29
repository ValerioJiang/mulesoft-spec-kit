---
description: Find and resolve missing initiative decisions without inventing answers.
argument-hint: <initiative-id> [domain]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Read the selected initiative's specification, common decisions and the relevant domain adapter. Record focused questions in `clarification-report.md` under the selected domain, using `.specify/extensions/technical-solution/templates/clarification-report-template.md`. For each question, state impact, owner and evidence needed. Answer only from a cited source or explicit user decision. Preserve unresolved questions and their effect on readiness.
