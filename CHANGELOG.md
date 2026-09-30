# Changelog

All notable changes to this repository are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.1] - 2026-09-30

Components: `technical-solution` 3.1.1, `mulesoft` 2.0.3, `salesforce` 2.0.3, `sf-workspace` 2.1.2 (unchanged), preset `central-workspace` 1.1.1, bundle `central-workspace` 1.1.2, workflow `technical-solution` 2.1.1.

### Changed

- The plan template speaks MuleSoft and Salesforce: its technical context and source layout examples are a Mule 4 application and a Salesforce DX project instead of a generic web and mobile project, and the constitution gate comes before the research it gates.
- `spec-kit-workspace.json`: `workflow_contract` now points at the workflow contract document that every command reads; the workflow definition it used to point at is `workflow_definition`.
- Stage paragraphs name their files relative to the initiative root (`salesforce/plan.md`, `common/review.md`), which `artifact_layout` decides, instead of spelling out `initiatives/<id>/`.
- The quickstart documents installing the released versions from the published catalogs, without a checkout.

### Fixed

- The workflow's `stage` input had no default although its prompt promised the full cycle; with no stage given, the first word of the request was read as the stage.
- `/speckit-review` resolved an application repository even for a review of initiative artifacts, which needs none, and did not say where the review goes. It now writes `review.md` under the selected scope and appends to an existing one; `/speckit-technical-solution-review` appends too.
- A core command called without a domain now has a stated scope (`common`).
- `/speckit-technical-solution-setup` seeds `.specify-dev/` in `.gitignore`, like the bootstrap scripts.
- The resolver reads Git's output as UTF-8 instead of the console code page.
- The plugin guide no longer names the example workspace submodule after this toolkit.

## [0.2.0] - 2026-09-30

Components: `technical-solution` 3.1.0, `mulesoft` 2.0.2, `salesforce` 2.0.2, `sf-workspace` 2.1.2, preset `central-workspace` 1.1.0, bundle `central-workspace` 1.1.1, workflow `technical-solution` 2.1.0 (unchanged).

### Added

- `/speckit-checklist` and `/speckit-taskstoissues` are now provided by the preset instead of the Spec Kit core, whose versions expect the single-repository `specs/<feature>/` layout. The checklist is written to `<initiative>/<scope>/checklists/<focus>.md` from the workspace's own requirement IDs, and its template is adapted to initiatives. Issues are created only on a direct request that names the tracker, in a target resolved for the application repository, never in the central workspace's own remote; created issues are recorded in `tasks.md`. `/speckit-constitution` is the only core command left as it is.
- A vocabulary in `docs/concepts/central-workspace.md` and, in short form, in the workflow contract.
- Issue forms and a pull request template.

### Changed

- One name per thing. *Application repository* replaces "source repository", "source repo" and "target repository" everywhere; *source workspace* is kept for what it is, a registered root from which application repositories are resolved, and selections are written `<source-workspace-id>` and `<source-workspace-id>:<relative-repository-path>` instead of `<workspace-id>`. `check-consistency.py` rejects the retired terms.
- **Resolver output:** the key `workspace_id` is now `source_workspace_id`. It held the source workspace ID and collided with the top-level `workspace_id` of `spec-kit-workspace.json`, which names the central workspace.
- The workspace constitution template starts at version 1.0.0 with placeholders for its dates, and `/speckit-technical-solution-setup` fills them with the day the workspace adopts it. It used to ship the version and ratification date of the project this toolkit came from. Setup no longer treats any bracketed token as a sign of the Spec Kit default; the title is the test.
- The Claude Code plugin's version follows the `technical-solution` extension that ships it (now 3.1.0, was an unrelated 0.2.0); `check-consistency.py` keeps the two equal.
- The constitution says *orchestrator* where it said *router*, like every other document.

## [0.1.1] - 2026-09-30

Components: `technical-solution` 3.0.1, `mulesoft` 2.0.1, `salesforce` 2.0.1, `sf-workspace` 2.1.1, preset `central-workspace` 1.0.1, bundle `central-workspace` 1.1.0, workflow `technical-solution` 2.1.0 (unchanged).

### Changed

- Renamed to MuleSoft Spec Kit. The repository is now https://github.com/ValerioJiang/mulesoft-spec-kit (the previous name redirects), the Claude Code plugin is `mulesoft-spec-kit` (`/mulesoft-spec-kit:run`), and the README credits GitHub Spec Kit and SFSpeckit. Catalog registration commands documented with the `--install-allowed` policy the CLI requires. The archives attached to `v0.1.0` were already built from the renamed tree while the `v0.1.0` tag points at the commit before the rename; from this release on the tag is created on the commit the archives are built from.
- The `central-workspace` bundle no longer installs `sf-workspace`. The add-on is opt-in on every path: `--with-sf-workspace` with the scripts, `specify extension add sf-workspace` from the catalog.
- `sf-workspace` installs only the 14 vendored prompts that have a command and the 4 templates they use; the 5 design-stage and constitution prompts and their templates stay in the repository for reference (`.extensionignore`). The descriptions of `setup`, `stories` and `deploy` no longer promise an installer, a named tracker or a fixed environment chain, which the workspace contract forbids.
- One description per command: the manifests now carry the text of the command files' frontmatter (the text the agent sees), and `docs/reference/commands.md` follows them.
- The orchestrator accepts `converge` and the domain-specific stages (MuleSoft `qa`, `pr`, `change`) and says which command handles a stage a domain extension does not provide. The workflow contract states that a domain command takes precedence over the core command for that domain, and that `Ready` needs both tasks and analyze (the quickstart now runs analyze).
- Initiative *state* and document *status* are separate vocabularies: the workflow contract defines the document statuses the templates use (`Draft`, `WIP`, `WIP — BLOCKED`, `Ready for review`, `Approved`), and templates label them `Status`.
- The seed `spec-kit-workspace.json` carries `workspace_id: central-workspace` and `setup` replaces it with the workspace's own name.
- `build-release-assets.py` writes to `dist/<tag>/`, honours `.extensionignore` and stops when the catalogs name an archive it did not build.

### Fixed

- `scripts/bash/create-workspace.sh` is executable in Git. Every CI run had failed on `Permission denied`, as did the README's own command on Linux and macOS.
- `create-workspace --update` left the generated extension commands as symlinks into the CLI's dev cache (`specify extension add --dev` always links), which Git checks out as text files where symlinks are unsupported. Both scripts now turn them back into regular files and ignore `.specify-dev/`.
- `create-workspace.sh`: `--help` as the first argument ran `mkdir -p --help`; `--update` on a missing directory created it before refusing; options are now accepted before the target. `create-workspace.ps1`: defaults to `-Script sh` like the bash script and the documentation (it defaulted to `ps`), and no longer creates the target before refusing it.
- The resolver failed with "unsupported format" on a repository whose `origin` is a filesystem path, even with `--root`. Such a repository now resolves with `remote_identity: null`; a filesystem path registered as the expected remote is reported as such.
- The smoke workflow's bare-path check could never fail (`! grep` under `bash -e`).
- References to things that do not exist: the README inside `claude-marketplace/` (now shipped), the "domain constitution" in `/speckit-mulesoft-implement`, `templates/` as the vendored template folder in `AGENTS.md` and `CONTRIBUTING.md`. `/speckit-mulesoft-review` names its output file and `/speckit-mulesoft-pr` appends to it instead of replacing it.
- Documentation that contradicted behaviour: the CLI does not check `requires.tools`; the workspace constitution is installed by `specify init`, not by `setup`; `setup` may replace an untouched default constitution.
- The tasks template no longer tells the agent to write failing tests first, commit after each task, deploy a demo or validate a `quickstart.md`, all of which the commands forbid or the layout lacks. Header lines of five templates no longer run together.
- A client programme name left in the README's upgrade note.

### Added

- `scripts/python/check-consistency.py`: fails when manifests, command files, catalogs, the bundle and the command reference disagree, when a command mention names no command, or when a bash script is not executable in Git. Run in CI.
- `tests/`: unit tests of the resolver, run in CI.
- CI installs the Spec Kit CLI at the revision pinned by `upstream/spec-kit`, runs with read-only permissions and checks that an updated workspace contains no symlinks.
- The README defines *initiative* and states that the project is not affiliated with Salesforce or GitHub. The three Spec Kit core commands the preset does not override (`constitution`, `checklist`, `taskstoissues`) are documented.

## [0.1.0] - 2026-09-30

### Changed

- Restructured as a Spec Kit toolkit (`extensions/`, `presets/`, `workflows/`, `bundles/`, `docs/`, `scripts/`) in the style of [github/spec-kit](https://github.com/github/spec-kit). The repository is no longer a pre-initialised workspace: workspaces are created with the `specify` CLI, and agent commands are generated from `commands/*.md` at install time.
- Removed every organisation-specific name, remote, profile and rule. Organisation conventions are now optional profiles seeded by `/speckit-technical-solution-setup`.
- Translated all documentation, templates, constitution and command prompts to English.
- The extension formerly installed as `sf` is now `sf-workspace`; its commands are `/speckit-sf-workspace-<stage>` and the vendored SFSpeckit prompts live under `prompts/`.
- The source-repository resolver now discovers the workspace root by walking up to `spec-kit-workspace.json` and is shipped by the `technical-solution` extension.

### Fixed (adversarial review of the restructure)

- `sf-workspace` is now an opt-in add-on with the 14 extended stages only; its `specify`, `clarify`, `plan`, `review` and `constitution` wrappers were removed because they overwrote the artifacts of the `salesforce` extension and the workspace constitution. Its vendored templates moved to `sf-templates/` so they no longer shadow core and workspace templates by name, `requires.tools` (sf, gh) is declared again, every wrapper carries an execution gate for the deploy, login and test commands in the prompts, and upstream's changelog is no longer installed.
- The `salesforce` adapter no longer requires `sf-workspace`; the extended stages read it only when installed and extend its artifacts instead of replacing them.
- The preset is documented and checked as mandatory (`run` and `setup` stop without it); the preset's plan and tasks templates describe the workspace layout instead of `specs/[###-feature]/` and `research.md`; `/speckit-specify` writes `common/initiative.md`, the name every template and manifest already used.
- Domain commands honour `artifact_layout` from `spec-kit-workspace.json` instead of hard-coding `initiatives/<id>/`; the orchestrator now owns `initiative.yml.state`, derives filesystem-safe IDs and refuses to edit a dirty repository without confirmation.
- `create-workspace.sh` refuses to run inside the toolkit or on an existing workspace (use `--update`), verifies every component (the CLI returns 0 on failed installs), seeds `.gitignore`, defaults to `--script sh` (the PowerShell resolver needs `python3`, absent on Windows), makes `sf-workspace` opt-in, and has a PowerShell twin. The resolver reports a missing `git` executable cleanly. Docs say `python3` on Linux/macOS and `python` on Windows.
- The workflow takes an `integration` input (default `auto`) instead of being pinned to Claude; preset, workflow and bundle catalogs were added next to the extension catalog with the publishing steps the bundle needs; `.gitattributes` normalises line endings; a smoke workflow for CI creates a workspace and checks the generated commands.

### Added

- `speckit.technical-solution.setup`: creates the workspace files without overwriting anything.
- `presets/central-workspace`: core `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement` and `converge` overrides plus `review`, `verify` and `release`, and the workspace-aware plan, tasks, checklist and constitution templates.
- `bundles/central-workspace`, `extensions/catalog.json` and `scripts/bash/create-workspace.sh`.
- Repository published at https://github.com/ValerioJiang/mulesoft-spec-kit; manifests carry the `repository` URL, the catalogs are served from `main` and point at the `v0.1.0` release assets built by `scripts/python/build-release-assets.py`.
- MIT license.

[Unreleased]: https://github.com/ValerioJiang/mulesoft-spec-kit/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/ValerioJiang/mulesoft-spec-kit/releases/tag/v0.2.1
[0.2.0]: https://github.com/ValerioJiang/mulesoft-spec-kit/releases/tag/v0.2.0
[0.1.1]: https://github.com/ValerioJiang/mulesoft-spec-kit/releases/tag/v0.1.1
[0.1.0]: https://github.com/ValerioJiang/mulesoft-spec-kit/releases/tag/v0.1.0

## Earlier history

The lineage before this release (a client-specific central workspace mounted as a submodule of a programme repository) is preserved in the Git history.
