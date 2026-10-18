#!/usr/bin/env python3
"""Check that packages loaded from public CDNs are pinned and integrity-checked.

GitHub Pages serves docs/. Code fetched from jsDelivr or unpkg runs with the
page's full trust, so every published page must:
  1. Pin an exact version (pkg@1.2.3), never a range such as mermaid@10 that
     silently moves to new releases.
  2. Give every classic <script src> from those CDNs an integrity attribute
     and crossorigin.
  3. List every ES module it imports from those CDNs in an import map
     "integrity" block (an import statement cannot carry the attribute), and
     keep those entries on the same version as the import.
scripts/mermaid-sri.py regenerates the Mermaid import map after a bump.

Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CDN_URL = re.compile(
    r"https://(?:cdn\.jsdelivr\.net/npm|unpkg\.com)/((?:@[\w.-]+/)?[\w.-]+)@([^/\"'\s]+)/?[^\"'\s)]*")
EXACT = re.compile(r"\d+\.\d+\.\d+(?:-[\w.]+)?")
SCRIPT = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.IGNORECASE | re.DOTALL)
ATTR = r"""\b{}(?:\s*=\s*["']([^"']*)["'])?"""
IMPORT = re.compile(r"""\b(?:from|import)\s*\(?\s*["'](https://[^"']+)["']""")
HASH = re.compile(r"sha(256|384|512)-[A-Za-z0-9+/]+=*")


def check(path: Path) -> list[str]:
    html = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    errors = []

    for url, (pkg, version) in ((m.group(0), m.groups()) for m in CDN_URL.finditer(html)):
        if not EXACT.fullmatch(version):
            errors.append(f"{path}: {pkg}@{version} is not an exact version ({url})")

    integrity: dict[str, str] = {}
    for attrs, body in SCRIPT.findall(html):
        if re.search(r"""type\s*=\s*["']importmap["']""", attrs):
            try:
                integrity.update(json.loads(body).get("integrity", {}))
            except json.JSONDecodeError as e:
                errors.append(f"{path}: import map is not valid JSON ({e})")

    for attrs, body in SCRIPT.findall(html):
        src = re.search(ATTR.format("src"), attrs)
        if src and src[1] and CDN_URL.match(src[1]):
            if not (re.search(ATTR.format("integrity"), attrs) or [None, ""])[1]:
                errors.append(f"{path}: <script src={src[1]}> has no integrity attribute")
            if not re.search(ATTR.format("crossorigin"), attrs):
                errors.append(f"{path}: <script src={src[1]}> has no crossorigin attribute")
        if re.search(r"""type\s*=\s*["']module["']""", attrs):
            for url in IMPORT.findall(body):
                match = CDN_URL.match(url)
                if not match:
                    continue
                if not HASH.fullmatch(integrity.get(url, "")):
                    errors.append(f"{path}: module {url} has no sha256/384/512 hash in an import map")
                pkg, version = match.groups()
                for listed in integrity:
                    other = CDN_URL.match(listed)
                    if other and other[1] == pkg and other[2] != version:
                        errors.append(f"{path}: import map lists {pkg}@{other[2]} but the page imports {pkg}@{version}")
    for url, value in integrity.items():
        if not HASH.fullmatch(value):
            errors.append(f"{path}: import map integrity for {url} is not a sha256/384/512 hash")
    return errors


def main() -> int:
    pages = sorted(Path("docs").rglob("*.html"))
    if not pages:
        print("❌ no published pages found under docs/")
        return 1
    errors = [e for page in pages for e in check(page)]
    for e in dict.fromkeys(errors):
        print(f"❌ {e}")
    if errors:
        return 1
    print(f"✅ CDN packages pinned and integrity-checked on all {len(pages)} published page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
