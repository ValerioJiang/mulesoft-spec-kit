---
description: Generate a requirements-quality checklist for an initiative scope without judging the implementation.
argument-hint: <initiative-id> [common|salesforce|mulesoft|domain] <focus>
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

A checklist here is a unit test for the writing of requirements: every item asks whether the requirements are complete, clear, consistent, measurable and cover the scenarios. It never tests whether the implementation works.

1. Select the scope: `common` when no domain is given, otherwise the domain folder. Read only what the focus needs from that scope: `common/initiative.md` or `<domain>/spec.md`, then `plan.md`, `tasks.md`, `common/integration-matrix.md` and `common/decisions.md` when they exist. If the specification of the scope is missing, stop and name the stage that produces it.
2. Take the focus from the user input (for example `security`, `api-contract`, `data-model`, `release`). If it is missing or too broad to act on, ask at most three questions about focus, depth and audience; never ask for what the user already said.
3. Write `<initiative-root>/<scope>/checklists/<focus>.md` using the resolved `checklist-template` (run `specify preset resolve checklist-template`; this preset overrides it). If the file exists, append to it and continue its `CHK` numbering; never delete or rewrite existing items and never change a checkbox.
4. Phrase every item as a question about what is written, tag its quality dimension and point at its evidence, for example `Is the retry policy of INT-002 defined together with its idempotency key? [Completeness, common/integration-matrix.md INT-002]`. Refer to the IDs of the workspace (`REQ-`, `<DOM>-REQ-`, `INT-`, `ADR-`, `Q-`) or to a section, and mark what is absent or doubtful with `[Gap]`, `[Ambiguity]`, `[Conflict]` or `[Assumption]`. At least four items in five carry a reference or a marker. For a domain scope, include the cross-domain view: is every shared integration ID described the same way in the common matrix and in this domain?
5. Do not write items that start with verify, test, confirm or check followed by system behaviour, and no test cases, code or tool details: those belong to the verify/QA stage.
6. Leave every new item unchecked. Marking `[x]` is the reviewer's decision that the requirement-quality criterion is met; it is not implementation progress and it does not change the initiative state.

Report the file path, the number of items added, whether the file was created or extended, and the gaps that most affect readiness. Do not edit the specification, plan or tasks from this stage, and do not resolve or inspect an application repository.
