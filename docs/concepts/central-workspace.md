# The central workspace

A central workspace is a Spec Kit project whose artifacts describe initiatives that span several application repositories. The workspace holds the specifications, plans, tasks, decisions and evidence; the application repositories are selected targets, never embedded dependencies and never output locations.

## Layers of a created workspace

| Layer | Location in the workspace | Responsibility |
| --- | --- | --- |
| Spec Kit core | `.specify/templates/`, `.specify/scripts/`, `.specify/memory/constitution.md` | Installed by `specify init`. The constitution is the workspace one, installed by `specify init` from the `central-workspace` preset. |
| Preset | `.specify/presets/central-workspace/` | Core commands (`/speckit-specify`, `-plan`, `-tasks`, ...) and core templates redirected to `initiatives/<id>/<domain>/`. |
| Orchestration | `.specify/extensions/technical-solution/` and the generated `/speckit-technical-solution-run` | Intake, single artifact path, routing per domain, stage gates and the completion report. |
| Common | `.specify/extensions/technical-solution/templates/` and `initiatives/<id>/common/` | Shared requirements, integration IDs, decisions and cross-domain review. |
| Salesforce | `.specify/extensions/salesforce/` (design stages) and optionally `.specify/extensions/sf-workspace/` (full SFSpeckit lifecycle) | Salesforce requirements and lifecycle; the upstream SFSpeckit prompts are adapted through a workspace contract. |
| MuleSoft | `.specify/extensions/mulesoft/` | MuleSoft requirements, contracts, tasks, implementation, tests, review and release. |
| Source registry | `spec-kit-workspace.json`, `spec-kit-workspace.local.json`, `.specify/extensions/technical-solution/scripts/source_workspaces/` | Versioned profiles by ID, domain and resolver; ignored local mapping from ID to checkout root. The resolver dispatches to registered adapters; commands never interpret repository formats themselves. |
| Output | `initiatives/<id>/{common,salesforce,mulesoft,<domain>}/` | Artifacts of the whole lifecycle, linked to sources, revisions and evidence. |

Every layer above the core is installed by the `specify` CLI from this repository, and the agent commands are generated from the extension and preset command files. Nothing is hand-copied into the workspace except through `/speckit-technical-solution-setup`, which seeds the root files.

## Boundaries

The workspace does not require an application repository to sit under a parent directory, to have a known name or to contain its own `.specify/`. Implementation and verification resolve repositories chosen per initiative and treat them according to their actual process and layout, discovered after resolution.

The Salesforce and MuleSoft adapters share the common requirement and integration IDs without flattening platform artifacts or responsibilities. A further domain is a further extension that follows the same contract: artifacts under `initiatives/<id>/<domain>/`, a `lifecycle.md` adapter document, commands that read the workflow contract first.

External actions are never automatic hooks. Tickets, merge or review requests, deployments, contract publication, org or Anypoint changes and communications require a direct request and a known target. Credential configurations stay in the native clients and do not enter the artifacts.

## Versioning

The building blocks carry their own versions in `extension.yml`, `preset.yml`, `workflow.yml` and `bundle.yml`; a workspace records the installed versions in `.specify/extensions/.registry` and its siblings. The two upstream repositories under `upstream/` in this toolkit are pinned to the commits reported by `git submodule status`; update them deliberately and review the vendored SFSpeckit prompts before changing a pin. The Spec Kit CLI version is checked through `requires.speckit_version` in each manifest.
