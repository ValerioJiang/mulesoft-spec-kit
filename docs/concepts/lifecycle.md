# Lifecycle

The lifecycle document is installed with the `technical-solution` extension because the commands read it at run time. The canonical copy is:

**[extensions/technical-solution/docs/lifecycle.md](../../extensions/technical-solution/docs/lifecycle.md)**

It defines:

- the one directory contract, `initiatives/<id>/{README.md, initiative.yml, common/, salesforce/, mulesoft/, <domain>/}`;
- what each stage (specify, clarify, plan, tasks, analyze, implement, verify/QA, review/PR, deploy/UAT/release) produces in `common/`, `salesforce/` and `mulesoft/`;
- how application repositories are selected and recorded (identity and commit, never a machine-local path);
- the evidence labels and the state machine `Draft → Clarifying → Planned → Ready → Implementing → Implemented → Verified → Released`, with `Blocked` naming the missing prerequisite.

In a created workspace the same file is at `.specify/extensions/technical-solution/docs/lifecycle.md`.
