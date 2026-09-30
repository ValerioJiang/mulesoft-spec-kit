# Extensions

Each directory here is a self-contained [Spec Kit extension](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md): an `extension.yml` manifest, the command prompts under `commands/`, and the templates, scripts and documents the commands rely on. The specify CLI copies the directory into a project at `.specify/extensions/<id>/` and generates one agent command per entry in `provides.commands` (for Claude Code: `.claude/skills/speckit-<id>-<cmd>/SKILL.md`).

| Extension | Purpose | Commands |
|---|---|---|
| [`technical-solution`](technical-solution/) | The central workspace itself: setup, initiative orchestration, cross-domain review, shared templates, the application-repository resolver and the workspace seed files. Required by every other extension here. | `/speckit-technical-solution-setup`, `-run`, `-review` |
| [`mulesoft`](mulesoft/) | MuleSoft lifecycle stages for any Mule 4 / Anypoint repository: requirements, contracts, plan, tasks, implementation, QA, verification, change, PR, deploy, UAT, release. | 14 × `/speckit-mulesoft-<stage>` |
| [`salesforce`](salesforce/) | Salesforce design stages for any Salesforce DX repository, with a read-only DX MCP gate. | 4 × `/speckit-salesforce-<stage>` |
| [`sf-workspace`](sf-workspace/) | Opt-in add-on: the 14 extended [SFSpeckit](https://github.com/ysumanth06/spec-kit-sf) stages (stories through UAT; vendored, MIT) on top of the `salesforce` design stages, with an execution gate for the deploy, login and test commands they contain. | 14 × `/speckit-sf-workspace-<stage>` |

The core commands (`/speckit-specify`, `/speckit-plan`, ...) are adapted to the central workspace by the [`central-workspace` preset](../presets/central-workspace/), and the whole set is described by the [`central-workspace` bundle](../bundles/central-workspace/).

## Installing

From an initialised Spec Kit project (or when creating one):

```bash
# into an existing project: the preset first, it is required
specify preset add --dev /path/to/this-repo/presets/central-workspace
specify extension add --dev /path/to/this-repo/extensions/technical-solution
specify extension add --dev /path/to/this-repo/extensions/mulesoft
specify extension add --dev /path/to/this-repo/extensions/salesforce
specify extension add --dev /path/to/this-repo/extensions/sf-workspace   # optional add-on

# or in one go while creating the workspace
specify init my-workspace --integration claude --script sh \
  --preset /path/to/this-repo/presets/central-workspace \
  --extension /path/to/this-repo/extensions/technical-solution \
  --extension /path/to/this-repo/extensions/mulesoft \
  --extension /path/to/this-repo/extensions/salesforce
```

`scripts/bash/create-workspace.sh` (or `scripts/powershell/create-workspace.ps1`) runs these steps, verifies the result and seeds `.gitignore`; `--with-sf-workspace` adds the add-on and `--update` refreshes an existing workspace. `catalog.json` in this directory is the extension catalog. Once the four catalogs of this repository are registered in a project (see [bundles](../bundles/README.md)), the default set installs with `specify bundle install central-workspace` and the add-on with `specify extension add sf-workspace`.

## Conventions shared by all extensions here

- Artifacts always live in the workspace under `initiatives/<id>/<domain>/`; never in an application repository.
- Command bodies reference installed files with full `.specify/extensions/<id>/...` paths.
- Application repositories are resolved only through the shared resolver CLI declared in `spec-kit-workspace.json`.
- Tests, deployments, tickets, PR/MR creation and publications happen only on a direct user request; there are no automatic hooks.
- No organisation-specific rule is baked in; organisation conventions go into optional profiles under `.specify/profiles/`.
