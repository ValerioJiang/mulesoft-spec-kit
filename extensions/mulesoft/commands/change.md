---
description: Assess a requested change against the current MuleSoft initiative baseline.
argument-hint: <initiative-id> <change-request>
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Compare the new request with central common requirements, integration decisions, MuleSoft spec/plan/tasks and current repository revision. Record impact on apps, API contracts, compatibility, tests, rollout and cross-domain IDs before editing baseline artifacts. Preserve prior decisions and approvals; append an impact note. Do not implement or publish the change unless separately requested.
