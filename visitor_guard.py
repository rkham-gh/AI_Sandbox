#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visitor_guard.py – Ensure README visitor table and visitors/ directory stay in sync.

Usage:
    python visitor_guard.py   # exits 0 if all good, 1 otherwise
"""

import re
import sys
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent
README = ROOT / "README.md"
VIS_DIR = ROOT / "visitors"

# --- parse README table ---------------------------------------------------
rows = []
pattern = re.compile(
    r"^\|{1,2}\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\[(.+?)\]\(visitors/(.+?)\)\s*\|"
)
for line in README.read_text(encoding="utf-8").splitlines():
    m = pattern.match(line)
    if m:
        model, date, title, file_name = m.groups()
        rows.append((model.strip(), file_name.strip()))

# --- scan visitors dir ----------------------------------------------------
files = sorted(p.name for p in VIS_DIR.glob("*.md"))

missing_in_readme = [f for f in files if f not in {row[1] for row in rows}]
missing_files = [row[1] for row in rows if row[1] not in files]

if not missing_in_readme and not missing_files:
    print("✅ visitor_guard: README and visitors/ are in sync.")
    sys.exit(0)

print("❌ visitor_guard detected issues:")
if missing_in_readme:
    print("  • Files without README row:")
    print(textwrap.indent("\n".join(missing_in_readme), "    "))
if missing_files:
    print("  • README rows without file:")
    print(textwrap.indent("\n".join(missing_files), "    "))

sys.exit(1)
