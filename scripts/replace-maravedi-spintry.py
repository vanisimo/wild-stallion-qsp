#!/usr/bin/env python3
"""Replace maravedi currency strings with spintry in QSP modules."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "modules"

STATIC = [
    ("Семьдесят мараведи", "семьдесят спинтарий"),
    ("семьдесят мараведи", "семьдесят спинтарий"),
    ("десять мараведи", "десять спинтарий"),
    ("Десять мараведи", "Десять спинтарий"),
    ("Пятьдесят мараведи", "пятьдесят спинтарий"),
    ("Пятнадцать мараведи", "пятнадцать спинтарий"),
    ("пятнадцать мараведи", "пятнадцать спинтарий"),
    ("Тридцать мараведи", "тридцать спинтарий"),
    ("Пять мараведи", "5 спинтарий"),
    ("15 мараведи", "15 спинтарий"),
    ("5 мараведи", "5 спинтарий"),
    ("10 мараведи", "10 спинтарий"),
    ("25 мараведи", "25 спинтарий"),
    ("30 мараведи", "30 спинтарий"),
    ("50 мараведи", "50 спинтарий"),
    ("55 мараведи", "55 спинтарий"),
    ("65 мараведи", "65 спинтарий"),
    ("70 мараведи", "70 спинтарий"),
    ("90 мараведи", "90 спинтарий"),
    ("Не хватает мараведи", "Не хватает спинтарий"),
    ("не мараведи", "не спинтарии"),
    ("<<stolen>> мараведи", "<<stolen>> спинтарий"),
    ("<<damage>> мараведи", "<<damage>> спинтарий"),
    ("<<fine>> мараведи", "<<fine>> спинтарий"),
    ("<<TavernCityTaxTotal>> мараведи", "<<TavernCityTaxTotal>> спинтарий"),
    ("<<MayorCityTaxGate>> мараведи", "<<MayorCityTaxGate>> спинтарий"),
    ("<<MayorAudienceBribe>> мараведи", "<<MayorAudienceBribe>> спинтарий"),
    ("<<BirthCertificateMagistrateFee>> мараведи", "<<BirthCertificateMagistrateFee>> спинтарий"),
]

DYN_RE = re.compile(r"STR\(([^)]+)\) \+ ' мараведи([^']*)'")
FMT_TOKEN_RE = re.compile(
    r"' \+ \$FormatSpintry_([A-Za-z0-9_]+)([^']*)' /\*FMT:([^*]+)\*/"
)


def safe_name(var: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", var)


def transform_dynamic(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        var = match.group(1).strip()
        suffix = match.group(2)
        return f"' + $FormatSpintry_{safe_name(var)}{suffix}' /*FMT:{var}*/"

    return DYN_RE.sub(repl, text)


def apply_dynamic_blocks(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []

    for line in lines:
        pending_vars: list[str] = []
        work = line

        while True:
            match = FMT_TOKEN_RE.search(work)
            if not match:
                break
            var = match.group(3)
            suffix = match.group(2)
            placeholder = f"' + $FormatSpintry_{match.group(1)}{suffix}'"
            work = work[: match.start()] + placeholder + work[match.end() :]
            if var not in pending_vars:
                pending_vars.append(var)

        if pending_vars and "$FormatSpintry_" in work:
            indent_match = re.match(r"(\s*)", work)
            indent = indent_match.group(1) if indent_match else ""
            for var in pending_vars:
                name = safe_name(var)
                out.append(f"{indent}gs 'FormatSpintry', {var}\n")
                out.append(f"{indent}$FormatSpintry_{name} = $FormatSpintry\n")
                out.append(f"{indent}killvar '$FormatSpintry'\n")

        out.append(work)

    return "".join(out)


def main() -> None:
    changed: list[Path] = []

    for path in sorted(ROOT.rglob("*.qsps")):
        text = path.read_text(encoding="utf-8")
        if "мараведи" not in text:
            continue

        original = text
        for old, new in STATIC:
            text = text.replace(old, new)
        text = transform_dynamic(text)
        text = apply_dynamic_blocks(text)

        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed.append(path)

    print(f"Updated {len(changed)} files")
    for path in changed:
        print(path.relative_to(ROOT.parent))


if __name__ == "__main__":
    main()