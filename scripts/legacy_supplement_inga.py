#!/usr/bin/env python3
"""Supplement: Inga/guard snippets not in named locations."""

import re
from pathlib import Path

LEGACY = Path(r"E:\Games\Albedo\Traktir Wild Stallion 0.05\traktr_old.txt")
OUT = Path(__file__).resolve().parent.parent / "docs" / "legacy-text-extracts" / "inga"

text = LEGACY.read_text(encoding="utf-16")
lines = text.splitlines()

guard_lines = []
for i, line in enumerate(lines, 1):
    low = line.lower()
    if "стражник" in low or "грюн" in low:
        guard_lines.append(f"L{i}: {line}")

lucas_lines = []
for i, line in enumerate(lines, 1):
    if "лукас" in line.lower() and ("*p" in line or "*pl" in line or line.strip().startswith("'")):
        if len(line.strip()) > 30:
            lucas_lines.append(f"L{i}: {line.strip()[:300]}")

out = [
    "# Inga / guard / Lucas — фрагменты из монолита",
    "",
    "Отдельной локации `IngaGuard*` в legacy **нет**. Квест стражника в `modules/` — **новый код**.",
    "Ниже — строки со «стражник» и реплики Лукаса для лора.",
    "",
    "## Стражник (все упоминания, первые 40)",
    "",
]
out.extend(guard_lines[:40])
out += ["", "## Лукас (нарратив, первые 25)", ""]
out.extend(lucas_lines[:25])

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "inga_guard_snippets.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote {OUT / 'inga_guard_snippets.md'}, guard={len(guard_lines)}, lucas={len(lucas_lines)}")