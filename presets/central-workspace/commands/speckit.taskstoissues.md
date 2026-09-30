---
description: Create tracker issues from the tasks of an initiative domain, only on a direct request that names the tracker.
argument-hint: <initiative-id> <domain> <tracker-and-project-or-repository> [task-ids]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `spec-kit-workspace.json` at the workspace root and `.specify/extensions/technical-solution/docs/workflow-contract.md` before acting. Resolve the initiative root from `artifact_layout.root`, replacing `{initiative_id}` with the initiative ID, and keep every artifact under it; domain scopes follow their adapter under `.specify/extensions/<domain>/lifecycle.md`. If `spec-kit-workspace.json` is missing, stop and tell the user to run `/speckit-technical-solution-setup`.

## Stage

Creating issues is an external write. Invoking this command with a named target is the direct request the workflow contract requires; a full-cycle request, or a plan that mentions a tracker, is not.

1. Read `<initiative-root>/<domain>/tasks.md`. If it is missing, stop and name the stage that produces it. Limit the work to the task IDs the user gave, otherwise to the unchecked tasks.
2. Establish the target from the user input: the tracker, and the project or repository that receives the issues. When the target is the issue tracker of an application repository, resolve that repository with the shared CLI at `source_resolution.entrypoint`, using an exact source workspace selection or explicit root, and use the remote identity it reports. Never derive the target from the central workspace's own remote, from another initiative or from a profile the initiative has not selected. If the target is missing or ambiguous, stop and ask only for it.
3. Use a capability for that tracker that is connected in the current session. If there is none, list the issues that would be created, mark the action `NOT_EXECUTED` and stop; do not substitute another tracker or tool.
4. Before creating anything, look up the existing issues of the target, open and closed, whose title carries the initiative ID together with one of the task IDs. Skip those tasks and report each one.
5. Create one issue per remaining task, titled `<initiative-id> <task-id>: <description>`, with the checkbox and the `[P]` and reference markers removed. In the body, give the requirement or integration IDs the task traces to, its dependencies and its planned verification, by ID and by path relative to the workspace. Do not copy source documents, customer data, credentials or machine-local paths. Apply labels, assignees or sprint fields only when the user asks for them or a selected profile defines them.
6. Record each created issue (task ID, issue reference, target, date) under an `## Issues` section at the end of `tasks.md`, appending without changing the tasks or their checkboxes.

Create issues only in the named target. Do not change, close or edit existing issues, do not create pull or merge requests, and do not notify anyone as a side effect. Report what was created, what was skipped as already present and what was not executed.
