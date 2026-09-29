# Integration matrix

IDs are stable within the initiative and must match across the documents of every domain involved.

| ID | Source → destination | Purpose/data | Contract and version | Sync/async | Limits | Security | Errors/retry/idempotency | Evidence/state |
|---|---|---|---|---|---|---|---|---|
| `INT-001` | [domain → domain/app] | [TBD] | [path or asset/version/TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [`SOLUTION_DESIGN`/`REPOSITORY`/`LIVE_MCP`/`INFERENCE`/`NOT_EXECUTED`] |

## Required consistency

- Call direction and responsibility are the same in the source and destination plans.
- Identifiers, names, versions and error models are consistent, or the divergence is an open decision.
- Retry and idempotency are defined together; do not assume a retry is safe.
- Limits and timeouts are explicit or marked `TBD`; no value is invented.
