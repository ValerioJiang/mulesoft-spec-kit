---
description: Review MuleSoft changes and prepare repository-native review evidence.
argument-hint: <initiative-id> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under `initiatives/<id>/mulesoft/` and cross-domain artifacts under `initiatives/<id>/common/`. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Compare the selected diff with approved tasks, plan, tests and contract compatibility. Use only the review convention discovered in the chosen repository. Record findings and revision in central `mulesoft/review.md`. Creating a PR/MR, assigning reviewers or sending a notification requires a direct user request and an explicitly selected repository/target branch.
