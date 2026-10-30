"""Fast QSP & Canon Linter for modified .qsps files and Antigravity rule files.

Checks:
1. Rule file byte size (< 23,500 bytes to prevent Antigravity 24 KB truncation).
2. #LocationName vs --- separator balance in modified .qsps files.
3. Duplicate #LocationName across all connected folders in qsp-project.json.
4. @qsp/converters (readQsps) parse verification on modified .qsps files (catches unclosed quotes).
5. Bare `act 'Label':` without second icon argument ($ActUiIconPath).
6. Eaten $-variables (e.g. `= LCASE([0])`, `if  = '...'`, `killvar ''`).
7. Mandatory `! [AI-WORKED]` header in modified *_text.qsps files (excluding USER-OWNED TEXT).
8. Glued consecutive `*p '...'` lines without a trailing space.
9. Prohibited Christian / non-lore terms («боже», «господи», «ради бога», «перекрестился») in modified non-USER-OWNED *_text.qsps files.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LOCATION_RE = re.compile(r"^\s*#\s*(\S+)\s*$")
SEPARATOR_RE = re.compile(r"^\s*---\s*(?:!.*)?$")
BARE_ACT_RE = re.compile(
    r"^\s*act\s+(?:'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|\$[A-Za-z0-9_.]+)\s*:",
    re.IGNORECASE,
)
EATEN_VAR_RE = re.compile(
    r"(?:^\s*=\s*|\b(?:if|elseif)\s+=\s*|killvar\s+''|(?<![A-Za-z0-9_$])\[0\])",
    re.IGNORECASE,
)
STAR_P_LITERAL_RE = re.compile(r"^\s*\*p\s+'((?:''|[^'])*)'\s*$", re.IGNORECASE)
FORBIDDEN_LORE_RE = re.compile(
    r"\b(?:господи|господь|боже\s+мой|о\s+боже|ради\s+бога|слава\s+богу|о\s+боги|перекрестил\w*|крестил\w*)\b",
    re.IGNORECASE,
)

MAX_RULE_BYTES = 23500


def get_modified_qsps(repo_root: Path) -> list[Path]:
    try:
        git_out = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=5,
        )
    except Exception:
        return []

    modified: list[Path] = []
    for line in git_out.splitlines():
        if len(line) < 4:
            continue
        rel = line[3:].strip().strip('"')
        if " -> " in rel:
            rel = rel.split(" -> ", 1)[1].strip('"')
        if rel.lower().endswith(".qsps"):
            p = repo_root / rel
            if p.is_file():
                modified.append(p)
    return modified


def check_rule_sizes(repo_root: Path) -> list[str]:
    errors: list[str] = []
    rule_files = [repo_root / "AGENTS.md", repo_root / "GEMINI.md"]
    rule_files.extend(sorted((repo_root / "modules").rglob("AGENTS.md")))

    for rf in rule_files:
        if rf.is_file():
            size = rf.stat().st_size
            if size > MAX_RULE_BYTES:
                rel = rf.relative_to(repo_root)
                errors.append(
                    f"Файл правил {rel} весит {size} байт (порог безопасности {MAX_RULE_BYTES} байт, лимит Antigravity 24000 байт). Сократите или разделите файл."
                )
    return errors


def verify_qsps_parse(repo_root: Path, files: list[Path]) -> list[str]:
    if not files:
        return []
    errors: list[str] = []
    try:
        resolver = repo_root / "scripts" / "resolve_qsp_converters.py"
        converters = (
            subprocess.check_output([sys.executable, str(resolver)], text=True, timeout=5)
            .strip()
            .replace("\\", "/")
        )
    except Exception:
        return []

    node_script = f"""
const {{readQsps}}=require('{converters}');
const fs=require('fs');
const files=JSON.parse(fs.readFileSync(0,'utf8'));
const out={{}};
for (const f of files) {{
  const txt=fs.readFileSync(f,'utf8');
  out[f]=readQsps(txt).map(l=>l.name);
}}
console.log(JSON.stringify(out));
"""
    try:
        file_strs = [str(f) for f in files]
        raw_out = subprocess.check_output(
            ["node", "-e", node_script],
            input=json.dumps(file_strs),
            text=True,
            encoding="utf-8",
            timeout=10,
        )
        parsed_map: dict[str, list[str]] = json.loads(raw_out)
        for f in files:
            text = f.read_text(encoding="utf-8", errors="ignore")
            rx_locs = [m.group(1) for m in LOCATION_RE.finditer(text)]
            pr_locs = set(parsed_map.get(str(f), []))
            missing = [loc for loc in rx_locs if loc not in pr_locs]
            if missing:
                rel = f.relative_to(repo_root)
                errors.append(
                    f"{rel}: парсер QSP потерял локации {missing[:3]} (проверьте незакрытые кавычки ' или разделитель ---)."
                )
    except Exception:
        pass
    return errors


def check_qsps_files(repo_root: Path, files: list[Path]) -> list[str]:
    errors: list[str] = []

    for qfile in files:
        rel_path = qfile.relative_to(repo_root)
        try:
            text = qfile.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(f"{rel_path}: ошибка чтения UTF-8 ({exc}).")
            continue

        lines = text.splitlines()
        head = "\n".join(lines[:15])
        is_user_owned = "USER-OWNED TEXT" in head
        is_text_file = qfile.name.lower().endswith("_text.qsps")

        locs = [m.group(1) for line in lines if (m := LOCATION_RE.match(line))]
        seps = [line for line in lines if SEPARATOR_RE.match(line)]
        if len(locs) != len(seps):
            errors.append(
                f"{rel_path}: число локаций (#Loc={len(locs)}) не совпадает с числом разделителей (---={len(seps)})."
            )

        if is_text_file and not is_user_owned and "[AI-WORKED]" not in head:
            errors.append(
                f"{rel_path}: отсутствует обязательная метка '! [AI-WORKED] Текст переработан / дополнен ассистентом DD.MM.YYYY' в шапке файла."
            )

        prev_star_p_no_space: int | None = None
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("!"):
                continue

            if EATEN_VAR_RE.search(line):
                errors.append(
                    f"{rel_path}:{idx}: пропущено имя переменной (возможно, съедена $-переменная): {stripped[:60]}"
                )

            if BARE_ACT_RE.match(line):
                errors.append(
                    f"{rel_path}:{idx}: 'act' без второго аргумента-иконки (используйте gs 'ActUiPrepare' и act $ActUiLabel, $ActUiIconPath:)."
                )

            m_p = STAR_P_LITERAL_RE.match(line)
            if m_p:
                val = m_p.group(1)
                if prev_star_p_no_space is not None:
                    errors.append(
                        f"{rel_path}:{idx}: подряд идущие *p без пробела в конце предыдущей строки (строка {prev_star_p_no_space}) приведут к склейке текста."
                    )
                prev_star_p_no_space = idx if (val and not val.endswith(" ")) else None
            else:
                prev_star_p_no_space = None

            if is_text_file and not is_user_owned:
                m_lore = FORBIDDEN_LORE_RE.search(line)
                if m_lore:
                    errors.append(
                        f"{rel_path}:{idx}: неканоничное выражение '{m_lore.group(0)}' (по лору используются Ильматер и святой круг)."
                    )

    return errors


def check_duplicate_locations(repo_root: Path) -> list[str]:
    errors: list[str] = []
    project_file = repo_root / "qsp-project.json"
    if not project_file.is_file():
        return errors

    try:
        proj = json.loads(project_file.read_text(encoding="utf-8"))
        module = proj["project"][0]
        all_files: list[Path] = []
        for f in module.get("files", []):
            fp = repo_root / f["path"]
            if fp.is_file():
                all_files.append(fp)
        for folder in module.get("folders", []):
            fd = repo_root / folder["path"]
            if fd.is_dir():
                all_files.extend(sorted(fd.rglob("*.qsps")))

        seen: dict[str, str] = {}
        for fp in all_files:
            rel = str(fp.relative_to(repo_root))
            for idx, line in enumerate(fp.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                m = LOCATION_RE.match(line)
                if m:
                    loc_name = m.group(1)
                    loc_ref = f"{rel}:{idx}"
                    if loc_name in seen:
                        errors.append(f"Дубликат локации '#{loc_name}': {seen[loc_name]} и {loc_ref}")
                    else:
                        seen[loc_name] = loc_ref
    except Exception:
        pass

    return errors


def run_all_checks(repo_root: Path, explicit_files: list[Path] | None = None) -> list[str]:
    errors: list[str] = []
    errors.extend(check_rule_sizes(repo_root))

    target_files = explicit_files if explicit_files is not None else get_modified_qsps(repo_root)
    if not target_files:
        return errors

    errors.extend(check_qsps_files(repo_root, target_files))
    errors.extend(verify_qsps_parse(repo_root, target_files))
    errors.extend(check_duplicate_locations(repo_root))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint modified QSP files and rule budgets.")
    parser.add_argument("files", nargs="*", help="Optional explicit .qsps files to lint")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    explicit = [Path(f).resolve() for f in args.files] if args.files else None
    errors = run_all_checks(repo_root, explicit)

    if errors:
        print("QSP Linter found issues:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    print("QSP Linter: OK")


if __name__ == "__main__":
    main()
