---
description: Check the selected MuleSoft scope, plan and tasks against the configured application repositories.
argument-hint: <initiative-id> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For stages that touch an application repository, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact source workspace ID or `<source-workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Read the central workflow contract, initiative artifacts and the selected MuleSoft application repositories. Inspect only the apps and dependencies in scope. Record each repository's actual Git root, branch, commit and dirty state; inspect the relevant POM, Mule manifest, API source, dependencies and MUnit tests. Classify findings as confirmed repository facts, live evidence, inference or open decision and update central `mulesoft/analyze.md`. Do not edit source code, run tests or assume a runtime/Exchange state.
