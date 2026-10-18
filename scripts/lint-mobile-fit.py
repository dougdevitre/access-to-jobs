#!/usr/bin/env python3
"""Check that every published page can fit a 320px phone screen.

GitHub Pages serves docs/. A page that is wider than the screen scrolls
sideways, which hides content and the disclaimer's edges on phones. This
guards the causes we have hit:

  1. Every <pre> must wrap or contain its own overflow. A <pre> keeps long
     lines on one line, so unwrapped text pushes the whole page wider. The
     Mermaid diagrams are <pre class="mermaid">: until Mermaid draws them
     (slow network, blocked CDN, no JavaScript) their source text is shown,
     and it made the landing page 473px wide at 375px.
     Accepted: white-space pre-wrap / pre-line / break-spaces / normal, or
     overflow(-x) auto / scroll / hidden, set by a <style> rule for `pre`,
     `.class` or `pre.class`, by an inline style, or by the matching
     Tailwind class on the element.
  2. No fixed width or min-width above 320px, in CSS, inline styles or
     Tailwind arbitrary values such as w-[480px].

Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_PX = 320
WRAPS = r"white-space\s*:\s*(pre-wrap|pre-line|break-spaces|normal)"
CONTAINS = r"overflow(-x)?\s*:\s*(auto|scroll|hidden|clip)"
FITS_DECL = re.compile(f"{WRAPS}|{CONTAINS}", re.IGNORECASE)
FITS_CLASSES = {
    "whitespace-pre-wrap", "whitespace-pre-line", "whitespace-break-spaces",
    "whitespace-normal", "overflow-auto", "overflow-x-auto", "overflow-scroll",
    "overflow-x-scroll", "overflow-hidden", "overflow-x-hidden", "overflow-clip",
    "overflow-x-clip",
}
STYLE_BLOCK = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
PRE_TAG = re.compile(r"<pre\b([^>]*)>", re.IGNORECASE)
ATTR = r"""\b{}\s*=\s*["']([^"']*)["']"""
FIXED_WIDTH = re.compile(r"(?<![\w-])(?:min-)?width\s*:\s*(\d+(?:\.\d+)?)px", re.IGNORECASE)
TW_WIDTH = re.compile(r"(?<![\w-])(?:min-)?w-\[(\d+(?:\.\d+)?)px\]")


def fitting_selectors(css: str) -> set[str]:
    """Simple selectors (`pre`, `.x`, `pre.x`) whose rule wraps or contains overflow."""
    found = set()
    for selectors, body in RULE.findall(re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)):
        if FITS_DECL.search(body):
            found.update(s.strip() for s in selectors.split(","))
    return found


def blank(match: re.Match) -> str:
    """Drop a span's text but keep its newlines, so line numbers stay right."""
    return "\n" * match.group(0).count("\n")


def check(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    css = "\n".join(STYLE_BLOCK.findall(html))
    selectors = fitting_selectors(css)
    markup = re.sub(r"<!--.*?-->|<(style|script)\b.*?</\1>", blank, html,
                    flags=re.IGNORECASE | re.DOTALL)
    errors = []

    for n, match in enumerate(PRE_TAG.finditer(markup), 1):
        attrs = match.group(1)
        classes = (re.search(ATTR.format("class"), attrs) or [None, ""])[1].split()
        style = (re.search(ATTR.format("style"), attrs) or [None, ""])[1]
        ok = (
            "pre" in selectors
            or any(f".{c}" in selectors or f"pre.{c}" in selectors for c in classes)
            or FITS_DECL.search(style)
            or FITS_CLASSES.intersection(classes)
        )
        if not ok:
            label = f'<pre class="{" ".join(classes)}">' if classes else "<pre>"
            line = markup.count("\n", 0, match.start()) + 1
            errors.append(f"{path}:{line}: {label} #{n} neither wraps nor contains its overflow")

    for pattern, kind in ((FIXED_WIDTH, "CSS width"), (TW_WIDTH, "Tailwind width")):
        for match in pattern.finditer(html):
            if float(match.group(1)) > MAX_PX:
                line = html.count("\n", 0, match.start()) + 1
                errors.append(f"{path}:{line}: fixed {kind} {match.group(0)!r} is wider than {MAX_PX}px")
    return errors


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
    print(f"✅ No page content wider than {MAX_PX}px on all {len(pages)} published page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
