# Organisation profiles

The toolkit assumes nothing about your organisation: no tracker, branch policy, quality gate, environment name, deploy sequence or documentation language is built into a command or template. Those conventions live in **profiles**, Markdown files under `.specify/profiles/` in the workspace, and a profile applies only when an initiative lists it in `selected_profiles` in its `initiative.yml` and the initiative owner confirms that its rules apply.

`/speckit-technical-solution-setup` seeds `.specify/profiles/README.md` and `.specify/profiles/example-salesforce.md`. The example shows the expected shape: provenance, status, activation rule, then sections for architecture and data, testing and quality, tracker/branches/review, release, and documentation language, each with bracketed placeholders.

## Writing a profile

- One file per organisation and domain: `<organisation>-<domain>.md` (for example `acme-salesforce.md`, `acme-mulesoft.md`).
- Every rule states its provenance and its status (`confirmed` or `to be confirmed`). A rule inherited from an older context does not become policy by inference.
- No credentials, org aliases, machine-local paths or business records. Only conventions that can be verified in the selected repository or with its owners.
- The profile never replaces the project's official policies, ADRs, pipelines or approvals. Where they diverge, the official source wins and the divergence is recorded as an open decision.

## How commands use it

Domain adapters (`.specify/extensions/salesforce/lifecycle.md`, `.specify/extensions/mulesoft/lifecycle.md`) instruct the agent to apply a profile only when the initiative selects it and otherwise to detect conventions from the selected repository. Migrating an existing overlay or constitution into a profile is described in [existing repositories](existing-repositories.md).
