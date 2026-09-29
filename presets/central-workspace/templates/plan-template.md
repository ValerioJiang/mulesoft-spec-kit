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

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Research

[Findings that resolve every NEEDS CLARIFICATION above: decision, rationale, alternatives considered, and the source (repository revision, live evidence, document) for each. Record them here; there is no separate research file.]

## Constitution Check

*GATE: Must pass before research. Re-check after design.*

[Gates determined based on constitution file]

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
  assumed. Replace the placeholder tree below with the concrete layout observed
  there. Delete unused options and expand the chosen structure with real paths
  (e.g., apps/admin, packages/something). The delivered plan must not include
  Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above, with the repository identity and commit they were observed at]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
