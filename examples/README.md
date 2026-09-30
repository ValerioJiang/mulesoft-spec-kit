# Examples

## A created workspace

Running `scripts/bash/create-workspace.sh my-workspace --integration claude --script sh` and then `/speckit-technical-solution-setup` inside it produces this layout (Claude Code shown; other integrations generate their own command files from the same sources; the script also seeds a root `.gitignore`):

```text
my-workspace/
├── spec-kit-workspace.json                 # workspace identity, artifact layout, resolver profiles (versioned)
├── spec-kit-workspace.local.json.template  # copy to spec-kit-workspace.local.json and add machine-local roots (ignored)
├── initiatives/
│   └── README.md
├── .specify/
│   ├── memory/constitution.md              # workspace constitution (from the central-workspace preset)
│   ├── profiles/                           # optional organisation profiles; example-salesforce.md shows the shape
│   ├── presets/central-workspace/
│   ├── extensions/
│   │   ├── technical-solution/             # commands, templates, docs, scripts/source_workspaces, workspace seeds
│   │   ├── mulesoft/
│   │   ├── salesforce/
│   │   └── sf-workspace/                   # optional
│   ├── workflows/technical-solution/
│   ├── templates/ scripts/ ...             # Spec Kit core
│   └── extensions.yml, .registry, ...
└── .claude/skills/
    ├── speckit-technical-solution-setup/  speckit-technical-solution-run/  speckit-technical-solution-review/
    ├── speckit-specify/ speckit-clarify/ speckit-plan/ speckit-tasks/ speckit-analyze/ speckit-implement/
    ├── speckit-converge/ speckit-checklist/ speckit-taskstoissues/ speckit-review/ speckit-verify/ speckit-release/
    ├── speckit-constitution/   (Spec Kit core, unchanged)
    ├── speckit-mulesoft-*/  (14)
    ├── speckit-salesforce-*/ (4)
    └── speckit-sf-workspace-*/ (14, only with --with-sf-workspace)
```

## An initiative

After `/speckit-technical-solution-run specify ORD-042 "Order status sync"` and the following stages:

```text
initiatives/ORD-042-order-status-sync/
├── README.md
├── initiative.yml
├── common/
│   ├── initiative.md            # shared requirements (REQ-...)
│   ├── integration-matrix.md    # INT-... IDs shared by the domains
│   ├── decisions.md
│   └── review.md
├── salesforce/
│   ├── spec.md  clarification-report.md  plan.md  data-model.md  tasks.md
│   ├── implementation-log.md  verification/  review.md  release.md
└── mulesoft/
    ├── spec.md  clarification-report.md  plan.md  contracts/  tasks.md  analyze.md
    ├── implementation-log.md  verification/  review.md  release.md
```

`initiative.yml` records only stable identities and observed commits:

```yaml
schema_version: 1
initiative:
  id: "ORD-042-order-status-sync"
  title: "Order status sync"
  domains: [common, salesforce, mulesoft]
  source_design:
    reference: "SD-ORD-042 v3 (document management system ID)"
    revision: "2026-09-12"
  repositories:
    salesforce: { name: "crm-app", url: "git@git.example.com:org/crm-app.git", commit: "a1b2c3d" }
    mulesoft:   { name: "orders-xapi", url: "git@git.example.com:org/orders-xapi.git", commit: "e4f5a6b" }
  selected_profiles: []
  state: Planned
```
