# -*- coding: utf-8 -*-
"""Regenerate project_tree.txt (UTF-8)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def walk(dir_path: Path, prefix: str = "", max_depth: int = 8, depth: int = 0):
    lines = []
    if depth > max_depth:
        return lines
    try:
        items = sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        return lines

    ignore = {
        ".git",
        "node_modules",
        "PIc",
        "PIC",
        "mcps",
        "terminals",
        "agent-tools",
        ".build",
        "tools",
    }
    items = [
        i
        for i in items
        if i.name not in ignore and not i.name.startswith(".aider")
    ]

    for idx, item in enumerate(items):
        last = idx == len(items) - 1
        branch = "└── " if last else "├── "
        add = "    " if last else "│   "

        if item.is_dir():
            nq = sum(1 for _ in item.rglob("*.qsps"))
            label = f"{item.name}/  ({nq} qsps)" if nq else f"{item.name}/"
            lines.append(prefix + branch + label)

            if item.name in {"images", "docs", "scripts"}:
                subs = sorted(
                    [p for p in item.iterdir() if p.is_dir()],
                    key=lambda p: p.name.lower(),
                )
                for j, sub in enumerate(subs):
                    last2 = j == len(subs) - 1
                    b2 = "└── " if last2 else "├── "
                    if item.name == "images":
                        nf = sum(1 for x in sub.rglob("*") if x.is_file())
                        lines.append(
                            prefix + add + b2 + f"{sub.name}/  (~{nf} files)"
                        )
                    else:
                        lines.append(prefix + add + b2 + f"{sub.name}/")
                if item.name == "docs":
                    mds = sorted(p.name for p in item.glob("*.md"))
                    for j, name in enumerate(mds):
                        last3 = j == len(mds) - 1
                        b3 = "└── " if last3 else "├── "
                        lines.append(prefix + add + b3 + name)
                continue

            lines.extend(walk(item, prefix + add, max_depth, depth + 1))
        else:
            keep_ext = {
                ".qsps",
                ".md",
                ".json",
                ".bat",
                ".txt",
                ".ps1",
                ".py",
            }
            if item.suffix.lower() in keep_ext or item.name in {
                "TraKtir.qsps",
                "game.qsp",
                "AGENTS.md",
            }:
                if item.name in {
                    "qsp-project-workspace.json",
                    "qsp-project.sublime-workspace",
                    "game.txt",
                }:
                    continue
                lines.append(prefix + branch + item.name)
    return lines


def main():
    out = [
        "Wild Stallion QSP — project tree",
        "Generated for layout orientation. Active build: modules/* via qsp-project.json",
        "Archive is NOT compiled.",
        "",
        "E:/traktir",
    ]
    root_files = [
        "AGENTS.md",
        "README.md",
        "TraKtir.qsps",
        "qsp-project.json",
        "project_tree.txt",
        "run_game.bat",
    ]
    dirs = ["modules", "archive", "docs", "images", "scripts"]
    items = [ROOT / n for n in root_files if (ROOT / n).exists()]
    items += [ROOT / n for n in dirs if (ROOT / n).exists()]

    for idx, item in enumerate(items):
        last = idx == len(items) - 1
        branch = "└── " if last else "├── "
        pref = "    " if last else "│   "
        if item.is_file():
            out.append(branch + item.name)
        else:
            nq = (
                sum(1 for _ in item.rglob("*.qsps"))
                if item.name in {"modules", "archive"}
                else 0
            )
            label = f"{item.name}/  ({nq} qsps)" if nq else f"{item.name}/"
            out.append(branch + label)
            out.extend(
                walk(
                    item,
                    pref,
                    max_depth=7 if item.name == "modules" else 5,
                )
            )

    (ROOT / "project_tree.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote project_tree.txt ({len(out)} lines)")


if __name__ == "__main__":
    main()
