# Claude Code plugin for a parent repository

When a workspace is used on its own, the generated skills in its `.claude/skills/` are all you need; the entrypoint is `/speckit-technical-solution-run`. The plugin described here is for the other setup: the workspace is mounted as a Git submodule of a parent repository (a monorepo or programme repository) and people start Claude Code from the parent root.

The `technical-solution` extension ships a small local marketplace for that case. Run `/speckit-technical-solution-setup --with-claude-plugin` in the workspace and it copies it to `claude-marketplace/` at the workspace root:

```text
claude-marketplace/
├── .claude-plugin/marketplace.json
└── plugins/speckit-workspace/
    ├── .claude-plugin/plugin.json
    └── skills/run/SKILL.md
```

The marketplace is a catalog; the plugin is the installable unit; the skill is the invocable command `/speckit-workspace:run`. The skill is a thin adapter: it does not duplicate the workflow, the resolver or the gates. It locates the workspace root from its own position (`${CLAUDE_PLUGIN_ROOT}/../../..`), reads the workspace's generated `/speckit-technical-solution-run` skill and follows it, running Spec Kit commands with the workspace as their working directory while the Claude session stays rooted in the parent repository.

## Setup in the parent repository

From the root of the parent repository, add and initialise the submodule (here called `spec-kit-workspace`; the name is free):

```bash
git submodule add <workspace-url> spec-kit-workspace
git submodule update --init --recursive spec-kit-workspace
```

Each developer registers the local marketplace and installs the plugin once at project scope:

```bash
claude plugin marketplace add ./spec-kit-workspace/claude-marketplace
claude plugin install speckit-workspace@speckit-workspace --scope project
```

The project configuration then declares the marketplace with a path relative to the parent repository and enables the plugin for it. After trusting the parent folder, every collaborator runs both commands on their own machine. Claude Code is started from the parent root, where the lifecycle starts or resumes with `/speckit-workspace:run`.

To develop the skill from the local checkout there is no need for a second marketplace: the plugin files are read directly from the submodule, and changes are picked up after a new session or `/reload-plugins`. Changes meant for the team are versioned in the workspace and selected by updating the gitlink in the parent repository.
