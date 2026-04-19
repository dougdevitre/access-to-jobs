#!/usr/bin/env bash
# validate-state.sh — Verify a state deployment is complete
# Usage: ./scripts/validate-state.sh <state-abbreviation>
# Example: ./scripts/validate-state.sh il

set -euo pipefail

STATE_ABBR="${1:-}"

if [[ -z "$STATE_ABBR" ]]; then
  echo "Usage: ./scripts/validate-state.sh <state-abbreviation>"
  echo "Example: ./scripts/validate-state.sh il"
  exit 1
fi

STATE_ABBR_LOWER=$(echo "$STATE_ABBR" | tr '[:upper:]' '[:lower:]')
STATE_DIR="states/${STATE_ABBR_LOWER}"

echo "=== Access to Jobs — State Deployment Validator ==="
echo "Validating: ${STATE_DIR}/"
echo ""

ERRORS=0
WARNINGS=0

# Check state directory exists
if [[ ! -d "$STATE_DIR" ]]; then
  echo "❌ FAIL: State directory ${STATE_DIR}/ does not exist"
  echo "  Run: ./scripts/deploy-state.sh ${STATE_ABBR_LOWER} <StateName>"
  exit 1
fi

# Required reference files
REQUIRED_FILES=(
  "references/state-programs.md"
  "references/state-labor-market.md"
  "references/state-training-pathways.md"
  "references/local-area.md"
)

# Files that should exist (copied during scaffolding)
EXPECTED_FILES=(
  "references/barrier-populations.md"
  "references/action-plan-template.md"
  "references/staff-workflows.md"
  "references/jobseeker-experience.md"
  "references/public-service-hiring.md"
  "references/hr-manager-toolkit.md"
  "references/resume-template.md"
  "references/cover-letter-template.md"
)

echo "--- Checking required files (need full rewrite) ---"
for file in "${REQUIRED_FILES[@]}"; do
  filepath="${STATE_DIR}/${file}"
  if [[ ! -f "$filepath" ]]; then
    echo "❌ MISSING: ${filepath}"
    ((ERRORS++))
  elif grep -q "^## TODO:" "$filepath" 2>/dev/null; then
    echo "⚠️  TODO:   ${filepath} still contains TODO placeholders"
    ((WARNINGS++))
  else
    size=$(wc -c < "$filepath")
    echo "✅ OK:     ${filepath} (${size} bytes)"
  fi
done

echo ""
echo "--- Checking expected files (should be copied/customized) ---"
for file in "${EXPECTED_FILES[@]}"; do
  filepath="${STATE_DIR}/${file}"
  if [[ ! -f "$filepath" ]]; then
    echo "⚠️  MISSING: ${filepath} (should be copied from references/)"
    ((WARNINGS++))
  else
    echo "✅ OK:     ${filepath}"
  fi
done

echo ""
echo "--- Checking for state README ---"
if [[ -f "${STATE_DIR}/README.md" ]]; then
  echo "✅ OK:     ${STATE_DIR}/README.md"
else
  echo "⚠️  MISSING: ${STATE_DIR}/README.md (recommended)"
  ((WARNINGS++))
fi

echo ""
echo "--- Checking JSON schemas are valid ---"
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "❌ FAIL: python3/python is required to validate schemas"
  exit 1
fi
for schema in schemas/*.json; do
  if "$PYTHON" -c 'import json,sys; json.load(open(sys.argv[1]))' "$schema" 2>/dev/null; then
    echo "✅ OK:     ${schema}"
  else
    echo "❌ INVALID: ${schema}"
    ((ERRORS++))
  fi
done

echo ""
echo "--- Checking for source citations ---"
for file in "${REQUIRED_FILES[@]}"; do
  filepath="${STATE_DIR}/${file}"
  if [[ -f "$filepath" ]] && ! grep -qi "source:" "$filepath" 2>/dev/null; then
    echo "⚠️  NO SOURCE: ${filepath} is missing a ### Source: citation"
    ((WARNINGS++))
  fi
done

echo ""
echo "========================================="
if [[ $ERRORS -gt 0 ]]; then
  echo "RESULT: ❌ FAIL — ${ERRORS} error(s), ${WARNINGS} warning(s)"
  exit 1
elif [[ $WARNINGS -gt 0 ]]; then
  echo "RESULT: ⚠️  PASS with ${WARNINGS} warning(s)"
  echo "Address warnings before submitting a PR."
  exit 0
else
  echo "RESULT: ✅ PASS — all checks passed"
  exit 0
fi
