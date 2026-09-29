---
name: run
description: Run or resume a Spec Kit initiative through requirements, planning, implementation, testing, and deployment from a parent repository that mounts the central workspace as a submodule.
argument-hint: <phase-or-full-cycle> <initiative-id-or-source> [domain] [repository-id-or-root]
user-invocable: true
disable-model-invocation: false
---

# Spec Kit workspace lifecycle entrypoint

This skill runs in a Claude Code session rooted at a parent repository that mounts the central Spec
Kit workspace as a submodule. The canonical workflow, domain routing, stage gates, resolver contract,
and artifact policy live in that workspace, not in this adapter.

## Required startup

1. Locate the workspace root. This plugin is published from
   `<workspace>/claude-marketplace/plugins/speckit-workspace/`, so the workspace root is
   `${CLAUDE_PLUGIN_ROOT}/../../..`. If that variable is unavailable, use the single directory under
   the current project root that contains `spec-kit-workspace.json`; if none or more than one
   exists, stop and report it. Refer to the resolved directory as `<workspace>` below.
2. Confirm that `<workspace>/spec-kit-workspace.json` exists. If the submodule is absent or empty,
   stop and report that it must be initialized with
   `git submodule update --init --recursive <submodule-path>`.
3. Read `<workspace>/.claude/skills/speckit-technical-solution-run/SKILL.md` completely. Treat it as
   the canonical orchestration contract and follow its dispatch, routing, gates, safety rules, and
   completion report for this invocation.
4. Read the lifecycle, workflow contract, and domain lifecycle documents that the canonical skill
   selects. Resolve their relative paths from `<workspace>`, not from the parent repository root.
5. Run Spec Kit commands with `<workspace>` as their working directory, while keeping the Claude
   session rooted in the parent repository. The initiative registry and every initiative artifact
   belong under `<workspace>/initiatives/`.
6. For source-code stages, use the workspace's resolver CLI and its machine-local
   `spec-kit-workspace.local.json`. Relative source roots are resolved from `<workspace>`. Never
   infer a repository by scanning folders or choose an ambiguous match.

Do not reproduce or replace the canonical workflow in this adapter. If its required file or a
declared workflow resource is missing, stop with the exact missing path instead of substituting a
different workflow.
