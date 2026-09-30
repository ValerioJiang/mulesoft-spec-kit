# Claude Code plugin for a parent repository

This directory is a local Claude Code marketplace with one plugin, `mulesoft-spec-kit`. It is for the setup where this workspace is mounted as a Git submodule of a parent repository and people start Claude Code from the parent root. When the workspace is used on its own, ignore it: the generated skills under `.claude/skills/` are all you need.

```text
claude-marketplace/
├── .claude-plugin/marketplace.json
└── plugins/mulesoft-spec-kit/
    ├── .claude-plugin/plugin.json
    └── skills/run/SKILL.md
```

From the root of the parent repository, each developer registers the marketplace and installs the plugin once (replace `<submodule-path>` with the path of this workspace inside the parent):

```bash
claude plugin marketplace add ./<submodule-path>/claude-marketplace
claude plugin install mulesoft-spec-kit@mulesoft-spec-kit --scope project
```

The lifecycle then starts or resumes with `/mulesoft-spec-kit:run <stage-or-full-cycle> <initiative-id-or-source>`. The skill is a thin adapter: it finds this workspace from its own location, reads the workspace's `/speckit-technical-solution-run` skill and follows it, so the workflow, the resolver and the gates are defined in one place only.
