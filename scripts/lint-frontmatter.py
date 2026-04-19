#!/usr/bin/env python3
"""Lint SKILL.md YAML frontmatter.

Checks:
  1. Frontmatter is delimited by `---` and parses as YAML.
  2. Required keys are present: name, description, version, license.
  3. No duplicate top-level keys (yaml.safe_load silently drops dupes, which
     is exactly how the 4.2.3/4.0.0 version bug in this repo went unnoticed).

Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REQUIRED_KEYS = ("name", "description", "version", "license")
TOP_LEVEL_KEY = re.compile(r"^([a-z_][a-z0-9_]*)\s*:", re.MULTILINE)


def main(path: Path) -> int:
    text = path.read_text()
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        print(f"❌ {path}: no YAML frontmatter delimited by '---' at top of file")
        return 1

    frontmatter = parts[1]

    try:
        data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        print(f"❌ {path}: frontmatter is not valid YAML: {exc}")
        return 1

    if not isinstance(data, dict):
        print(f"❌ {path}: frontmatter must be a YAML mapping, got {type(data).__name__}")
        return 1

    errors: list[str] = []

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        errors.append(f"missing required keys: {', '.join(missing)}")

    seen: dict[str, int] = {}
    for match in TOP_LEVEL_KEY.finditer(frontmatter):
        key = match.group(1)
        seen[key] = seen.get(key, 0) + 1
    duplicates = sorted(k for k, count in seen.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate top-level key(s): {', '.join(duplicates)}")

    if errors:
        print(f"❌ {path}:")
        for err in errors:
            print(f"   - {err}")
        return 1

    print(f"✅ {path}: frontmatter OK (version={data['version']})")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("SKILL.md")
    sys.exit(main(target))
