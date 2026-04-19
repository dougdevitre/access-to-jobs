#!/usr/bin/env bash
# validate-evals.sh — Verify every `expected_module` and `expected_programs` value
# in evals/*.json is listed in schemas/program-registry.json. Catches typos,
# drift from SKILL.md, and new program codes added without registry updates.

set -euo pipefail

REGISTRY="schemas/program-registry.json"
EVALS_GLOB="evals/*.json"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "❌ FAIL: python3/python is required to validate evals"
  exit 1
fi

if [[ ! -f "$REGISTRY" ]]; then
  echo "❌ FAIL: registry not found at $REGISTRY"
  exit 1
fi

"$PYTHON" - "$REGISTRY" $EVALS_GLOB <<'PY'
import json
import sys
from pathlib import Path

registry_path = Path(sys.argv[1])
eval_paths = [Path(p) for p in sys.argv[2:]]

registry = json.loads(registry_path.read_text())
valid_modules = set(registry["modules"])
valid_programs = set(registry["programs"])

unknown_modules = []
unknown_programs = []

def walk(node, path):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "expected_module" and isinstance(value, str):
                if value not in valid_modules:
                    unknown_modules.append((path, value))
            elif key == "expected_programs" and isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item not in valid_programs:
                        unknown_programs.append((path, item))
            walk(value, path)
    elif isinstance(node, list):
        for item in node:
            walk(item, path)

for eval_path in eval_paths:
    with open(eval_path) as fh:
        data = json.load(fh)
    walk(data, str(eval_path))

failed = False
if unknown_modules:
    failed = True
    print("❌ Unknown module IDs:")
    for path, value in unknown_modules:
        print(f"   {path}: {value!r}")
if unknown_programs:
    failed = True
    print("❌ Unknown program codes:")
    for path, value in unknown_programs:
        print(f"   {path}: {value!r}")

if failed:
    print()
    print(f"Fix: add the value to {registry_path} or correct the eval entry.")
    sys.exit(1)

print(f"✅ All modules and programs in {len(eval_paths)} eval file(s) match the registry.")
PY
