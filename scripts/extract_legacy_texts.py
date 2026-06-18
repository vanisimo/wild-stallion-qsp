#!/usr/bin/env python3
"""Extract QSP location sections from legacy traktr_old.txt (UTF-16) into docs/legacy-text-extracts/."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LEGACY_PATH = Path(r"E:\Games\Albedo\Traktir Wild Stallion 0.05\traktr_old.txt")
OUT_ROOT = Path(__file__).resolve().parent.parent / "docs" / "legacy-text-extracts"

# PR-I intimacy bundle: full source per location
EXTRACT_LOCATIONS: dict[str, list[str]] = {
    "becky": [
        "InitBecky",
        "IntBeckyTalk",
        "IntBeckyDance",
        "BeckyInviteHome",
        "BeckyHomeFront",
        "BeckyHome",
        "IntBeckyGuest",
        "IntBeckySex",
        "BeckyLoversInStore",
        "IntBeckyDressChange",
        "BeckyQuestInit",
        "IntBeckyTalkSherwood",
    ],
    "eddie": [
        "IntEddieTalk",
        "BeckyEddieJoinFirst",
        "IntEddieBeckySex",
        "GeorgettBeckyVisit",
    ],
    "becky_church": [
        "IntBeckyAfterCermon",
        "ChurchAfterCermon",
    ],
    "amanda": [
        "InitAmanda",
        "IntAmandaTalk",
        "IntAmandaDance",
        "IntAmandaDressChange",
        "IntAmandaSex",
        "AmandaSexDanceStreet",
        "AmandaLoverSex",
        "AmandaLegareDanceSequence",
        "AfterDanceSexLegare",
        "AfterDanceLegare",
        "TavernAmandaRoom",
        "AmandaAtHomeCode",
    ],
    "melissa": [
        "InitMelissa",
        "IntMelissaTalk",
        "IntMelissaDressChange",
    ],
    "sandra": [
        "InitSandra",
        "IntSandraTalk",
        "IntSandraDressChange",
    ],
    "inga": [
        "InitInga",
    ],
    "clarissa": [
        "IntAlberTalk",
    ],
    "cut_reference": [
        "AmandaAtGloryHole",
        "SexProstTavern",
    ],
}

STATUS: dict[str, str] = {
    "GeorgettBeckyVisit": "CUT — оргия за столом, не в v1",
    "IntBeckyTalkSherwood": "CUT — Шервуд, опционально позже",
    "IntEddieBeckySex": "CUT menu — только narrative 2–3 шага",
    "AmandaAtGloryHole": "CUT",
    "SexProstTavern": "CUT — порт вместо трактира",
    "AmandaSexDanceStreet": "ADAPT — заменено amanda_dark_alley event",
    "IntBeckySex": "ADAPT — SexSceneStart",
    "ChurchAfterCermon": "ADAPT — разбить на church_spy_*",
    "IntBeckyAfterCermon": "TAKE — укороченно, ongoing Бекки",
    "BeckyEddieJoinFirst": "TAKE — упростить до 2–3 шагов",
    "IntEddieTalk": "TAKE",
    "IntBeckyTalk": "TAKE — слить в talk_with_becky",
    "IntBeckyDance": "TAKE — becky_dance.qsps",
    "BeckyInviteHome": "TAKE",
    "BeckyHomeFront": "TAKE — только Инга+Лукас",
    "BeckyHome": "TAKE",
    "IntBeckyGuest": "TAKE — ужин укороченный",
    "BeckyLoversInStore": "ADAPT — моряки DP",
    "IntAmandaDance": "PARTIAL — уже amanda_dance.qsps",
    "IntMelissaDressChange": "TAKE — самопокупка д.35",
    "IntAmandaDressChange": "TAKE — самопокупка д.28",
}


def parse_sections(text: str) -> dict[str, str]:
    start_re = re.compile(r"^Название локации: (\S+)\s*$", re.M)
    end_re = re.compile(r"^------------ Конец локации: (\S+) ------------\s*$", re.M)

    starts = [(m.start(), m.group(1)) for m in start_re.finditer(text)]
    ends = {m.group(1): m.start() for m in end_re.finditer(text)}

    sections: dict[str, str] = {}
    for i, (pos, name) in enumerate(starts):
        end_pos = ends.get(name)
        if end_pos is None:
            next_pos = starts[i + 1][0] if i + 1 < len(starts) else len(text)
            body = text[pos:next_pos]
        else:
            end_line = text.find("\n", end_pos)
            if end_line == -1:
                end_line = len(text)
            else:
                end_line += 1
            body = text[pos:end_line]
        sections[name] = body.strip() + "\n"
    return sections


def extract_narrative(source: str) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()

    patterns = [
        re.compile(r"^\s*\*p\s+'(.*)'\s*$", re.M),
        re.compile(r"^\s*\*pl\s+'(.*)'\s*$", re.M),
        re.compile(r"^\s*\*p\s+\"(.*)\"\s*$", re.M),
        re.compile(r"^\s*\*pl\s+\"(.*)\"\s*$", re.M),
        re.compile(r"GS\s+'Menu\.Add','[^']+','([^']{8,})','", re.I),
        re.compile(r"gs\s+'Menu\.Add','[^']+','([^']{8,})','", re.I),
        re.compile(r"^'([^']{20,})'$", re.M),
        re.compile(r"^\"([^\"]{20,})\"$", re.M),
    ]

    for pat in patterns:
        for m in pat.finditer(source):
            s = m.group(1).strip()
            if len(s) < 12 or s in seen:
                continue
            if any(x in s for x in ("Menu.", "gs ", "GS ", "gt ", "IIF(", "BeckyVar")):
                continue
            seen.add(s)
            lines.append(s)
    return lines


def write_bundle(sections: dict[str, str]) -> tuple[int, list[str]]:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    missing: list[str] = []
    written = 0

    index_lines = [
        "# Legacy text extracts (`traktr_old.txt`)",
        "",
        f"**Источник:** `{LEGACY_PATH}`",
        f"**Кодировка:** UTF-16 LE",
        "",
        "Полные фрагменты локаций для PR-I. Статус переноса — см. `design-character-intimacy-arc.md` §Сверка.",
        "",
        "| Папка | Локации |",
        "|-------|---------|",
    ]

    for folder, names in EXTRACT_LOCATIONS.items():
        folder_path = OUT_ROOT / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        index_lines.append(f"| `{folder}/` | {', '.join(names)} |")

        for name in names:
            body = sections.get(name)
            if not body:
                missing.append(name)
                continue

            (folder_path / f"{name}.legacy.txt").write_text(body, encoding="utf-8")

            narrative = extract_narrative(body)
            nar_path = folder_path / f"{name}.narrative.md"
            nar_lines = [f"# {name}", ""]
            status = STATUS.get(name)
            if status:
                nar_lines += [f"**Статус:** {status}", ""]
            nar_lines.append("## Тексты (выжимка)")
            nar_lines.append("")
            if narrative:
                for n in narrative:
                    nar_lines.append(f"- {n}")
            else:
                nar_lines.append("_(автоматическая выжимка пуста — смотри `.legacy.txt`)_")
            nar_lines.append("")
            nar_path.write_text("\n".join(nar_lines), encoding="utf-8")
            written += 1

    index_lines += [
        "",
        "## Статусы (ключевые)",
        "",
        "| Локация | Решение |",
        "|---------|---------|",
    ]
    for name in sorted(STATUS):
        index_lines.append(f"| `{name}` | {STATUS[name]} |")

    if missing:
        index_lines += ["", "## Не найдено в монолите", ""]
        for m in missing:
            index_lines.append(f"- `{m}`")

    (OUT_ROOT / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return written, missing


def main() -> int:
    if not LEGACY_PATH.is_file():
        print(f"ERROR: legacy file not found: {LEGACY_PATH}", file=sys.stderr)
        return 1

    text = LEGACY_PATH.read_text(encoding="utf-16")
    sections = parse_sections(text)
    print(f"Parsed {len(sections)} locations from monolith")

    written, missing = write_bundle(sections)
    print(f"Wrote {written} extracts to {OUT_ROOT}")
    if missing:
        print(f"Missing ({len(missing)}): {', '.join(missing)}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())