---
description: Prepare or record business UAT for a MuleSoft initiative.
argument-hint: <initiative-id> [tester]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Generate UAT scenarios from approved acceptance criteria and existing contract/flow behavior. Save scripts under central `mulesoft/verification/`; use synthetic examples and omit secrets or real customer payloads. Record business execution only from results supplied by the named tester. Do not contact testers, change ticket status or deploy as a side effect.
