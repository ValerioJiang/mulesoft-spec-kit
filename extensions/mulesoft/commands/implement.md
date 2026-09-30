---
description: Implement explicitly selected MuleSoft tasks in the configured application repository.
argument-hint: <initiative-id> <task-ids> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For stages that touch an application repository, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact source workspace ID or `<source-workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Read the central task list, approved plan, workspace constitution (`.specify/memory/constitution.md`) and initiative configuration. Confirm the invocation identifies the task(s), application repository and expected scope. Discover actual app paths and toolchain; check branch, commit and existing dirty changes before editing. Implement only the selected tasks and keep every Spec Kit artifact in the central initiative. Record changed files and decisions in `implementation-log.md`, using `.specify/extensions/technical-solution/templates/implementation-log-template.md`. Do not commit, push, create tickets or deploy unless each action is directly requested.
