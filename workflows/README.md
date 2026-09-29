# Workflows

[Workflows](https://github.com/github/spec-kit/blob/main/workflows/README.md) are resumable multi-step pipelines that the specify CLI runs through the installed agent integration.

| Workflow | Steps |
|---|---|
| [`technical-solution`](technical-solution/workflow.yml) | Runs `speckit.technical-solution.run` for the requested stage (or the full design-to-verification cycle), then pauses at a review gate. The gate does not authorise external actions or record business or architecture approval. |

Install into a workspace with `specify workflow add --dev /path/to/this-repo/workflows/technical-solution`, then run it with `specify workflow run technical-solution`.
