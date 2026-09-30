## What changes and why

<!-- The behaviour that changes for someone using a workspace, and the reason. Keep prompt changes small. -->

## How it was checked

<!-- Which commands you regenerated in a scratch workspace and read, and what you ran. -->

- [ ] Created a scratch workspace with `scripts/bash/create-workspace.sh` (or the PowerShell twin) and read the generated file of every command I touched
- [ ] `python scripts/python/check-consistency.py` passes
- [ ] `python -m unittest discover -s tests` passes (if the resolver changed)

## Checklist

- [ ] Bumped the `version` of every manifest I changed, its catalog entry and the bundle pin, and added a line to `CHANGELOG.md`
- [ ] No organisation names, remotes, hosts, tracker keys, environment names or quality thresholds in prompts or templates
- [ ] Vendored files under `extensions/sf-workspace/prompts/`, `sf-templates/` and `docs/` are untouched
- [ ] Used the vocabulary of `docs/concepts/central-workspace.md` (application repository, source workspace)
