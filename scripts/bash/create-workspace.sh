#!/usr/bin/env bash
# Create or update a central Spec Kit workspace from this toolkit checkout.
#
#   scripts/bash/create-workspace.sh <target-dir> [--integration <id>] [--script sh|ps|py]
#                                    [--with-sf-workspace] [--update]
#
#   --integration <id>    coding agent integration (default: claude)
#   --script sh|ps|py     Spec Kit helper-script variant (default: sh; use ps only if your
#                         agent runs in PowerShell and `python3` is on its PATH)
#   --with-sf-workspace   also install the optional sf-workspace add-on (extended Salesforce
#                         lifecycle; its prompts contain deploy/login/test commands)
#   --update              refresh the preset, extensions and workflow of an existing workspace
#
# Requires the specify CLI (https://github.com/github/spec-kit) on PATH. Writes only inside
# <target-dir>. Refuses to run inside the toolkit checkout and refuses to re-initialise an
# existing workspace unless --update is given. Exits non-zero when any component is missing
# afterwards.
set -euo pipefail

usage() { sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit "${1:-2}"; }
fail() { echo "create-workspace: $*" >&2; exit 1; }

TOOLKIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET=""; INTEGRATION="claude"; SCRIPT="sh"; WITH_SF=0; UPDATE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --integration) INTEGRATION="${2:?--integration needs a value}"; shift 2 ;;
    --script) SCRIPT="${2:?--script needs a value}"; shift 2 ;;
    --with-sf-workspace) WITH_SF=1; shift ;;
    --update) UPDATE=1; shift ;;
    -h|--help) usage 0 ;;
    -*) fail "unknown option: $1" ;;
    *) [ -z "$TARGET" ] || fail "only one target directory is accepted (got '$TARGET' and '$1')"
       TARGET="$1"; shift ;;
  esac
done
[ -n "$TARGET" ] || usage
case "$SCRIPT" in sh|ps|py) ;; *) fail "--script must be sh, ps or py" ;; esac
command -v specify >/dev/null 2>&1 || fail "specify CLI not found on PATH"

# Every refusal that can be decided without touching the filesystem comes before mkdir.
case "$TARGET" in /*) target_abs="$TARGET" ;; *) target_abs="$PWD/$TARGET" ;; esac
case "${target_abs%/}" in
  "$TOOLKIT"|"$TOOLKIT"/*) fail "refusing to create a workspace inside the toolkit checkout ($TOOLKIT)" ;;
esac
if [ "$UPDATE" = 1 ] && [ ! -e "$TARGET/.specify" ]; then
  fail "$TARGET is not a Spec Kit project yet; run without --update"
fi
created=0
[ -d "$TARGET" ] || { mkdir -p "$TARGET"; created=1; }
TARGET="$(cd "$TARGET" && pwd)"
case "$TARGET" in
  "$TOOLKIT"|"$TOOLKIT"/*)
    [ "$created" = 1 ] && rmdir "$TARGET" 2>/dev/null
    fail "refusing to create a workspace inside the toolkit checkout ($TOOLKIT)" ;;
esac
if [ -e "$TARGET/.specify" ] && [ "$UPDATE" = 0 ]; then
  fail "$TARGET is already a Spec Kit project; re-run with --update to refresh the toolkit components"
fi

EXTENSIONS=(technical-solution mulesoft salesforce)
[ "$WITH_SF" = 1 ] && EXTENSIONS+=(sf-workspace)

cd "$TARGET"
if [ "$UPDATE" = 0 ]; then
  args=(--here --force --non-interactive --ignore-agent-tools
        --integration "$INTEGRATION" --script "$SCRIPT"
        --preset "$TOOLKIT/presets/central-workspace")
  for ext in "${EXTENSIONS[@]}"; do args+=(--extension "$TOOLKIT/extensions/$ext"); done
  specify init "${args[@]}"
  specify workflow add --dev "$TOOLKIT/workflows/technical-solution"
else
  if [ -d .specify/presets/central-workspace ]; then
    specify preset update central-workspace --dev "$TOOLKIT/presets/central-workspace"
  else
    specify preset add --dev "$TOOLKIT/presets/central-workspace"
  fi
  for ext in "${EXTENSIONS[@]}"; do
    specify extension add --dev "$TOOLKIT/extensions/$ext" --force
  done
  specify workflow remove technical-solution >/dev/null 2>&1 || true
  specify workflow add --dev "$TOOLKIT/workflows/technical-solution"
fi

# `specify extension add --dev` links every generated command to a cache under
# .specify/extensions/<id>/.specify-dev/. A workspace is a shared repository, and Git checks
# symlinks out as plain text files where they are unsupported (the Windows default), so turn
# the links back into regular files. `specify init` writes regular files already.
while IFS= read -r -d '' link; do
  case "$(readlink "$link")" in
    *.specify-dev/*) cp -L "$link" "$link.materialised" && mv -f "$link.materialised" "$link" ;;
  esac
done < <(find . -path ./.git -prune -o -type l -print0)

# Verify every component is present; specify init returns 0 even when a component failed.
missing=0
[ -f .specify/presets/central-workspace/preset.yml ] || { echo "missing: preset central-workspace" >&2; missing=1; }
for ext in "${EXTENSIONS[@]}"; do
  [ -f ".specify/extensions/$ext/extension.yml" ] || { echo "missing: extension $ext" >&2; missing=1; }
done
[ -f .specify/workflows/technical-solution/workflow.yml ] || { echo "missing: workflow technical-solution" >&2; missing=1; }
[ "$missing" = 0 ] || fail "workspace verification failed; see the messages above"

# Seed the root .gitignore (machine-local registry, Python bytecode, local agent settings,
# the dev-install cache of the CLI).
for line in "spec-kit-workspace.local.json" "__pycache__/" "*.pyc" ".claude/settings.local.json" ".specify-dev/"; do
  grep -qxF "$line" .gitignore 2>/dev/null || printf '%s\n' "$line" >> .gitignore
done

cat <<MSG

Workspace ready at: $TARGET  (integration: $INTEGRATION, scripts: $SCRIPT, extensions: ${EXTENSIONS[*]})
Next: open your coding agent there and run /speckit-technical-solution-setup
      (creates spec-kit-workspace.json, initiatives/ and .specify/profiles/ without overwriting anything).
MSG
