#!/usr/bin/env bash
# Create a central Spec Kit workspace from this toolkit checkout.
#
#   scripts/bash/create-workspace.sh <target-dir> [--integration <id>] [--without-sf-workspace]
#
# Runs `specify init` with the central-workspace preset and the extensions of this
# repository, then installs the technical-solution workflow. Requires the specify CLI
# (https://github.com/github/spec-kit) on PATH. Nothing is written outside <target-dir>.
set -euo pipefail

TOOLKIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET="${1:?usage: create-workspace.sh <target-dir> [--integration <id>] [--without-sf-workspace]}"
shift
INTEGRATION="claude"
SF_WORKSPACE=1
while [ $# -gt 0 ]; do
  case "$1" in
    --integration) INTEGRATION="$2"; shift 2 ;;
    --without-sf-workspace) SF_WORKSPACE=0; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

command -v specify >/dev/null 2>&1 || { echo "specify CLI not found on PATH" >&2; exit 1; }
mkdir -p "$TARGET"

args=(
  --here --force --non-interactive --ignore-agent-tools
  --integration "$INTEGRATION"
  --preset "$TOOLKIT/presets/central-workspace"
  --extension "$TOOLKIT/extensions/technical-solution"
  --extension "$TOOLKIT/extensions/mulesoft"
  --extension "$TOOLKIT/extensions/salesforce"
)
if [ "$SF_WORKSPACE" = 1 ]; then
  args+=(--extension "$TOOLKIT/extensions/sf-workspace")
fi

(
  cd "$TARGET"
  specify init "${args[@]}"
  specify workflow add --dev "$TOOLKIT/workflows/technical-solution"
)

cat <<MSG

Workspace created at: $TARGET
Next: open your coding agent there and run /speckit-technical-solution-setup
      (creates spec-kit-workspace.json, initiatives/ and .specify/profiles/ without overwriting anything).
MSG
