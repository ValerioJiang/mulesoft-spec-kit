# Salesforce extension

Adds the Salesforce design stages to a central Spec Kit workspace: specify, clarify, plan (with a read-only Salesforce DX MCP gate) and review. It works with any Salesforce DX repository; package directories are discovered from the selected repository's `sfdx-project.json`, so no application layout, org alias, tracker or Git host is assumed.

The extension requires the `technical-solution` extension and the `central-workspace` preset from this repository. Every artifact it writes lives under `initiatives/<id>/salesforce/` in the workspace; shared requirements and decisions stay under `initiatives/<id>/common/`. Nothing is written into the application repository's `.specify/` directory.

## Commands

| Command | What it does |
|---|---|
| `/speckit-salesforce-specify` | Produce Salesforce CRM requirements from the shared common intent. |
| `/speckit-salesforce-clarify` | Identify missing Salesforce-specific requirements and org evidence. |
| `/speckit-salesforce-plan` | Draft the technical plan and data model; blocked (`WIP — BLOCKED`) without read-only DX MCP evidence. |
| `/speckit-salesforce-review` | Check plan traceability and consistency with the common integration contracts. |

The rules shared by all four stages are in `lifecycle.md`.

## Templates

- `templates/salesforce-plan-template.md` — technical plan.
- `templates/salesforce-data-model-template.md` — object, field, relationship and constraint model.

## Full lifecycle

These stages cover design only; they never implement, test, deploy or mutate an org. The extended lifecycle (stories through UAT: stories, analyze, implement, change, QA, PR, verify, deploy, score, hotfix, regression, release notes, UAT) is provided by the optional `sf-workspace` add-on (14 stages), an adapter of the upstream SFSpeckit prompts that requires this extension and extends its artifacts without replacing them.
