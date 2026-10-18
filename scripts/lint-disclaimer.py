#!/usr/bin/env python3
"""Check the in-app disclaimer on every published page.

GitHub Pages serves docs/, so every HTML page under docs/ must:
  1. Carry the canonical short notice, with 911 and 988 as tel: links and a
     link to the full DISCLAIMER.md.
  2. Show it before the page content (ahead of the first <section>), so the
     crisis numbers are visible without scrolling or clicking.
  3. If the page takes input (form, input, select, textarea), also carry the
     one-time acknowledgment dialog under the versioned storage key.

Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TITLE = "Access to Jobs"
NOTICE = (
    f"Educational information only. {TITLE} is not legal, medical, mental "
    "health, financial or safety advice, and using it creates no professional "
    "relationship. In danger now? Call 911. For crisis support, call or text "
    "988. Confirm anything important with the official source or a licensed "
    "professional."
)
FULL_LINK = "https://github.com/dougdevitre/access-to-jobs/blob/main/DISCLAIMER.md"
INPUT = re.compile(r"<(form|input|select|textarea)\b", re.IGNORECASE)


def check(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html))
    notice = html.find('class="atd-notice')
    first_section = html.find("<section")
    checks = {
        "short notice text": NOTICE in text,
        "911 as a tel: link": re.search(r'<a[^>]*href="tel:911"[^>]*>911</a>', html),
        "988 as a tel: link": re.search(r'<a[^>]*href="tel:988"[^>]*>988</a>', html),
        "link to the full disclaimer": FULL_LINK in html,
        "notice ahead of the page content": notice > -1
        and (first_section == -1 or notice < first_section),
    }
    if INPUT.search(html):
        checks["acknowledgment dialog"] = "<dialog" in html and ">I understand</button>" in html
        checks["versioned storage key"] = '"disclaimer-ack-v1"' in html
    return [f"{path}: missing {name}" for name, ok in checks.items() if not ok]


def main() -> int:
    pages = sorted(Path("docs").rglob("*.html"))
    if not pages:
        print("❌ no published pages found under docs/")
        return 1
    errors = [e for page in pages for e in check(page)]
    for e in errors:
        print(f"❌ {e}")
    if errors:
        return 1
    print(f"✅ Disclaimer present on all {len(pages)} published page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
