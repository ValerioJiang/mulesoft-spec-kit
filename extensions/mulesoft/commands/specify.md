---
description: Produce MuleSoft requirements for the selected initiative using the shared common intent.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Apply the MuleSoft domain adapter. Read common requirements and the integration matrix. Create/update only `mulesoft/spec.md`, using `.specify/extensions/technical-solution/templates/domain-spec-template.md`; identify candidate apps separately from confirmed changes and cite source evidence.
