---
description: Review requirements, implementation evidence and cross-domain consistency of an initiative.
argument-hint: <initiative-id>
---

## User Input

```text
$ARGUMENTS
```

## Stage

Read `spec-kit-workspace.json`, `.specify/extensions/technical-solution/docs/workflow-contract.md` and the selected initiative only; the initiative root is the one declared by `artifact_layout` (by default `initiatives/<id>/`). Review spec-to-plan-to-task traceability, application changes, test and live evidence, release gates, and every shared integration ID in `common/integration-matrix.md` against the plans of the domains involved. Keep review findings separate from approval; do not change source code or create external review requests. Write the review to `common/review.md` under the initiative root, appending to an existing review instead of replacing it, with file and section evidence and a severity for each finding.
