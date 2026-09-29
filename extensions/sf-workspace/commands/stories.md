---
description: Generate Jira-ready developer stories with security matrices.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/sf-workspace/WORKSPACE-CONTRACT.md` and `.specify/extensions/technical-solution/docs/workflow-contract.md` first. Every Salesforce artifact stays under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/salesforce/`); shared artifacts under `initiatives/<id>/common/`. Artifacts already produced by the `salesforce` extension (`spec.md`, `clarification-report.md`, `plan.md`, `data-model.md`, `review.md`) are authoritative: read and extend them, never replace them. Resolve application code only from the explicitly selected Salesforce repository through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`. Never write `.specify/memory/constitution.md`.

## Execution gate

The vendored prompt contains concrete `sf`, `gh`, `npm` and deployment commands. Run any of them only if the user input explicitly requests that action and names its target (org alias, environment, repository or branch); otherwise report the exact command you would run and stop. Never log in to an org, install tools or plugins, create branches, tickets or pull requests, deploy, or roll back as a side effect of following the prompt.

## Stage

Follow the Salesforce-specific procedure in `.specify/extensions/sf-workspace/prompts/stories.md` for the user input. The workspace contract overrides every upstream path, repository, configuration, alias, target, installation and action assumption in that prompt. Where the prompt refers to the upstream scoring rubric (`scoring.md`), read `.specify/extensions/sf-workspace/docs/scoring.md`; where it refers to `.specify/templates/<name>.md`, use `.specify/extensions/sf-workspace/sf-templates/<name>.md`; where it invokes `/speckit.sf.specify`, `/speckit.sf.clarify`, `/speckit.sf.plan` or `/speckit.sf.review`, use the `salesforce` extension's `/speckit-salesforce-<stage>` instead; where it invokes any other `/speckit.sf.<other>`, the equivalent here is `/speckit-sf-workspace-<other>`.
