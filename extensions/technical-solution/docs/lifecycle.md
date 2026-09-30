# Full lifecycle

Spec Kit artifacts live in the central workspace. Application code stays in a source repository selected per initiative. The workflow has no fixed dependency on a parent workspace, a named application directory, a particular Salesforce package layout, or a particular MuleSoft repository.

## One directory contract

```text
initiatives/<initiative-id>/
├── README.md
├── initiative.yml             # portable IDs, selected domains, source revisions
├── common/                    # shared requirements, contracts, decisions, review
├── salesforce/                # Salesforce specification through release evidence
├── mulesoft/                  # MuleSoft specification through release evidence
└── <other-domain>/            # future domain adapters follow the same contract
```

Only create domain directories for confirmed scope. Never put generated artifacts in an application repository's `.specify/` directory. `initiative.yml` records repository identity and revision, not a machine-local path or credentials. `artifact_layout` in `spec-kit-workspace.json` may relocate the root shown above; every command reads it and treats `initiatives/<initiative-id>/` as the default only. Initiative IDs are filesystem-safe: letters, digits, `.`, `_` and `-`; the orchestrator derives them from the business key and title.

## Stages

| Stage | Common | Salesforce | MuleSoft |
|---|---|---|---|
| Specify | User needs, shared requirements, integrations | CRM requirements and data/security constraints | App/layer scope, APIs and integration requirements |
| Clarify | Cross-domain gaps and decisions | Org metadata and Salesforce-specific gaps | Contract ownership, runtime and Anypoint evidence gaps |
| Plan | Architecture, boundaries, decisions | Metadata, Apex/Flow/LWC, dependencies and migration | API-led boundaries, contracts, mappings, errors and operations |
| Tasks | Ordered work and traceability | Story/task breakdown compatible with the selected repo's process | App/contract/MUnit and deployment work breakdown |
| Analyze | Scope and dependency consistency | Target repo and org impact within the selected scope | Target apps, Exchange contracts and runtime dependencies |
| Implement | Cross-domain changes when needed | Changes only in the configured Salesforce source repo | Changes only in configured MuleSoft source repo(s) |
| Verify / QA | Traceability and evidence review | Tests, code analysis, metadata and persona evidence | MUnit, contract, static and runtime evidence |
| Review / PR | Cross-domain consistency and approvals | Repository-native review request | Repository-native review request |
| Deploy / UAT / Release | Release record and cross-domain state | Salesforce target selected by user and project policy | Anypoint target selected by user and deployment policy |

Stages can be invoked separately. The orchestrator may run the next read/write stage only when the current stage's prerequisites are met. Tests, remote writes, PR/MR creation, deployments, tracker changes and Anypoint/Salesforce mutations require a direct user request for that action; they are never automatic hooks.

## Source repository selection

Register source workspace roots in the ignored root `spec-kit-workspace.local.json`. Resolve them through the CLI declared by `source_resolution.entrypoint` in `spec-kit-workspace.json`: use an exact workspace ID for a single-repository root, or `<workspace-id>:<relative-repository-path>` for a repository selected from a catalog. The resolver owns config parsing, format adapters, path containment and Git-root checks; skills do not parse catalogs or search the filesystem. Relative roots resolve from the central workspace; absolute roots are allowed only in the ignored local config. Record repository identity and commit SHA in the initiative, never the machine-local path. Discover package directories and application layout only after the resolver returns the selected Git root.

Design stages require no source repository. Implementation and execution stages stop if the relevant source root, clean/dirty status, branch, commit, target environment, or required permissions are not known. Do not clone or modify application repositories unless the user explicitly requests it.

## Evidence and lifecycle state

Keep source claims distinct: `SOLUTION_DESIGN`, `REPOSITORY`, `LIVE_MCP`, `TEST_RESULT`, `DEPLOYMENT_RESULT`, `INFERENCE`, `OPEN_DECISION`, `NOT_EXECUTED`. Record tool, repository revision, target, date and exact artifact path for evidence. A planned test is not a test result; a successful local test is not a deployment; a deployment is not business acceptance.

States are monotonic only by evidence: `Draft` → `Clarifying` → `Planned` → `Ready` → `Implementing` → `Implemented` → `Verified` → `Released`. Any missing blocking prerequisite sets `Blocked` with its owner and evidence needed. An approval state is recorded only when the named approver explicitly approves.
