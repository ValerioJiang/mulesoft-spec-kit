# Contributing

Thanks for helping. This repository is a set of Spec Kit building blocks, so most contributions are prompt, template or documentation changes, and the test is always the same: create a workspace and check what the `specify` CLI generates.

## Prerequisites

- The Spec Kit CLI (`specify`) 1.0 or later on your PATH.
- Python 3.11 or later (the resolver scripts and the quick checks below use it).
- A coding agent for manual checks (Claude Code is the reference integration; others work through the same command files).

## Validate a change

1. Create a scratch workspace from your checkout:

   ```bash
   scripts/bash/create-workspace.sh /tmp/ws-test --integration claude
   ```

2. In the scratch workspace, confirm that everything installed and that the generated commands look right:

   ```bash
   specify extension list
   specify preset list
   specify workflow list
   ls .claude/skills            # one speckit-* directory per command
   ```

3. Read the generated file for the command you changed (for example `.claude/skills/speckit-mulesoft-plan/SKILL.md`). Every path in it must resolve inside the workspace: `.specify/extensions/<id>/...`, `initiatives/<id>/...`, `spec-kit-workspace.json`.
4. Run the resolver: `python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py list` (`python` instead of `python3` on Windows; after copying `spec-kit-workspace.local.json.template` to `spec-kit-workspace.local.json`).
5. Run `python scripts/python/check-consistency.py` (needs PyYAML). It parses every manifest and catalog and fails when a description, version, command count or asset name differs between a manifest, a command file, a catalog and `docs/reference/commands.md`.
6. If you changed the resolver, run `python -m unittest discover -s tests`.

Run `specify` commands only inside the scratch workspace, never with the toolkit checkout as the working directory: the CLI writes a `.specify/` cache wherever it runs, and the toolkit must not contain one.

## Conventions

- **Command files** (`extensions/*/commands/*.md`, `presets/*/commands/*.md`) use frontmatter `description` and `argument-hint`, a `## User Input` block with `$ARGUMENTS`, then the instructions. They must be self-contained: the CLI generates the agent command from them and nothing else.
- **Paths in command bodies** are written in full (`.specify/extensions/<id>/templates/x.md`). A bare `templates/`, `scripts/`, `docs/` or `memory/` token at the start of a path is rewritten by the CLI at install time, so avoid it unless you rely on that rewrite.
- **Templates provided by an extension** live at `templates/<name>.md` and are declared in `provides.templates`, so `specify preset resolve <name>` can find them and presets can override them.
- **No organisation-specific content.** Tracker names, branch rules, environment names, remotes, hosts and quality gates belong in an optional profile, never in a command or template.
- **English only** for prompts, templates and documentation. Evidence labels are `SOLUTION_DESIGN`, `REPOSITORY`, `LIVE_MCP`, `TEST_RESULT`, `DEPLOYMENT_RESULT`, `INFERENCE`, `OPEN_DECISION` and `NOT_EXECUTED`.
- **Vendored files** under `extensions/sf-workspace/prompts/`, `sf-templates/` and `docs/` come unchanged from [spec-kit-sf](https://github.com/ysumanth06/spec-kit-sf); adapt behaviour in `WORKSPACE-CONTRACT.md` and the wrapper commands instead of editing them.
- **One name per thing.** *Application repository* for a Git repository with application code, *source workspace* for a registered root the resolver resolves them from; the full vocabulary is in [docs/concepts/central-workspace.md](docs/concepts/central-workspace.md). `check-consistency.py` rejects the retired synonyms.
- **Versions.** Bump the `version` in the manifest you change, in its catalog entry (with the `download_url`) and in the bundle if it pins the component, and add a line to `CHANGELOG.md`.

## Submitting

Open a pull request with the scratch-workspace check you ran (which commands you regenerated and read). Keep prompt changes small and explain the behaviour they change.
