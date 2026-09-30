# Quickstart

## 1. Install the Spec Kit CLI

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify --version   # 1.0 or later
```

Other installation methods are in the [Spec Kit installation guide](https://github.com/github/spec-kit/blob/main/docs/installation.md).

## 2. Create a workspace

Clone this repository once (it is the source of the building blocks, not the workspace itself), then create a workspace next to it:

```bash
git clone https://github.com/ValerioJiang/mulesoft-spec-kit.git mulesoft-spec-kit
mulesoft-spec-kit/scripts/bash/create-workspace.sh my-workspace --integration claude
```

The script is equivalent to:

```bash
mkdir my-workspace && cd my-workspace
specify init --here --force --non-interactive --ignore-agent-tools --integration claude --script sh \
  --preset    ../mulesoft-spec-kit/presets/central-workspace \
  --extension ../mulesoft-spec-kit/extensions/technical-solution \
  --extension ../mulesoft-spec-kit/extensions/mulesoft \
  --extension ../mulesoft-spec-kit/extensions/salesforce
specify workflow add --dev ../mulesoft-spec-kit/workflows/technical-solution
```

plus a `.gitignore` seed and a check that every component is present (`specify init` returns 0 even when a component fails to install). The preset is not optional: without it the core commands write to `specs/` instead of `initiatives/`. Add `--extension ../mulesoft-spec-kit/extensions/sf-workspace` (script: `--with-sf-workspace`) only if you want the extended Salesforce add-on; its prompts contain deploy and login commands, gated to explicit requests. After a toolkit update, refresh an existing workspace with `create-workspace.sh my-workspace --update`. On Windows use the PowerShell twin `scripts\powershell\create-workspace.ps1` or Git Bash. Both default to `--script sh`; choose `ps` only if your agent runs `python3` from PowerShell.

Use any integration Spec Kit supports in place of `claude`; the commands are generated from the same sources. Put the workspace under version control: it is where every initiative's artifacts will live.

## 3. Initialise the workspace files

Open your coding agent in `my-workspace` and run:

```text
/speckit-technical-solution-setup
```

It creates `spec-kit-workspace.json` (workspace identity, artifact layout and resolver profiles), `spec-kit-workspace.local.json.template`, `initiatives/README.md` and `.specify/profiles/`. Nothing you have written is overwritten; the workspace constitution is already in place, installed by `specify init` from the preset.

## 4. Register application repositories (only for code stages)

Design stages (`specify`, `clarify`, `plan`, `tasks`) need no repository. Before `analyze`, `implement`, `verify` or `deploy`, register where the code lives:

1. Add a profile to `source_workspace_profiles` in `spec-kit-workspace.json` (versioned): an ID, the domain and the resolver (`git-root` for a single repository, `path-remote-manifest` for a catalog of nested repositories described by a manifest file).
2. Copy `spec-kit-workspace.local.json.template` to `spec-kit-workspace.local.json` (ignored by Git) and map each profile ID to a path on your machine.
3. Check with the resolver (`python3` on Linux and macOS, `python` on Windows):

   ```bash
   python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py list
   python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py resolve <workspace-id>
   ```

Details and examples: [source repositories](guides/source-workspaces.md).

## 5. Run an initiative

```text
/speckit-technical-solution-run specify ORD-042 Order status sync between CRM and the order system
/speckit-technical-solution-run clarify ORD-042
/speckit-technical-solution-run plan ORD-042
/speckit-technical-solution-run tasks ORD-042 mulesoft
/speckit-technical-solution-run analyze ORD-042 mulesoft mulesoft-catalog:experience/orders-xapi
/speckit-technical-solution-run implement ORD-042 mulesoft mulesoft-catalog:experience/orders-xapi
/speckit-technical-solution-run verify ORD-042 mulesoft
/speckit-technical-solution-review ORD-042
```

The first word is the stage, the second the initiative ID (or a source reference), and any further text is the title or request; the orchestrator derives a filesystem-safe folder name (`ORD-042-order-status-sync`). `full` runs the internal stages in sequence and stops at every gate; external actions (tests, deployments, tickets, PR/MR) run only when you ask for them explicitly with their target. You can also call the stage commands directly (`/speckit-mulesoft-plan ORD-042`, `/speckit-salesforce-clarify ORD-042`, `/speckit-tasks ORD-042 common`) or run the workflow with `specify workflow run technical-solution`.

## 6. Where things end up

```text
my-workspace/initiatives/ORD-042-order-status-sync/
├── README.md  initiative.yml
├── common/      initiative.md  integration-matrix.md  decisions.md  review.md
├── salesforce/  spec.md  clarification-report.md  plan.md  data-model.md  tasks.md  ...
└── mulesoft/    spec.md  clarification-report.md  plan.md  contracts/  tasks.md  verification/  release.md
```

See [examples](../examples/README.md) for a fuller picture and the [lifecycle](concepts/lifecycle.md) for what each stage produces.
