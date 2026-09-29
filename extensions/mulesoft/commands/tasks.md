---
description: Decompose the selected MuleSoft plan into traceable app, contract, test, and release tasks.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Read the central workflow contract, initiative common artifacts and MuleSoft plan. Create or update `initiatives/<id>/mulesoft/tasks.md` using the resolved `tasks-template` (run `specify preset resolve tasks-template`). Map each task to a requirement or integration ID, selected application/repository, exact discovered relative path, dependency, and verification evidence. Include implementation and MUnit/contract-verification tasks required by the plan. Do not create Jira issues. Do not infer all candidate apps are in scope.
