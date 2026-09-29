---
description: Draft Salesforce technical and data-model plans in the selected initiative.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/salesforce/lifecycle.md` before acting. Keep every Spec Kit artifact under `initiatives/<id>/salesforce/` and cross-domain artifacts under `initiatives/<id>/common/`. Resolve a Salesforce repository only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, using an exact workspace ID or explicit root, then discover package directories from its `sfdx-project.json`; never assume a fixed application directory, package names, org aliases, tracker projects, branch names or Git hosting, and never write into an application repository's `.specify/` directory.

## Stage

Apply the Salesforce domain adapter and use `.specify/extensions/salesforce/templates/salesforce-plan-template.md` and `.specify/extensions/salesforce/templates/salesforce-data-model-template.md` to write `initiatives/<id>/salesforce/plan.md` and `initiatives/<id>/salesforce/data-model.md`. For blast radius and org discovery, the read-only Salesforce DX MCP capability is mandatory; if it is unavailable, produce only the part supported by the Solution Design and the repository, declare the org analysis `NOT_EXECUTED` and keep the plan `WIP — BLOCKED`. Salesforce CLI, SOQL, Tooling API via another client and static inventories are not substitutes. Never run implementation, test, deployment or org mutation commands.
