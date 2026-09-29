---
description: Deploy a MuleSoft application only to an explicitly requested target.
argument-hint: <initiative-id> <application> <target>
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/mulesoft/lifecycle.md` before acting. Keep every Spec Kit artifact under `initiatives/<id>/mulesoft/` and cross-domain artifacts under `initiatives/<id>/common/`. For source-repository stages, resolve repositories only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, selecting an exact workspace ID or `<workspace-id>:<relative-repository-path>`; never parse the local registry or repository manifests in this command, and never rely on a parent workspace or an application repository's `.specify/` directory.

## Stage

Require a direct user request naming the application, source revision, target environment and deployment action. Read the selected repository's current release procedure, initiative approvals, verification evidence and deployment configuration. Show the concrete app/revision/target and preflight result before deployment. Run only the repository-defined deployment mechanism. Record command or tool, target, deployment ID, timestamp, outcome and post-deployment verification in central `release.md`. Never infer credentials or environment aliases, publish a draft API contract, or deploy because a plan says to deploy.
