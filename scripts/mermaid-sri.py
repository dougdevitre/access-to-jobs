#!/usr/bin/env python3
"""Print the import map that pins Mermaid on docs/index.html with Subresource Integrity.

The landing page imports Mermaid as an ES module from jsDelivr. An `import`
statement cannot carry an integrity attribute, so the hashes live in an
<script type="importmap"> "integrity" block: one entry for the entry module and
one for every module that drawing a flowchart loads. jsDelivr serves the npm
package files byte for byte, so the hashes are taken from the npm tarball,
after checking the tarball against the registry's own sha512.

Usage: python3 scripts/mermaid-sri.py 10.9.8
Paste the output over the importmap in docs/index.html and change the version
in the `import` URL to match; scripts/lint-third-party.py checks they agree.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import posixpath
import re
import sys
import tarfile
import urllib.request

REGISTRY = "https://registry.npmjs.org/mermaid"
CDN = "https://cdn.jsdelivr.net/npm/mermaid@{version}/{path}"
ENTRY = "dist/mermaid.esm.min.mjs"
DIAGRAMS = ("flowDiagram-v2-",)  # the diagram types the page draws (flowchart)
STATIC = re.compile(r"""(?:\bfrom|\bimport)\s*["'](\./[^"']+)["']""")
DYNAMIC = re.compile(r"""\bimport\(\s*["'](\./[^"']+)["']\s*\)""")


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        print("usage: python3 scripts/mermaid-sri.py <exact version, e.g. 10.9.8>", file=sys.stderr)
        return 1
    version = sys.argv[1]
    meta = json.loads(fetch(f"{REGISTRY}/{version}"))["dist"]
    tarball = fetch(meta["tarball"])
    algo, digest = meta["integrity"].split("-", 1)
    if base64.b64encode(hashlib.new(algo, tarball).digest()).decode() != digest:
        print("❌ tarball does not match the registry integrity", file=sys.stderr)
        return 1
    with tarfile.open(fileobj=io.BytesIO(tarball)) as tar:
        files = {m.name.removeprefix("package/"): tar.extractfile(m).read()
                 for m in tar.getmembers() if m.isfile()}

    def resolve(base: str, rel: str) -> str:
        return posixpath.normpath(posixpath.join(posixpath.dirname(base), rel))

    def closure(start: str, found: list[str]) -> None:
        if start in found:
            return
        found.append(start)
        for rel in STATIC.findall(files[start].decode()):
            closure(resolve(start, rel), found)

    needed: list[str] = []
    closure(ENTRY, needed)
    for path in list(needed):
        for rel in DYNAMIC.findall(files[path].decode()):
            if posixpath.basename(rel).startswith(DIAGRAMS):
                closure(resolve(path, rel), needed)

    integrity = {
        CDN.format(version=version, path=path):
            "sha384-" + base64.b64encode(hashlib.sha384(files[path]).digest()).decode()
        for path in needed
    }
    print(json.dumps({"integrity": integrity}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
