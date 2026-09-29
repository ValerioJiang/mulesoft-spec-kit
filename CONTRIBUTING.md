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
4. Run the resolver: `python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py list` (after copying `spec-kit-workspace.local.json.template` to `spec-kit-workspace.local.json`).
5. If you changed a manifest, run `python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>` on it.

## Conventions

- **Command files** (`extensions/*/commands/*.md`, `presets/*/commands/*.md`) use frontmatter `description` and `argument-hint`, a `## User Input` block with `$ARGUMENTS`, then the instructions. They must be self-contained: the CLI generates the agent command from them and nothing else.
- **Paths in command bodies** are written in full (`.specify/extensions/<id>/templates/x.md`). A bare `templates/`, `scripts/`, `docs/` or `memory/` token at the start of a path is rewritten by the CLI at install time, so avoid it unless you rely on that rewrite.
- **Templates provided by an extension** live at `templates/<name>.md` and are declared in `provides.templates`, so `specify preset resolve <name>` can find them and presets can override them.
- **No organisation-specific content.** Tracker names, branch rules, environment names, remotes, hosts and quality gates belong in an optional profile, never in a command or template.
- **English only** for prompts, templates and documentation. Evidence labels are `SOLUTION_DESIGN`, `REPOSITORY`, `LIVE_MCP`, `TEST_RESULT`, `DEPLOYMENT_RESULT`, `INFERENCE`, `OPEN_DECISION` and `NOT_EXECUTED`.
- **Vendored files** under `extensions/sf-workspace/prompts/`, `templates/` and `docs/` come unchanged from [spec-kit-sf](https://github.com/ysumanth06/spec-kit-sf); adapt behaviour in `WORKSPACE-CONTRACT.md` and the wrapper commands instead of editing them.
- **Versions.** Bump the `version` in the manifest you change and add a line to `CHANGELOG.md`.

## Submitting

Open a pull request with the scratch-workspace check you ran (which commands you regenerated and read). Keep prompt changes small and explain the behaviour they change.
