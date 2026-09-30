# MuleSoft extension

`mulesoft` adds the MuleSoft lifecycle stages to a central Spec Kit workspace: specify, clarify, plan, review, tasks, analyze, implement, qa, verify, change, pr, deploy, uat and release. Each stage writes its artifacts under `initiatives/<id>/mulesoft/` and reads the shared intent, integration matrix and decisions from `initiatives/<id>/common/`.

The extension works with any Mule 4 / Anypoint Platform repository layout. It assumes no runtime version, API-led layer, application inventory, Anypoint organisation, environment or deployment target: all of that is discovered from the repository the user selects for the initiative, after the shared resolver has verified its Git root.

## Requirements

- The `technical-solution` extension from this repository (workflow contract, common templates, source resolver).
- The `central-workspace` preset from this repository (core commands adapted to the central workspace).
- Spec Kit CLI `>=1.0.0`.

## Commands

| Command | Description |
|---|---|
| `/speckit-mulesoft-specify` | Produce MuleSoft requirements for the selected initiative using the shared common intent. |
| `/speckit-mulesoft-clarify` | Identify MuleSoft contract, app ownership, runtime and live-evidence gaps. |
| `/speckit-mulesoft-plan` | Draft a MuleSoft technical plan for the selected initiative. |
| `/speckit-mulesoft-review` | Review MuleSoft app scope, contract provenance and shared integration consistency. |
| `/speckit-mulesoft-tasks` | Decompose the selected MuleSoft plan into traceable app, contract, test, and release tasks. |
| `/speckit-mulesoft-analyze` | Check the selected MuleSoft scope, plan and tasks against the configured application repositories. |
| `/speckit-mulesoft-implement` | Implement explicitly selected MuleSoft tasks in the configured application repository. |
| `/speckit-mulesoft-qa` | Execute the MuleSoft verification cases selected in the approved initiative plan. |
| `/speckit-mulesoft-verify` | Summarize MuleSoft implementation evidence against requirements and tasks. |
| `/speckit-mulesoft-change` | Assess a requested change against the current MuleSoft initiative baseline. |
| `/speckit-mulesoft-pr` | Review MuleSoft changes and prepare repository-native review evidence. |
| `/speckit-mulesoft-deploy` | Deploy a MuleSoft application only to an explicitly requested target. |
| `/speckit-mulesoft-uat` | Prepare or record business UAT for a MuleSoft initiative. |
| `/speckit-mulesoft-release` | Prepare a MuleSoft release record from approved, observed evidence. |

## Artifacts and templates

Stages produce `spec.md`, `clarification-report.md`, `plan.md`, `contracts/`, `tasks.md`, `analyze.md`, `implementation-log.md`, `verification/`, `review.md` and `release.md` under `initiatives/<id>/mulesoft/`. The extension ships two templates, `templates/mulesoft-plan-template.md` and `templates/mulesoft-contract-template.md`; the common templates (domain spec, clarification report, tasks, implementation log, verification, release) come from the `technical-solution` extension and the `central-workspace` preset. Contract drafts stay `DRAFT — NOT PUBLISHED` until an owner records publication approval.

## External actions

Deployments, Exchange publication, Anypoint mutations, PR/MR creation and tickets happen only on a direct user request that names the target; no stage triggers them as a side effect. Live Exchange or Runtime Manager facts come from a connected read-only capability; when it is unavailable the evidence is recorded as `NOT_EXECUTED` and the dependent decision stays open. Local RAML/OAS files and Maven metadata are never a substitute for the live asset. The full adapter rules are in `lifecycle.md`.
