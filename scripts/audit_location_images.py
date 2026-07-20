# -*- coding: utf-8 -*-
"""
Location image audit for Traktir.

Resolves real ShowImage / ShowLocationTimeImage / ShowLocationImage / ShowImagePath
calls the same way QSP legacy map does, and asserts files exist (>1KB).

Does NOT hardcode a tiny critical list only — scans modules/**/*.qsps.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(r"D:\Traktir")
MOD = ROOT / "modules"
SCRATCH = Path(
    os.environ.get(
        "TRAKTIR_AUDIT_OUT",
        str(Path(__file__).resolve().parent.parent / ".build" / "image-audit"),
    )
)
SCRATCH.mkdir(parents=True, exist_ok=True)

TIMES = ("morning", "day", "evening", "night")
EXTS = (".png", ".jpg", ".jpeg", ".webp")

# Smart ShowImage first-arg types (not legacy location map)
SMART_TYPES = {
    "portrait",
    "location",
    "dance",
    "event",
    "sex",
    "scene",
    "common",
}

# First-arg values that remap when second arg is portraits/dance/group — handled in scan
# Residual non-location (sex/dance/event libraries) are still listed but can be NOTED.

pat_time = re.compile(r"ShowLocationTimeImage['\"],\s*['\"]([^'\"]+)['\"]")
pat_path = re.compile(r"ShowImagePath['\"],\s*['\"]([^'\"]+)['\"]")
pat_loc_img = re.compile(r"ShowLocationImage['\"],\s*['\"]([^'\"]+)['\"]")
# 4-arg legacy: type, cat, action, pose
pat_legacy4 = re.compile(
    r"ShowImage['\"],\s*['\"]([a-zA-Z0-9_]+)['\"],\s*['\"]([a-zA-Z0-9_/]+)['\"],\s*['\"]([a-zA-Z0-9_]+)['\"],\s*['\"]([a-zA-Z0-9_]+)['\"]"
)
# 3-arg legacy: type, cat, action  (pose empty)
pat_legacy3 = re.compile(
    r"ShowImage['\"],\s*['\"]([a-zA-Z0-9_]+)['\"],\s*['\"]([a-zA-Z0-9_/]+)['\"],\s*['\"]([a-zA-Z0-9_]+)['\"]\s*(?:,|\))"
)


def exists_any(base: Path) -> Path | None:
    for e in EXTS:
        p = Path(str(base) + e)
        if p.is_file() and p.stat().st_size > 1024:
            return p
    if base.is_file() and base.stat().st_size > 1024:
        return base
    return None


def md5(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def legacy_resolve(typ: str, cat: str, action: str, pose: str) -> str | None:
    """Mirror #ShowImageLegacyLocationMap → base path without extension."""
    typ = typ.lower()
    cat = cat.lower()
    action = action.lower()
    pose = (pose or "").lower()

    if typ in SMART_TYPES:
        return None

    # Remaps from show_image.qsps
    if cat == "portraits":
        return None  # becomes portrait type
    if cat == "dance":
        return None  # becomes dance type under images/dance
    if action == "group":
        return None  # sex

    legacy_file = action
    if pose and pose != "normal":
        legacy_file = action + "_" + pose

    # images/locations/{typ}/{cat}/{legacy_file}
    return f"images/locations/{typ}/{cat}/{legacy_file}"


def is_location_scope(path: str) -> bool:
    return path.startswith("images/locations/") or path.startswith("images/items/")


missing: list[str] = []
ok: list[str] = []
resolved_paths: set[str] = set()

time_folders: set[str] = set()
show_paths: set[str] = set()
loc_ids: set[str] = set()
legacy_calls: list[tuple[str, str, str, str, str]] = []  # file, typ, cat, act, pose

for qsps in MOD.rglob("*.qsps"):
    text = qsps.read_text(encoding="utf-8", errors="replace")
    rel = str(qsps.relative_to(ROOT)).replace("\\", "/")

    for m in pat_time.finditer(text):
        time_folders.add(m.group(1).replace("\\", "/"))

    for m in pat_path.finditer(text):
        show_paths.add(m.group(1).replace("\\", "/"))

    for m in pat_loc_img.finditer(text):
        loc_ids.add(m.group(1).replace("\\", "/"))

    # Prefer 4-arg first; track spans to avoid double-counting 3-arg of same call
    used_spans: set[tuple[int, int]] = set()
    for m in pat_legacy4.finditer(text):
        used_spans.add((m.start(), m.end()))
        legacy_calls.append((rel, m.group(1), m.group(2), m.group(3), m.group(4)))

    for m in pat_legacy3.finditer(text):
        span = (m.start(), m.end())
        # skip if this match is nested inside a 4-arg match
        if any(s <= m.start() and m.end() <= e for s, e in used_spans):
            continue
        # if next non-space after match starts a 4th string arg, skip (handled by 4-arg)
        after = text[m.end() - 1 : m.end() + 40]
        if re.match(r",\s*['\"]", after):
            continue
        legacy_calls.append((rel, m.group(1), m.group(2), m.group(3), ""))


# --- TIME folders ---
for folder in sorted(time_folders):
    if not folder.startswith("images/"):
        folder = "images/" + folder.lstrip("/")
    if "images/locations/" not in folder and not folder.startswith("images/locations"):
        continue
    for t in TIMES:
        base = ROOT / folder / t
        p = exists_any(base)
        key = f"{folder}/{t}"
        if p:
            ok.append(f"TIME {key} ({p.stat().st_size})")
            resolved_paths.add(key)
        else:
            missing.append(f"TIME {key}  [from ShowLocationTimeImage]")


# --- ShowImagePath ---
for path in sorted(show_paths):
    if not is_location_scope(path):
        continue
    p = exists_any(ROOT / path)
    if p:
        ok.append(f"PATH {path} ({p.stat().st_size})")
        resolved_paths.add(path)
    else:
        missing.append(f"PATH {path}  [from ShowImagePath]")


# --- ShowLocationImage ids ---
for lid in sorted(loc_ids):
    for t in TIMES:
        if lid.startswith("rooms/"):
            parts = lid.split("/")
            # rooms/player/chest → images/locations/rooms/player/chest_{t}
            alt = ROOT / "images" / "locations" / "/".join(parts[:-1]) / f"{parts[-1]}_{t}"
            p = exists_any(alt)
            if not p:
                p = exists_any(ROOT / "images" / "locations" / f"{lid}_{t}")
        else:
            p = exists_any(ROOT / "images" / "locations" / f"{lid}_{t}")
        key = f"LOCIMG {lid}_{t}"
        if p and p.stat().st_size > 1024:
            ok.append(f"{key} ({p.stat().st_size})")
        else:
            missing.append(f"{key}  [from ShowLocationImage]")


# --- Legacy ShowImage location map ---
for rel, typ, cat, act, pose in legacy_calls:
    path = legacy_resolve(typ, cat, act, pose)
    if not path:
        continue
    if not is_location_scope(path):
        continue
    p = exists_any(ROOT / path)
    tag = f"LEGACY {path}  [{rel} ShowImage {typ}/{cat}/{act}" + (f"/{pose}" if pose else "") + "]"
    if p and p.stat().st_size > 1024:
        ok.append(f"OK {path} ({p.stat().st_size})")
        resolved_paths.add(path)
    else:
        missing.append(tag)


# --- Named checks from acceptance criteria ---
named_checks = {
    "church_ajar": ROOT / "images/locations/church/window/ajar.png",
    "church_general": ROOT / "images/locations/church/general/normal.png",
    "guard_closed": ROOT / "images/locations/guard/post/closed.jpg",
    "guard_normal": ROOT / "images/locations/guard/post/normal.jpg",
    "guard_talk": ROOT / "images/locations/guard/post/talk.jpg",
    "guard_street": ROOT / "images/locations/guard/street/normal.jpg",
    "port_day": ROOT / "images/locations/port/general/day.jpg",
    "becky_shop": ROOT / "images/locations/becky/shop/normal.jpg",
    "inga_shop": ROOT / "images/locations/inga/shop/normal.jpg",
    "inga_backroom_guard": ROOT / "images/locations/inga/backroom/guard.jpg",
    "draupnir_closed": ROOT / "images/locations/draupnir/shop/closed.jpg",
}

named = {}
for k, p in named_checks.items():
    found = exists_any(p.with_suffix("")) if p.suffix else exists_any(p)
    if found is None:
        found = exists_any(Path(str(p).rsplit(".", 1)[0])) if "." in p.name else None
    # try stem
    if found is None:
        found = exists_any(p.parent / p.stem)
    if found:
        named[k] = (found.stat().st_size, md5(found))
    else:
        named[k] = None
        missing.append(f"NAMED missing {k} expected near {p}")

# Inga == Becky
inga_eq = (
    named.get("inga_shop")
    and named.get("becky_shop")
    and named["inga_shop"][1] == named["becky_shop"][1]
)
ajar_ne = (
    named.get("church_ajar")
    and named.get("church_general")
    and named["church_ajar"][1] != named["church_general"][1]
)
# Guard open must differ from closed (no shared CLOSED placard plate)
guard_open_ne_closed = (
    named.get("guard_normal")
    and named.get("guard_closed")
    and named["guard_normal"][1] != named["guard_closed"][1]
)
guard_talk_ne_closed = (
    named.get("guard_talk")
    and named.get("guard_closed")
    and named["guard_talk"][1] != named["guard_closed"][1]
)

# Deduplicate missing
missing = sorted(set(missing))

report = []
report.append("# location-image-audit")
report.append(f"legacy_calls_scanned={len(legacy_calls)}")
report.append(f"ok={len(ok)} missing={len(missing)}")
report.append(f"ajar_ne_general={ajar_ne}")
report.append(f"inga_eq_becky={inga_eq}")
report.append(f"guard_open_ne_closed={guard_open_ne_closed}")
report.append(f"guard_talk_ne_closed={guard_talk_ne_closed}")
report.append("")
report.append("## Named")
for k, v in named.items():
    report.append(f"- {k}: {v}")
report.append("")
report.append("## Missing")
for m in missing:
    report.append(f"- {m}")
report.append("")
report.append("## OK (first 100)")
for line in ok[:100]:
    report.append(f"- {line}")

(SCRATCH / "location-image-audit.md").write_text("\n".join(report), encoding="utf-8")
(SCRATCH / "named-asset-check.txt").write_text(
    "\n".join(
        [f"{k}={v}" for k, v in named.items()]
        + [
            f"ajar_ne_general={ajar_ne}",
            f"inga_eq_becky={inga_eq}",
            f"guard_open_ne_closed={guard_open_ne_closed}",
            f"guard_talk_ne_closed={guard_talk_ne_closed}",
            f"missing_count={len(missing)}",
        ]
    ),
    encoding="utf-8",
)

print(f"legacy_calls={len(legacy_calls)} ok={len(ok)} missing={len(missing)}")
print(f"ajar_ne={ajar_ne} inga_eq={inga_eq} guard_open_ne={guard_open_ne_closed} talk_ne={guard_talk_ne_closed}")
for m in missing[:50]:
    print("FAIL", m)
if len(missing) > 50:
    print(f"... +{len(missing)-50} more")

fail = bool(missing) or not ajar_ne or not inga_eq or not guard_open_ne_closed or not guard_talk_ne_closed
if fail:
    print("AUDIT_FAIL")
    sys.exit(1)
print("AUDIT_PASS")
print(f"WROTE {SCRATCH / 'location-image-audit.md'}")
