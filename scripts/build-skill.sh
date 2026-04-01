#!/usr/bin/env bash
# build-skill.sh — Package repo content into a .skill file for Claude upload
# Usage: ./scripts/build-skill.sh [output-name]
# Example: ./scripts/build-skill.sh access-to-jobs.skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_NAME="${1:-access-to-jobs.skill}"
OUTPUT_PATH="${REPO_ROOT}/${OUTPUT_NAME}"

echo "=== Access to Jobs — Skill Builder ==="
echo "Source:  ${REPO_ROOT}"
echo "Output:  ${OUTPUT_PATH}"
echo ""

# Remove old build if exists
rm -f "$OUTPUT_PATH"

# Build the .skill zip from repo root
# Include all content directories and key files, exclude dev/CI files
cd "$REPO_ROOT"

zip -r "$OUTPUT_PATH" \
  SKILL.md \
  README.md \
  LICENSE \
  CONTRIBUTING.md \
  DEPLOYMENT.md \
  CHANGELOG.md \
  SECURITY.md \
  references/ \
  templates/ \
  schemas/ \
  assets/ \
  slash-commands/ \
  guides/ \
  evals/ \
  states/ \
  scripts/ \
  -x "*.git*" \
  -x "*.DS_Store" \
  -x "scripts/build-skill.sh" \
  -x "scripts/validate-state.sh"

echo ""
echo "✅ Built: ${OUTPUT_PATH}"
echo "   Size: $(du -h "$OUTPUT_PATH" | cut -f1)"
echo ""
echo "Upload to Claude.ai → Settings → Skills"
