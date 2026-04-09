#!/usr/bin/env bash
# build-skill.sh — Package repo content into a .skill file for Claude upload
# Usage: ./scripts/build-skill.sh [output-name]
# Examples:
#   ./scripts/build-skill.sh                        → access-to-jobs.skill
#   ./scripts/build-skill.sh access-to-jobs.skill   → access-to-jobs.skill
#   ./scripts/build-skill.sh --versioned            → access-to-jobs-v4.1.0.skill (auto-detects from CHANGELOG)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Detect version from CHANGELOG.md header (e.g., "## v4.1.0")
detect_version() {
  grep -oP '## v\K[0-9]+\.[0-9]+\.[0-9]+' "$REPO_ROOT/CHANGELOG.md" | head -1
}

# Handle --versioned flag
if [ "${1:-}" = "--versioned" ]; then
  VERSION=$(detect_version)
  if [ -z "$VERSION" ]; then
    echo "❌ Could not detect version from CHANGELOG.md"
    exit 1
  fi
  OUTPUT_NAME="access-to-jobs-v${VERSION}.skill"
else
  OUTPUT_NAME="${1:-access-to-jobs.skill}"
fi

OUTPUT_PATH="${REPO_ROOT}/${OUTPUT_NAME}"

echo "=== Access to Jobs — Skill Builder ==="
echo "Source:  ${REPO_ROOT}"
echo "Output:  ${OUTPUT_PATH}"
if [ "${1:-}" = "--versioned" ]; then
  echo "Version: ${VERSION}"
fi
echo ""

# Remove old build if exists
rm -f "$OUTPUT_PATH"

# Build the .skill zip from repo root
# Include all content directories and key files, exclude dev/CI files
cd "$REPO_ROOT"

zip -r "$OUTPUT_PATH" \
  SKILL.md \
  README.md \
  INSTALL.md \
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
echo ""
echo "To create a GitHub release, tag and push:"
echo "  git tag v<VERSION>"
echo "  git push origin v<VERSION>"
echo "The release workflow will build and publish the .skill file automatically."
