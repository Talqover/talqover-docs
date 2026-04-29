#!/usr/bin/env python3
"""
Verify whitelabel PDFs have 0 references to talqover/talkover.

Usage:
  python3 editorial/rebrand_check.py

Exits 1 if any client PDF has refs.
"""

from __future__ import annotations
import glob
import re
import sys

from pypdf import PdfReader


def main() -> int:
    fail = False
    pdfs = sorted(glob.glob("dist/*.pdf"))
    if not pdfs:
        print("no PDFs in dist/. Run `make pdfs` first.")
        return 1

    for f in pdfs:
        # Talkover default is allowed to mention itself.
        if "talkover-api-docs" in f or "/talkover/" in f.replace("\\", "/"):
            continue
        try:
            r = PdfReader(f)
            full = "".join(p.extract_text() + "\n" for p in r.pages)
        except Exception as e:
            print(f"  {f}: ERROR reading PDF — {e}")
            fail = True
            continue

        hits = re.findall(r"talq\w*|talkover\w*", full, re.IGNORECASE)
        if hits:
            print(f"  {f}: FAIL — {len(hits)} ref(s) — examples: {hits[:3]}")
            fail = True
        else:
            print(f"  {f}: OK")

    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
