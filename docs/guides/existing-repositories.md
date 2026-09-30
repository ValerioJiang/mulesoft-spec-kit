# Adopting the workspace for existing repositories

## Destination and layout

The output of each initiative lives under `initiatives/<id>/common|salesforce|mulesoft|<domain>/`. Code stays in the source repositories chosen per initiative; the Spec Kit lifecycle does not require a parent directory, a known repository name or a `.specify/` inside the application repository.

The adapters are installed in the workspace by the `specify` CLI (`.specify/extensions/<id>/`) and do not depend on files installed in the application repositories.

## Bringing an existing project into the workspace

1. **Register the repository.** Version a profile in `source_workspace_profiles` of `spec-kit-workspace.json` (ID, domain, resolver, optional `expected_remote` or manifest) and map the ID to the local root in the ignored file `spec-kit-workspace.local.json`. See [source-workspaces](source-workspaces.md).
2. **Do not copy local configuration.** Files such as `sf-config.yml`, org aliases, tokens, `.mcp.json` or `.env` of the application repository stay there or in the native clients; they do not enter the workspace or the artifacts.
3. **Convert local overlays and constitutions into a profile.** If the application repository had its own Spec Kit constitution, a rule overlay or team conventions (tracker, branch policy, quality gates, deployment sequences), summarise them in `.specify/profiles/<organisation>-<domain>.md` following `.specify/profiles/example-salesforce.md`. Mark every rule as to be confirmed until an owner verifies it; the generic lifecycle does not select any profile implicitly.
4. **Do not transfer generated artifacts.** Specs, plans or tasks previously produced inside the application repository's `.specify/specs/` are not copied: a new initiative starts from the updated primary source and records the repository identity and revision, not local paths.
5. **Remove duplicate entrypoints.** If the application repository or a parent workspace exposed their own Spec Kit commands, disable them after the cutover: the only entrypoint is `/speckit-technical-solution-run` (or `/mulesoft-spec-kit:run` when the workspace is a submodule).

## Cutover

The cutover moves the complete lifecycle into the central workspace. The local configuration for target repositories is empty by default and includes no predefined paths; the operator selects a repository for each activity that requires code. A project's migration history must be documented in the initiative or in the profile it concerns, not in the commands: references to a previous context describe provenance and are not used at runtime.
