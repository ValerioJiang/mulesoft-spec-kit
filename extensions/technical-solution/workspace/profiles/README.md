# Optional profiles

A profile collects the conventions of a specific organisation or project (tracker, branch policy, quality gates, release sequences, documentation language) that the generic lifecycle must not assume. The backbone, the domain adapters and the skills stay agnostic; a profile applies only when `initiative.yml` lists it in `selected_profiles` and the initiative owner confirms that its rules hold.

- One file per profile: `<organisation>-<domain>.md` (for example `acme-salesforce.md`).
- Every rule states its provenance and status (`confirmed` or `to be confirmed`); a rule inherited from a previous context does not become policy by inference.
- No credentials, org aliases, local paths or business records: only conventions verifiable in the selected repository or with the owners.
- The profile does not replace the project's official policies, ADRs, pipelines or approvals: when they diverge, the official source prevails and the divergence is an open decision.

`example-salesforce.md` shows the expected structure with placeholders.
