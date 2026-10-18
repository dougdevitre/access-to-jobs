#!/usr/bin/env python3
"""Build access-to-jobs.skill, the package Claude actually loads.

The .skill file is a zip of the skill sources. Claude reads the package, not
the repo, so a source edit that is not followed by a rebuild never reaches
users. This script builds the package deterministically: files are added in
sorted order with a fixed timestamp and fixed permissions, so building the
same sources twice gives byte-identical output with the same Python/zlib.

Usage:
  python3 scripts/build-skill.py            # write access-to-jobs.skill
  python3 scripts/build-skill.py OUT.skill  # write somewhere else
  python3 scripts/build-skill.py --check    # fail if the committed package
                                            # is out of date with the sources

--check builds into a temp dir and compares the extracted file list and file
contents with the committed package (not the zip bytes, which can differ
between zlib versions). Exits 0 when they match, 1 when they don't.
"""
from __future__ import annotations

import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACKAGE = "access-to-jobs.skill"

# What goes in the package, in this order. Directories are walked recursively.
FILES = [
    "SKILL.md",
    "DISCLAIMER.md",  # SKILL.md points readers to it
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "DEPLOYMENT.md",
    "CHANGELOG.md",
    "SECURITY.md",
]
DIRS = [
    "references",
    "templates",
    "schemas",
    "assets",
    "slash-commands",
    "guides",
    "evals",
    "states",
]
# Only the state scaffolder is useful inside the skill; the other scripts are
# repo tooling (CI lints, this builder).
EXTRA = ["scripts/deploy-state.sh"]

SKIP_NAMES = {".DS_Store", "Thumbs.db"}
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def entries() -> list[str]:
    """Return package paths in build order; directories end with '/'."""
    out: list[str] = list(FILES)
    for top in DIRS:
        root = REPO / top
        if not root.is_dir():
            sys.exit(f"build-skill: missing directory {top}/")
        out.append(f"{top}/")
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            rel = Path(dirpath).relative_to(REPO).as_posix()
            if rel != top:
                out.append(f"{rel}/")
            for name in sorted(filenames):
                if name in SKIP_NAMES or name.startswith(".") or name.endswith(("~", ".swp")):
                    continue
                out.append(f"{rel}/{name}")
    if EXTRA:
        out.append("scripts/")
        out.extend(EXTRA)
    for path in out:
        if not path.endswith("/") and not (REPO / path).is_file():
            sys.exit(f"build-skill: missing file {path}")
    return out


def build(dest: Path) -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for path in entries():
            info = zipfile.ZipInfo(path, date_time=FIXED_TIME)
            info.create_system = 3  # Unix, so the permissions below apply
            if path.endswith("/"):
                info.external_attr = (0o40755 << 16) | 0x10
                zf.writestr(info, b"")
                continue
            mode = 0o755 if path.endswith(".sh") else 0o644
            info.external_attr = (0o100000 | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, (REPO / path).read_bytes(), compresslevel=9)
    dest.write_bytes(buf.getvalue())


def contents(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as zf:
        return {i.filename: zf.read(i) for i in zf.infolist() if not i.is_dir()}


def check() -> int:
    committed = REPO / PACKAGE
    if not committed.is_file():
        print(f"::error::{PACKAGE} is missing. Run scripts/build-skill.sh and commit it.")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / PACKAGE
        build(fresh)
        want, have = contents(fresh), contents(committed)
    missing = sorted(set(want) - set(have))
    extra = sorted(set(have) - set(want))
    changed = sorted(p for p in set(want) & set(have) if want[p] != have[p])
    if not (missing or extra or changed):
        print(f"OK: {PACKAGE} matches the sources ({len(want)} files).")
        return 0
    for p in missing:
        print(f"  missing from package: {p}")
    for p in extra:
        print(f"  in package but not in sources: {p}")
    for p in changed:
        print(f"  out of date in package: {p}")
    total = len(missing) + len(extra) + len(changed)
    print(
        f"::error::{PACKAGE} is out of date — run scripts/build-skill.sh and commit it. "
        f"({total} file(s) differ: {len(missing)} missing, {len(extra)} extra, {len(changed)} changed)"
    )
    return 1


def main(argv: list[str]) -> int:
    if argv[:1] == ["--check"]:
        return check()
    out = Path(argv[0]) if argv else REPO / PACKAGE
    if not out.is_absolute():
        out = REPO / out
    build(out)
    print(f"Built {out} ({len(contents(out))} files, {out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
