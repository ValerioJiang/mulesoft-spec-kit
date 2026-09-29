# MuleSoft technical plan

**Initiative**: `[EPIC-KEY]-<slug>`<br>
**State**: `WIP`<br>
**Workspace/repository/revision**: [actual Git root, app and commit/branch]
**Exchange/Anypoint/Runtime Manager evidence**: [tool/capability/date or `NOT_EXECUTED`]

## Summary and boundary

[Describe the change per requirement; do not assume every candidate app must change.]

## Candidate apps and layers

| App | Declared layer | Observed current responsibility | Change required | Evidence |
|---|---|---|---|---|
| [TBD] | [Experience/Process/System/TBD] | [path and source] | [yes/no/TBD] | [repository/live/inference] |

## Contracts and provenance

| Integration ID | Contract | Format/version | Source of truth | Compatibility/ownership | State |
|---|---|---|---|---|---|
| `INT-001` | [path/Exchange app/TBD] | [RAML/OAS/AsyncAPI/TBD] | [repository/Exchange/TBD] | [TBD] | [evidence required] |

## Flow, mapping and behavior

- Direction and sync/async mode: [TBD]
- Mapping/transformations and semantics: [TBD]
- Payload/batch limits, throughput and timeouts: [source/TBD]
- Error mapping, retry and idempotency: [TBD]
- AuthN/AuthZ, secrets and classification: [TBD; do not report secret values]
- Correlation/trace ID, logging and audit: [TBD]

## Runtime and dependencies

| App | Mule runtime/Java/plugin/dependency | Evidence | Target/compatibility |
|---|---|---|---|
| [TBD] | [values] | [POM/mule-artifact/Anypoint and revision] | [only if verified] |

## Proposed verification

| Requirement/contract | Contract or MUnit scenario to design | Synthetic test data | Live outcome |
|---|---|---|---|
| `[MS]-REQ-001` | [scenario] | [yes/no] | `NOT_EXECUTED` |

No coverage threshold is introduced without a verified policy. This section describes proposed scenarios; it does not attest executed tests.

## Blockers and open decisions

| ID | Issue | Evidence needed | Owner | State |
|---|---|---|---|---|
| `MS-OPEN-001` | [TBD] | [repository/Exchange/Runtime Manager/owner] | [TBD] | `WIP` |
