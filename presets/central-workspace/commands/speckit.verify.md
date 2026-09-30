---
description: Verify completed implementation against initiative requirements and record exact evidence.
argument-hint: <initiative-id> <domain> [task-ids]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Resolve the selected application repository with the shared CLI at `source_resolution.entrypoint`, using an exact source workspace selection or explicit root. Verify its Git root, then use the selected domain's verification procedure and `.specify/extensions/technical-solution/templates/verification-template.md`. Do not parse the local registry or catalog manifests in this command. Run only checks relevant to approved requirements and the chosen application repository. Record the commit, target, exact command/tool, exit result and evidence. Keep local tests, live checks, deployment and business acceptance separate. Do not claim an unexecuted check.
