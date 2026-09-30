---
description: Review initiative artifacts or an application diff against approved scope and evidence.
argument-hint: <initiative-id> [domain] [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Review requirements-to-plan-to-task traceability, test evidence, security, contracts and cross-domain integration IDs of the selected scope. A review of initiative artifacts alone needs no repository. When the review covers an application diff or needs repository evidence, resolve the selected application repository with the shared CLI at `source_resolution.entrypoint`, using an exact source workspace selection or explicit root, and review against its verified Git root. Do not parse the local registry or catalog manifests in this command. Report findings with file/section evidence and severity, and write them to `review.md` under the selected scope of the initiative, appending to an existing review instead of replacing it. Do not create a PR/MR, approve on behalf of an owner or change source files during review.
