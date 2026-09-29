# sf-workspace extension

An adapter that runs the SFSpeckit Salesforce lifecycle inside a central Spec Kit workspace. The 19 stage prompts are vendored unchanged from [spec-kit-sf](https://github.com/ysumanth06/spec-kit-sf) 2.0.0 by Sumanth Yanamala (MIT, see `LICENSE`; upstream docs at <https://ysumanth06.github.io/spec-kit-sf/>) under `prompts/`, with the upstream templates under `templates/` and the scoring rubric at `docs/scoring.md`. Each command here wraps one upstream prompt with the workspace contract in `WORKSPACE-CONTRACT.md`, which overrides the prompt's paths, repository layout, configuration, aliases, targets, installation steps and action assumptions.

Compared with the sibling `salesforce` extension, which covers design only (specify, clarify, plan, review), this extension provides the full 19-stage lifecycle from setup through release notes. Artifacts go to `initiatives/<id>/salesforce/` and `initiatives/<id>/common/`; the Salesforce repository is resolved through the workspace's shared source CLI and is never written to under its own `.specify/`.

## Commands

| Command | What it does |
|---|---|
| `/speckit-sf-workspace-setup` | Check the required tools (sf, gh, code-analyzer); install only on explicit request. |
| `/speckit-sf-workspace-constitution` | Establish Salesforce project principles with 9 articles and environmental discovery. |
| `/speckit-sf-workspace-specify` | Create a Salesforce feature spec with object maps and security model. |
| `/speckit-sf-workspace-clarify` | Analyze the specification for gaps and edge cases with stakeholder sign-off. |
| `/speckit-sf-workspace-plan` | Create a technical plan with package structure and blast radius analysis. |
| `/speckit-sf-workspace-stories` | Generate tracker-ready developer stories with security matrices. |
| `/speckit-sf-workspace-analyze` | Pre-implementation analysis with mother story context and org drift detection. |
| `/speckit-sf-workspace-implement` | Implement a story file with auto-heal loop and scoring gates. |
| `/speckit-sf-workspace-review` | TPO and Architect review of generated stories before ticket creation. |
| `/speckit-sf-workspace-change` | Impact analysis for mid-sprint requirement changes. |
| `/speckit-sf-workspace-qa` | Generate manual test scripts and run automated Apex/Jest tests. |
| `/speckit-sf-workspace-pr` | Prepare a PR with scoring gates and code review checklist. |
| `/speckit-sf-workspace-verify` | Generate formal Verification Evidence documents with coverage metrics. |
| `/speckit-sf-workspace-deploy` | Promote Salesforce code to an explicitly named target environment. |
| `/speckit-sf-workspace-score` | 555-point quality scoring dashboard across all stories in a feature. |
| `/speckit-sf-workspace-hotfix` | Emergency production bug fix workflow with fast-track deployment. |
| `/speckit-sf-workspace-regression` | Full feature regression before release. |
| `/speckit-sf-workspace-release-notes` | Business-ready delivery summary from completed stories. |
| `/speckit-sf-workspace-uat` | Generate UAT scripts and manage business sign-offs. |

## Notes

- Upstream prompts invoke siblings as `/speckit.sf.<x>`; here the equivalent is `/speckit-sf-workspace-<x>`.
- Do not install this extension alongside the catalog `sf` extension in the same workspace; both target the same lifecycle.
- The scoring rubric in `docs/scoring.md` is advisory unless the selected project explicitly adopts its gates.
- Branch policy, tracker, Git host, org aliases, environments, analyzers and release gates come from the user or the selected repository, never from upstream sample values.
