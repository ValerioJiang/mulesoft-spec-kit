---
description: Summarize MuleSoft implementation evidence against requirements and tasks.
argument-hint: <initiative-id> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Compare actual code and test evidence with the initiative specification, plan and tasks. Run additional checks only when requested and when the target is explicit. Use `.specify/extensions/technical-solution/templates/verification-template.md`; record uncovered requirements, failed checks, unavailable live capabilities and residual risks. A local build/test does not prove Exchange publication, Runtime Manager state or release acceptance. Do not mark verified if required evidence is missing.
