---
description: Prepare a MuleSoft release record from approved, observed evidence.
argument-hint: <initiative-id> [target]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/mulesoft/`) and cross-domain artifacts under its `common/` folder. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Use `.specify/extensions/technical-solution/templates/release-template.md` to summarize selected applications, repository revisions, contracts, approvals, test results and deployment evidence. Keep unexecuted gates explicit. Do not publish, deploy, create a release ticket or announce a release unless directly requested. Deployment and UAT acceptance are distinct states.
