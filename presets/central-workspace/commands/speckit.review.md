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

Resolve the selected source with the shared CLI at `source_resolution.entrypoint`, using an exact workspace selection or explicit root. Use its verified Git root before reviewing requirements-to-plan-to-task traceability, source diff, test evidence, security, contracts and cross-domain integration IDs. Do not parse local config or source manifests in this command. Report findings with file/section evidence and severity. Write a review record centrally. Do not create a PR/MR, approve on behalf of an owner or change source files during review.
