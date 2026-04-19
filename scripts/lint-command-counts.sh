#!/usr/bin/env bash
# lint-command-counts.sh — Catch drift between slash-commands/commands.md
# and the three places README.md states the command count.

set -euo pipefail

COMMANDS_FILE="slash-commands/commands.md"
README_FILE="README.md"

if [[ ! -f "$COMMANDS_FILE" || ! -f "$README_FILE" ]]; then
  echo "❌ FAIL: expected $COMMANDS_FILE and $README_FILE in CWD"
  exit 1
fi

actual=$(grep -cE '^\| `/' "$COMMANDS_FILE")

readme_trigger=$(grep -oE '^[0-9]+ quick-trigger commands' "$README_FILE" | grep -oE '^[0-9]+' || true)
readme_stats=$(grep -oE '^\| Slash commands \| [0-9]+' "$README_FILE" | grep -oE '[0-9]+$' || true)
readme_tree=$(grep -oE 'commands\.md[[:space:]]+[0-9]+ commands' "$README_FILE" | grep -oE '[0-9]+' || true)

fail=0
check() {
  local label="$1" value="$2"
  if [[ -z "$value" ]]; then
    echo "❌ $label: not found in $README_FILE"
    fail=1
  elif [[ "$value" != "$actual" ]]; then
    echo "❌ $label: README says $value, $COMMANDS_FILE has $actual"
    fail=1
  else
    echo "✅ $label: $value"
  fi
}

echo "Command rows in $COMMANDS_FILE: $actual"
check "quick-trigger count"          "$readme_trigger"
check "Repo Stats 'Slash commands'"  "$readme_stats"
check "Directory-structure listing"  "$readme_tree"

if [[ $fail -ne 0 ]]; then
  echo ""
  echo "Update README.md to match $actual, or add rows to $COMMANDS_FILE."
  exit 1
fi

echo "✅ Command counts consistent ($actual everywhere)."
