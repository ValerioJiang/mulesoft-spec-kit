# Bundles

A [bundle](https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md) names a set of extensions, presets and workflows that are installed together.

| Bundle | Contents |
| --- | --- |
| [`central-workspace`](central-workspace/bundle.yml) | Extensions `technical-solution`, `mulesoft`, `salesforce`, `sf-workspace`; preset `central-workspace`; workflow `technical-solution`. |

## Publishing, so that `specify bundle install central-workspace` works

Bundle components are resolved by catalog ID through each primitive's own catalog, so four catalog files have to be served over HTTPS from a release of this repository and registered by the user:

| Catalog | File | Registered with |
| --- | --- | --- |
| extensions | `extensions/catalog.json` | `specify extension catalog add <url>` |
| presets | `presets/catalog.json` | `specify preset catalog add <url>` |
| workflows | `workflows/catalog.json` | `specify workflow catalog add <url>` |
| bundles | `bundles/catalog.json` | `specify bundle catalog add <url>` |

Before serving them, replace every `<...-when-served>` and `<release-archive-url...>` placeholder with the real URLs (release archives for extensions and the preset, raw file URLs for the workflow and the bundle). `specify bundle validate --path bundles/central-workspace` reports unresolved components until the catalogs are registered; that is expected.

Until the catalogs are published, install the same set from a local checkout with `scripts/bash/create-workspace.sh <target-dir>` (or `scripts/powershell/create-workspace.ps1`) or with the explicit `specify init --preset ... --extension ...` commands in the [quickstart](../docs/quickstart.md). The `sf-workspace` add-on is opt-in there (`--with-sf-workspace`) even though the bundle lists it.
