---
description: Review MuleSoft app scope, contract provenance and shared integration consistency.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For stages that touch an application repository, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact source workspace ID or `<source-workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Apply the MuleSoft domain adapter. Check app ownership, layer, contract source/version, compatibility, request/response, limits, auth, errors/retry/idempotency, observability, target runtime and required live evidence. Reconcile every shared integration ID. Write the findings to central `mulesoft/review.md` and report remaining gaps without approving or publishing a contract.
