# Bundles

A [bundle](https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md) names a set of extensions, presets and workflows that are installed together.

| Bundle | Contents |
|---|---|
| [`central-workspace`](central-workspace/bundle.yml) | Extensions `technical-solution`, `mulesoft`, `salesforce`, `sf-workspace`; preset `central-workspace`; workflow `technical-solution`. |

Bundle components are resolved by catalog ID, so `specify bundle install central-workspace` works once the extensions, preset and workflow of this repository are served from an HTTPS catalog (see `extensions/catalog.json`). Until then, install the same set from the local checkout with `scripts/bash/create-workspace.sh <target-dir>` or with the explicit `specify init --preset ... --extension ...` commands in the [quickstart](../docs/quickstart.md).
