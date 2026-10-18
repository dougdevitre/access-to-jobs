#!/usr/bin/env bash
# build-skill.sh — Package the skill sources into access-to-jobs.skill
# Usage: ./scripts/build-skill.sh [output-name]   build (default: access-to-jobs.skill)
#        ./scripts/build-skill.sh --check         fail if the committed package is stale
#
# Rebuild and commit the package whenever SKILL.md or any packaged file changes:
# Claude loads the .skill file, not the repo. The build is deterministic (sorted
# files, fixed timestamps); the file list lives in scripts/build-skill.py.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/build-skill.py" "$@"
