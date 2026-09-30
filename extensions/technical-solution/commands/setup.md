---
description: Create the central workspace files (manifest, initiative registry, profiles) without overwriting anything.
argument-hint: [--with-claude-plugin]
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Prepare the current Spec Kit project as a central technical-solution workspace. This command only creates files that are missing. It never deletes or installs anything, and the only existing file it touches is the constitution: replaced when it is still the Spec Kit default, and dated when its ratification date is still a placeholder (step 4).

## Steps

1. Confirm that `.specify/` exists (the project was initialised with `specify init`), that this extension is installed at `.specify/extensions/technical-solution/`, and that the `central-workspace` preset is installed at `.specify/presets/central-workspace/preset.yml`. Stop and report the missing path otherwise; for the preset, tell the user to run `specify preset add --dev <toolkit>/presets/central-workspace`, because without it the core commands write to `specs/` instead of the workspace layout.
2. Create each of the following files at the workspace root only if it does not exist yet, copying the seed from `.specify/extensions/technical-solution/workspace/`:
   - `spec-kit-workspace.json` from `.specify/extensions/technical-solution/workspace/spec-kit-workspace.json`; in the new copy, replace the seed `workspace_id` (`central-workspace`) with the name the user gave for this workspace, or with the name of the workspace directory
   - `spec-kit-workspace.local.json.template` from `.specify/extensions/technical-solution/workspace/spec-kit-workspace.local.json.template`
   - `initiatives/README.md` from `.specify/extensions/technical-solution/workspace/initiatives-README.md`
   - `.specify/profiles/README.md` and `.specify/profiles/example-salesforce.md` from `.specify/extensions/technical-solution/workspace/profiles/`
3. Make sure the root `.gitignore` exists and contains these lines, creating the file or appending the missing lines: `spec-kit-workspace.local.json` (machine-local paths, never versioned), `__pycache__/` and `*.pyc` (bytecode of the resolver), and `.claude/settings.local.json` (local agent settings).
4. Constitution: `specify init` with the `central-workspace` preset already installs the workspace constitution, so this step matters only when the preset was added to an existing project. If `.specify/memory/constitution.md` is missing, or is still the unmodified Spec Kit default (its title still reads `[PROJECT_NAME] Constitution`), replace it with the resolved `constitution-template` (run `specify preset resolve constitution-template`; the `central-workspace` preset provides the workspace constitution). Then, if the file still contains `[RATIFICATION_DATE]` or `[LAST_AMENDED_DATE]`, replace both with today's date (`YYYY-MM-DD`): the day this workspace adopted the constitution. Change nothing else in it; if it has been customised in any other way, leave that content untouched and report it. Later amendments go through `/speckit-constitution`.
5. If the user input contains `--with-claude-plugin`, copy `.specify/extensions/technical-solution/workspace/claude-marketplace/` to `claude-marketplace/` at the workspace root, only if that directory is absent. It lets a parent repository mount this workspace as a submodule and invoke `/mulesoft-spec-kit:run`; see `claude-marketplace/README.md`.
6. Verify the resolver by running `.specify/extensions/technical-solution/scripts/source_workspaces/cli.py list` with your Python 3 interpreter (`python3` on Linux and macOS, `python` on Windows) and report its output. An error about the missing local registry is expected until the operator copies the template to `spec-kit-workspace.local.json` and registers repository roots.
7. Report every file created, every file left untouched, and the next step: `/speckit-technical-solution-run specify <initiative-id-or-source>`.

Never write credentials, machine-local paths or organisation names into versioned files.
