# Bundles

A [bundle](https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md) names a set of extensions, presets and workflows that are installed together.

| Bundle | Contents |
| --- | --- |
| [`central-workspace`](central-workspace/bundle.yml) | Extensions `technical-solution`, `mulesoft`, `salesforce`, `sf-workspace`; preset `central-workspace`; workflow `technical-solution`. |

## Publishing, so that `specify bundle install central-workspace` works

Bundle components are resolved by catalog ID through each primitive's own catalog. The four catalog files of this repository are served from `main` on GitHub and already carry their URLs:

| Catalog | Served at | Registered with |
| --- | --- | --- |
| extensions | `https://raw.githubusercontent.com/ValerioJiang/spec-kit-workspace/main/extensions/catalog.json` | `specify extension catalog add <url>` |
| presets | `https://raw.githubusercontent.com/ValerioJiang/spec-kit-workspace/main/presets/catalog.json` | `specify preset catalog add <url>` |
| workflows | `https://raw.githubusercontent.com/ValerioJiang/spec-kit-workspace/main/workflows/catalog.json` | `specify workflow catalog add <url>` |
| bundles | `https://raw.githubusercontent.com/ValerioJiang/spec-kit-workspace/main/bundles/catalog.json` | `specify bundle catalog add <url>` |

The workflow and the bundle are downloaded as raw files, so they work as soon as `main` is pushed. Extensions and the preset are downloaded as archives with the component directory as the single top-level folder, so a release must exist with those assets attached. The catalogs point at release `v0.1.0`:

```bash
python scripts/python/build-release-assets.py          # writes dist/<id>-<version>.zip
gh release create v0.1.0 dist/*.zip --title "Spec Kit Workspace 0.1.0" --notes-file CHANGELOG.md
```

When a component version changes, update its `download_url` (and the release tag) in the catalog before cutting the next release. `specify bundle validate --path bundles/central-workspace` reports unresolved components until the catalogs are registered in a project; that is expected.

Without the catalogs, install the same set from a local checkout with `scripts/bash/create-workspace.sh <target-dir>` (or `scripts/powershell/create-workspace.ps1`) or with the explicit `specify init --preset ... --extension ...` commands in the [quickstart](../docs/quickstart.md). The `sf-workspace` add-on is opt-in there (`--with-sf-workspace`) even though the bundle lists it.
