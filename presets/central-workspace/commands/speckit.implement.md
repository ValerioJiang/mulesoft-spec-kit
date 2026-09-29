---
description: Implement explicitly selected tasks in the application repository for a central initiative.
argument-hint: <initiative-id> <domain> <task-ids> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Read the initiative plan, approved tasks and selected domain lifecycle adapter. Resolve the source through the shared CLI at `source_resolution.entrypoint`, using an exact workspace selection or explicit root. Require exact task scope; use the verified Git root and inspect branch, commit, dirty state and toolchain before editing. Do not parse local config or source manifests in this command. Change only files needed for the selected task and keep Spec Kit artifacts central; record changed files and decisions in `implementation-log.md` using `.specify/extensions/technical-solution/templates/implementation-log-template.md`. Do not execute tests or verification checks from the implement stage; record planned checks for the explicit verify/QA stage. Do not create commits, tickets, PR/MR or deployments unless directly requested.
