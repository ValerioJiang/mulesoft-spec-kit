---
description: Draft a MuleSoft technical plan for the selected initiative.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Apply the MuleSoft domain adapter and `.specify/extensions/mulesoft/templates/mulesoft-plan-template.md`; write contract drafts with `.specify/extensions/mulesoft/templates/mulesoft-contract-template.md`. Ground app scope and versions in repository/live evidence. Keep drafts unpublished and do not run app, test, deployment or Anypoint write commands.
