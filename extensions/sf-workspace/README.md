# sf-workspace extension

An opt-in add-on that brings the extended SFSpeckit Salesforce lifecycle into a central Spec Kit workspace: stories, pre-implementation analysis, implementation, change impact, QA, PR preparation, verification evidence, deployment, scoring, hotfix, regression, release notes and UAT. Upstream's 19 stage prompts and 9 templates are vendored unchanged from [spec-kit-sf](https://github.com/ysumanth06/spec-kit-sf) 2.0.0 by Sumanth Yanamala (MIT, see `LICENSE`; upstream docs at <https://ysumanth06.github.io/spec-kit-sf/>) under `prompts/` and `sf-templates/`, with the scoring rubric at `docs/scoring.md`. A workspace receives the 14 prompts that have a command here and the 4 templates they use; the rest is kept for reference and listed in `.extensionignore`. Each command wraps one prompt with the workspace contract in `WORKSPACE-CONTRACT.md`, which overrides the prompt's paths, repository layout, configuration, aliases, targets, installation steps and action assumptions.

The design stages (specify, clarify, plan, review) are not provided here: they belong to the `salesforce` extension, whose artifacts this add-on reads and extends but never replaces. The upstream `constitution` stage has no command here either, because it would rewrite the workspace constitution; Salesforce principles are recorded as an organisation profile under `.specify/profiles/` instead.

## Requirements and install

- The `technical-solution` and `salesforce` extensions and the `central-workspace` preset from this repository.
- Salesforce CLI `sf` (required) and GitHub CLI `gh` (optional) are declared in the manifest and shown by `specify extension info sf-workspace`. The CLI neither checks nor installs them: make sure `sf` is on the PATH before a stage that needs it.

```bash
scripts/bash/create-workspace.sh <dir> --with-sf-workspace
# or, in an existing workspace
specify extension add --dev /path/to/this-repo/extensions/sf-workspace
```

Do not install this extension alongside the catalog `sf` extension in the same workspace; both target the same lifecycle.

## Commands

| Command | What it does |
|---|---|
| `/speckit-sf-workspace-setup` | Check the required tools (sf, gh, code-analyzer); install only on explicit request. |
| `/speckit-sf-workspace-stories` | Generate tracker-ready developer stories with security matrices. |
| `/speckit-sf-workspace-analyze` | Pre-implementation analysis with mother story context and org drift detection. |
| `/speckit-sf-workspace-implement` | Implement a story file with auto-heal loop and scoring gates. |
| `/speckit-sf-workspace-change` | Handle mid-sprint requirement changes with impact analysis. |
| `/speckit-sf-workspace-qa` | Generate manual test scripts and run automated Apex/Jest tests. |
| `/speckit-sf-workspace-pr` | Prepare a PR with scoring gates and code review checklist. |
| `/speckit-sf-workspace-verify` | Generate formal Verification Evidence documents with coverage metrics. |
| `/speckit-sf-workspace-deploy` | Promote Salesforce code to an explicitly named target environment. |
| `/speckit-sf-workspace-score` | 555-point quality scoring dashboard across all stories in a feature. |
| `/speckit-sf-workspace-hotfix` | Emergency production bug fix workflow with fast-track deployment. |
| `/speckit-sf-workspace-regression` | Run full regression tests across all stories in a feature. |
| `/speckit-sf-workspace-release-notes` | Auto-generate release notes from completed stories and test results. |
| `/speckit-sf-workspace-uat` | Generate UAT scripts and manage business sign-offs. |

## Execution gate

The vendored prompts contain concrete `sf`, `gh`, `npm` and deployment commands. Every wrapper instructs the agent to run one only when the user input explicitly requests that action and names its target; otherwise it reports the command it would run and stops. Logging in to an org, installing tools, creating branches, tickets or pull requests, deploying and rolling back never happen as side effects.

## Notes

- Upstream prompts invoke siblings as `/speckit.sf.<x>`; here the design stages map to `/speckit-salesforce-<x>` and the rest to `/speckit-sf-workspace-<x>` (see the contract's mapping table).
- The scoring rubric in `docs/scoring.md` is advisory unless the selected project explicitly adopts its gates.
- Branch policy, tracker, Git host, org aliases, environments, analyzers and release gates come from the user or the selected repository, never from upstream sample values.
- `sf-templates/` is deliberately not named `templates/`, so the vendored files never shadow workspace or core templates in the resolver.
