---
description: Produce Salesforce CRM requirements for the selected initiative using the shared common intent.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/salesforce/lifecycle.md` before acting. Keep every Spec Kit artifact under `initiatives/<id>/salesforce/` and cross-domain artifacts under `initiatives/<id>/common/`. Resolve a Salesforce repository only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, using an exact workspace ID or explicit root, then discover package directories from its `sfdx-project.json`; never assume a fixed application directory, package names, org aliases, tracker projects, branch names or Git hosting, and never write into an application repository's `.specify/` directory.

## Stage

Apply the Salesforce domain adapter. Read the common initiative and integration matrix first. Create/update only `initiatives/<id>/salesforce/spec.md` from the source Solution Design, using `.specify/extensions/technical-solution/templates/domain-spec-template.md`; preserve its intent and cite evidence. Do not create a branch or use an application repository's `.specify` paths.
