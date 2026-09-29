---
description: Check Salesforce plan traceability and consistency with common integration contracts.
argument-hint: <initiative-id> [details]
---

## User Input

```text
$ARGUMENTS
```

## Workspace contract

Read `.specify/extensions/technical-solution/docs/workflow-contract.md` and `.specify/extensions/salesforce/lifecycle.md` before acting. Keep every Spec Kit artifact under the initiative root declared by `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/salesforce/`) and cross-domain artifacts under its `common/` folder. Resolve a Salesforce repository only through the shared CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`, using an exact workspace ID or explicit root, then discover package directories from its `sfdx-project.json`; never assume a fixed application directory, package names, org aliases, tracker projects, branch names or Git hosting, and never write into an application repository's `.specify/` directory.

## Stage

Apply the Salesforce domain adapter. Review requirement traceability, object/security model, DX MCP evidence and every applicable common integration ID. Write the findings to `initiatives/<id>/salesforce/review.md`. Report remaining gaps; do not mark approval or implementation complete.
