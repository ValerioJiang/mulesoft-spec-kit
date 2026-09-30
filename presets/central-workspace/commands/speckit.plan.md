---
description: Produce an implementation-ready technical plan under the selected central initiative domain.
argument-hint: <initiative-id> [common|salesforce|mulesoft|domain]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Read the central specification, clarification report, decisions and domain adapter. Create/update `plan.md` under the selected scope of the initiative using the resolved `plan-template` (run `specify preset resolve plan-template`; this preset overrides it), with boundaries, architecture, data/API contracts, security, dependencies, rollout considerations and verification approach. Discover application layout only in a selected application repository. Mark unknowns and gates; don't turn suggestions into approved decisions.
