# Example profile: Salesforce <organisation>

**Provenance**: [document, overlay or constitution the rules derive from; revision/date]  
**Status**: `to be confirmed for each initiative`  
**Activation**: only when the initiative lists `<organisation>-salesforce` in `selected_profiles` of `initiative.yml` and owner/project confirm that the rules apply.

This profile is not a prerequisite of the generic workflow and does not point to a specific repository, parent workspace or directory structure. The conventions below are references to verify in the selected repository and with the current owners; they do not replace official policies, ADRs, pipelines or approvals.

## Architecture and data

- [Declarative-vs-Apex preference and the criterion for justifying custom code]
- [Volumes and bulk thresholds to cover in tests; state whether still current policy]
- [Sharing, CRUD/FLS, access control; rules on credentials and reading records]
- [Metadata/service/UI layer separation adopted by the project]
- [Mandatory checks on objects/fields (for example data dictionary, permission matrix) and required capabilities; if absent, mark `NOT_EXECUTED`]

## Testing and quality

- [Required test patterns (positive/negative/bulk), test catalog, minimum coverage and where to detect them]
- [Pre-merge verification scripts (formatter, lint, unit tests, code analyzer) and external gates]
- [MCP capabilities or tools required by the gates and behaviour when not connected]
- The project's pipeline and quality gate remain authoritative: a local scoring or a static analysis does not replace them.

## Tracker, branches and review

- [Tracker and item hierarchy; rules for references in commits]
- [Base branches, prefixes, merge policy (PR/MR), protections, reviewers]
- [Existing design documents to reference instead of rewriting]
- Confirm tracker, branches, Git host and reviewers from the selected project before creating branches, commits or tickets. Do not perform these actions from a design stage.

## Release

- [Environments, who may deploy where, mandatory steps via pipeline, human gate for destructive changes]
- [Special deploy sequences (for example multi-step packages) and where they are documented]
- Discover packages and manifests from the selected project; do not fix paths or sequences from a previous context.
- Do not promote a state based only on test completion or a dry-run. Record approval, pipeline, deployment and post-verification as distinct evidence.

## Documentation and language

- [Language of functional/technical documentation and naming convention for files, metadata and code]
- Confirm the convention with the initiative owner before generating artifacts.
