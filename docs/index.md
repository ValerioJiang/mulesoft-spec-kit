# Spec Kit Workspace documentation

Spec Kit Workspace packages a *central workspace* for Spec-Driven Development across several application repositories (Salesforce, MuleSoft, and any further domain with an adapter) as standard [Spec Kit](https://github.com/github/spec-kit) building blocks.

## Getting started

- [Quickstart](quickstart.md): install the CLI, create a workspace, run the first initiative.
- [Existing repositories](guides/existing-repositories.md): bring an application repository that already has its own conventions into the workspace.

## Concepts

- [The central workspace](concepts/central-workspace.md): the layers, boundaries and versioning of a workspace.
- [Lifecycle](concepts/lifecycle.md): the directory contract, the stages per domain, evidence and states.

## Guides

- [Source repositories](guides/source-workspaces.md): register and resolve the application repositories an initiative works on.
- [Organisation profiles](guides/organisation-profiles.md): express tracker, branch, quality-gate and release conventions without baking them into the toolkit.
- [Claude Code plugin for a parent repository](guides/claude-code-plugin.md): expose the workspace from a monorepo or programme repository that mounts it as a submodule.

## Reference

- [Commands](reference/commands.md): every command of every extension and of the preset.
- [Workflow contract](reference/workflow-contract.md): inputs, stages, gates, evidence labels and states.
- Manifests: [extensions](../extensions/), [preset](../presets/central-workspace/preset.yml), [workflow](../workflows/technical-solution/workflow.yml), [bundle](../bundles/central-workspace/bundle.yml).
