# Technical initiatives

Each initiative has the directory `initiatives/<id>/` with `initiative.yml`, `common/` and only the confirmed domain folders.

The root `spec-kit-workspace.json` is the authoritative manifest for the paths of this structure and for the installed adapters.

```text
initiatives/<id>/
├── README.md
├── initiative.yml
├── common/
├── salesforce/     # if impacted
├── mulesoft/       # if impacted
└── <domain>/       # if an explicit adapter exists
```

Use `/speckit-technical-solution-run` to start or resume the complete lifecycle. Design stages do not require application repositories. For analysis, implementation and verification, select the repository and record the observed revision. Do not copy raw source documents; create synthetic artifacts with verifiable references.
