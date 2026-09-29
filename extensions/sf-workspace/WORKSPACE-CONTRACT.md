# SFSpeckit adapter contract for this workspace

The prompts under `.specify/extensions/sf-workspace/prompts/` are vendored unchanged from spec-kit-sf 2.0.0 (MIT, see the `LICENSE` file in this directory). They describe a Salesforce-specific lifecycle, but their original paths and project assumptions are not authoritative here. This adapter is the binding contract for every `/speckit-sf-workspace-*` skill. This extension is an opt-in add-on: it provides the extended stages only; the design stages (specify, clarify, plan, review) belong to the `salesforce` extension and its adapter `.specify/extensions/salesforce/lifecycle.md`, which every stage here reads first.

## Paths and context

- Require the initiative ID as input. Resolve the canonical artifact directory from `artifact_layout` in `spec-kit-workspace.json` (by default `initiatives/<id>/salesforce/`); shared artifacts live in `initiatives/<id>/common/`.
- Artifacts produced by the `salesforce` extension (`spec.md`, `clarification-report.md`, `plan.md`, `data-model.md`, `review.md`) are authoritative. Read and extend them; never replace them with the upstream document shapes. Story files, verification evidence, release notes and UAT scripts are added next to them.
- Translate every upstream `.specify/specs/<feature>/...` or `.specify/specs/...` artifact path to the relevant file in the central initiative directory. Never write Salesforce artifacts into the target repository.
- Use task/story identifiers from central `tasks.md` or the selected project's established tracker; don't allocate sequence numbers by scanning unrelated initiatives.
- For source inspection and code changes, resolve the Salesforce repository through the shared CLI declared by `spec-kit-workspace.json`, using an exact workspace ID or explicit root. Record the verified Git root, sanitized remote identity, branch, commit and dirty state returned by the resolver.
- Discover package directories and source paths from the selected repository's `sfdx-project.json`. Translate upstream `force-app/...` examples to the actual configured package directory. Do not assume a fixed application directory, a parent repository, package name or Salesforce structure.
- Read the root constitution and selected initiative profile, if any. Do not copy or read any configuration from a sibling repository.
- Never write `.specify/memory/constitution.md`: it is the workspace constitution owned by the `central-workspace` preset. If a project wants the nine SFSpeckit constitution articles, record them as an organisation profile in `.specify/profiles/<organisation>-salesforce.md` and select it in the initiative's `initiative.yml`; the upstream `constitution` stage has no command in this add-on.
- If an upstream prompt refers to `docs/scoring.md`, read `.specify/extensions/sf-workspace/docs/scoring.md`. A scoring rubric is advisory unless the selected project explicitly adopts its gates.
- If an upstream prompt refers to `.specify/templates/<name>.md`, use `.specify/extensions/sf-workspace/sf-templates/<name>.md`. These vendored templates are deliberately kept outside the resolver's `templates/` convention so they never shadow the workspace or core templates by name.
- The central workflow contract is `.specify/extensions/technical-solution/docs/workflow-contract.md`; read it before any stage.

## Command name mapping

Upstream prompts invoke sibling commands as `/speckit.sf.<x>`. In this workspace:

| Upstream | Here |
|---|---|
| `/speckit.sf.specify`, `/speckit.sf.clarify`, `/speckit.sf.plan`, `/speckit.sf.review` | `/speckit-salesforce-specify`, `-clarify`, `-plan`, `-review` (the `salesforce` extension) |
| `/speckit.sf.constitution` | no equivalent; record principles as an organisation profile (see above) |
| `/speckit.sf.setup`, `stories`, `analyze`, `implement`, `change`, `qa`, `pr`, `verify`, `deploy`, `score`, `hotfix`, `regression`, `release-notes`, `uat` | `/speckit-sf-workspace-<x>` |

Do not install this extension together with the catalog `sf` extension in the same workspace: both target the same lifecycle and their generated skills would compete for the same stages.

## Project-specific choices

The user or selected repository supplies branch policy, issue tracker, Git host, org alias, environments, test catalog, analyzers and release gates. Never use upstream sample values such as `dev`, `qa`, `prod`, `main`, `gh`, or fixed Salesforce paths as actual settings. Do not install dependencies or plugins unless the requested stage includes setup and the user asks to install them. The manifest declares `sf` (required) and `gh` (optional) so the CLI can warn when they are missing; nothing installs them automatically.

## Evidence and actions

Do not convert planned tests into passing results. Run tests and verification only in an explicitly requested QA/verify stage. The implement stage may create or update test code when a selected task requires it, but it does not execute tests. Record exact repository revision, target, command, exit status and report path for tests. A local test does not prove org state; a dry-run does not prove deployment; deployment does not prove UAT acceptance.

Create a branch, ticket, PR/MR, deploy, mutate an org or make another external write only when the user directly asks for that action. A deploy request does not authorize rollback; rollback requires its own direct request after the recovery change is reviewable. A generic request to complete the lifecycle authorizes internal stage work but does not authorize external publication or deployment. Before an external action, make the target and concrete changes reviewable; never infer a production target.

## Upstream command adaptation

Follow the applicable stage prompt under `.specify/extensions/sf-workspace/prompts/` for Salesforce-specific coverage. This contract takes precedence whenever that prompt mentions `.specify/specs/`, a fixed application path, repository root, provider, branch, alias, environment, automatic installation, rollback, external write or an assumed approval. The prompts contain concrete `sf`, `gh`, `npm` and deployment commands: execute one only when the user input explicitly requests that action and names its target; otherwise report the exact command you would run and stop. Do not execute a command copied from the prompt without first confirming that it is relevant to the selected repository and explicitly authorized.
