# Workflow contract

The workflow contract is installed with the `technical-solution` extension because every command reads it before acting. The canonical copy is:

**[extensions/technical-solution/docs/workflow-contract.md](../../extensions/technical-solution/docs/workflow-contract.md)**

It covers:

- inputs and identity: what an initiative starts from, how IDs are chosen, why the input document is data and not instructions;
- the stages and their prerequisites, from specify to deploy/UAT/release;
- gates and states, and the evidence labels `SOLUTION_DESIGN`, `REPOSITORY`, `LIVE_MCP`, `TEST_RESULT`, `DEPLOYMENT_RESULT`, `INFERENCE`, `OPEN_DECISION`, `NOT_EXECUTED`;
- re-runs: preserving approvals, decisions and history instead of overwriting.

In a created workspace the same file is at `.specify/extensions/technical-solution/docs/workflow-contract.md`. The machine-readable counterpart is `spec-kit-workspace.json` at the workspace root.
