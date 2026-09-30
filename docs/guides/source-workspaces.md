# Source workspace registry

Spec Kit and the initiative artifacts live in the central workspace. Application repositories remain separate sources of truth. The versioned file `spec-kit-workspace.json` defines the resolution contract and the CLI; the local source workspace roots live in the ignored file `spec-kit-workspace.local.json`.

A *source workspace* is a registered root from which application repositories are resolved. It is either one application repository (resolver `git-root`) or a catalog of nested application repositories (resolver `path-remote-manifest`). Its ID is the `id` of its profile, and the resolver's output repeats it as `source_workspace_id`. It is not the central workspace, whose own name is the top-level `workspace_id` of `spec-kit-workspace.json`.

## Registering source workspaces

Copy `spec-kit-workspace.local.json.template` to `spec-kit-workspace.local.json` at the root of the workspace. The stable profiles (`id`, `domain`, `resolver`, remote identity and manifest, if needed) are versioned in `source_workspace_profiles` inside `spec-kit-workspace.json`. The ignored local file contains only the mapping between each ID and the machine root in `workspace_roots`; relative paths start from the central root, absolute ones are allowed only here. Do not record local paths in the initiative artifacts or in the versioned configuration.

```json
{
  "schema_version": 1,
  "workspace_roots": [
    {
      "id": "salesforce-app",
      "root": "../my-salesforce-app"
    },
    {
      "id": "mulesoft-catalog",
      "root": "../my-mulesoft-catalog"
    }
  ]
}
```

The `salesforce-app` profile uses `git-root` and points to a single repository; it can constrain the expected remote with the optional `expected_remote` field. `mulesoft-catalog` uses `path-remote-manifest` on the `repos.conf` manifest of the registered root: a text file with one line per repository (`<relative-path> <remote-url>`, comments with `#`) that lists the nested application repositories. Local paths are relative to the root of this workspace. For a new source workspace, version its profile and add only the local path; for a new format, implement and register an adapter once, without changing the skills. CLI dispatch is based on the adapter registry: the central registry contains no platform-specific branches.

From `source_resolution` the resolver reads `profile_collection`, `local_collection`, the four field lists, `resolvers.<id>.required_profile_fields` and `absolute_roots_allowed`. The other keys (`selection`, `manifest_format`, `comment_prefix`, `reject_path_traversal`, `filesystem_search`, `path_policy` and the like) describe behaviour that is fixed in the resolver code for agents and readers; editing them changes nothing.

A remote named in a catalog manifest or in `expected_remote` must be host-based (`https://host/path` or `host:path`). A repository whose `origin` is a filesystem path, or that has no `origin`, resolves with `remote_identity: null`, because a local path identifies nothing outside one machine.

## Shared CLI

All skills use the CLI indicated by `source_resolution.entrypoint` in the root manifest. Skills do not interpret the local configuration or the repository manifests directly.

```sh
# python3 on Linux and macOS, python on Windows
python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py list --domain mulesoft
python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py resolve 'mulesoft-catalog:experience/orders-xapi'
python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py resolve salesforce-app
# a one-off root that is not registered: it passes the same Git checks
python3 .specify/extensions/technical-solution/scripts/source_workspaces/cli.py resolve --root ../one-off-repository --domain mulesoft
```

Catalog selection is exact: `<source-workspace-id>:<relative-repository-path>`. The resolver reads only the manifest declared by the profile, rejects duplicate paths or paths that escape the root, verifies the expected remote and that the selected path coincides with the Git root. It reports repository identity, branch, commit and working tree. Unconfigured local roots or missing checkouts produce an explicit error; the first result is not chosen, the filesystem is not searched and repositories are not cloned. A root passed for a single invocation must pass the same Git checks.

The CLI output may show local absolute paths for the current operation. Use them only in the session; in the initiative artifacts record the repository identity and revision, never personal paths or credentials.

## Evidence per domain

### Salesforce

After resolution, detect `sfdx-project.json`, package directories and the repository toolchain. Use a connected, read-only Salesforce capability for the required live facts. Do not use CLI or static files as substitutes for live evidence and do not read business records.

### MuleSoft

After resolving the selected nested repository, detect the Git root, layer, `pom.xml`, `mule-artifact.json`, RAML/OAS/AsyncAPI sources, dependencies and MUnit tests. Distinguish source contracts from Exchange publications. Use Anypoint, Exchange or Runtime Manager when version, compatibility or runtime state affect the decision; otherwise mark the evidence `NOT_EXECUTED`. Do not assume that all applications in the manifest are involved.

## Boundaries

Design stages do not require application repositories and do not write into the application repositories. Code stages operate only in the selected Git root and within the task perimeter. The local registry contains paths, not credentials, org aliases or environment targets. External writes, publications and deployments require a direct request and an explicit target.
