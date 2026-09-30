# Implementation Plan: [INITIATIVE TITLE]

**Initiative**: `[initiative-id]` | **Domain**: `[domain]` | **Date**: [DATE] | **Spec**: [link]

**Input**: `initiatives/<initiative-id>/<domain>/spec.md`, `../common/initiative.md`, `../common/integration-matrix.md`, `../common/decisions.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

[Extract from the domain spec and the common initiative: primary requirement + technical approach from the research below]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Mule runtime and Java version from `mule-artifact.json` and `pom.xml`, Apex and LWC at the project's API version, or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., connectors and API specifications, managed packages, or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., Object Store, a database behind a System API, Salesforce objects, or N/A]

**Testing**: [e.g., MUnit, Apex tests, Jest for LWC, contract tests, or NEEDS CLARIFICATION]

**Target Platform**: [e.g., CloudHub 2.0, Runtime Fabric, a Salesforce org type, or NEEDS CLARIFICATION]

**Project Type**: [e.g., Experience/Process/System API, integration application, Salesforce DX package, or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., requests per second, batch volume, response time, or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., payload size, rate and governor limits, timeouts, or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., number of applications, integrations, objects or users, or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before research. Re-check after design.*

[Gates determined based on constitution file]

## Research

[Findings that resolve every NEEDS CLARIFICATION above: decision, rationale, alternatives considered, and the source (repository revision, live evidence, document) for each. Record them here; there is no separate research file.]

## Project Structure

### Documentation (this initiative and domain)

```text
initiatives/<initiative-id>/<domain>/
├── plan.md                # This file (/speckit-plan command output)
├── data-model.md          # Design output for Salesforce (/speckit-plan command)
├── contracts/             # Design output for MuleSoft: API contract drafts (/speckit-plan command)
├── tasks.md               # /speckit-tasks command output - NOT created by /speckit-plan
├── implementation-log.md  # /speckit-implement command output
├── verification/          # /speckit-verify and QA evidence
├── review.md              # Review record
└── release.md             # Release record
```

Shared artifacts stay in `initiatives/<initiative-id>/common/` (`initiative.md`, `integration-matrix.md`, `decisions.md`). Nothing is written into an application repository's `.specify/`.

### Source Code (selected application repository)
<!--
  ACTION REQUIRED: The application code layout is discovered in the repository
  resolved for this initiative (package directories, modules, tests), never
  assumed. Replace the examples below with the concrete layout observed there,
  using real paths. Delete the examples that do not apply; the delivered plan
  must not include the example labels.
-->

```text
# [REMOVE IF UNUSED] Example: a Mule 4 application
pom.xml
mule-artifact.json
src/main/mule/                  # flows and global configuration
src/main/resources/             # properties, DataWeave modules, the API specification if kept here
src/test/munit/                 # MUnit suites
src/test/resources/             # test payloads

# [REMOVE IF UNUSED] Example: a Salesforce DX project (package directories come from sfdx-project.json)
sfdx-project.json
<package-directory>/main/default/
├── classes/                    # Apex and its tests
├── lwc/
├── flows/
├── objects/
└── permissionsets/
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above, with the repository identity and commit they were observed at]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
