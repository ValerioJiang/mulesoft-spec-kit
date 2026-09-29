---
description: Implement a story file with auto-heal loop and scoring gates.
argument-hint: <initiative-id> <story-id> [repository-id-or-root]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/sf-workspace/WORKSPACE-CONTRACT.md` and `.specify/extensions/technical-solution/docs/workflow-contract.md` first. Every Salesforce artifact stays under `initiatives/<id>/salesforce/`; shared artifacts under `initiatives/<id>/common/`. Resolve application code only from the explicitly selected Salesforce repository through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`.

## Stage

Follow the Salesforce-specific procedure in `.specify/extensions/sf-workspace/prompts/implement.md` for the user input. The workspace contract overrides every upstream path, repository, configuration, alias, target, installation and action assumption in that prompt. Where the prompt refers to the upstream scoring rubric (`scoring.md`), read `.specify/extensions/sf-workspace/docs/scoring.md`; where it refers to `.specify/templates/<name>.md`, use `.specify/extensions/sf-workspace/templates/<name>.md`; where it invokes `/speckit.sf.<other>`, the equivalent command here is `/speckit-sf-workspace-<other>`.
