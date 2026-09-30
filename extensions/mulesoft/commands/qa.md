---
description: Execute the MuleSoft verification cases selected in the approved initiative plan.
argument-hint: <initiative-id> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For stages that touch an application repository, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact source workspace ID or `<source-workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Read the approved plan, tasks and the selected application repository's configuration. Run only relevant project-defined build, MUnit, contract or static checks; preserve the repository's existing changes. For each run record app, repository commit, exact command, target/environment, exit result and evidence path in `verification/`. Keep planned, local, live and deployment checks separate. Do not deploy, publish contracts or mutate Anypoint as part of QA.
