#!/usr/bin/env python3
"""Copy curated PIc assets into images/ with game naming (webp)."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PIC = ROOT / "PIc"
IMAGES = ROOT / "images"
MANIFEST = PIC / "DEPLOYED_MANIFEST.json"

MAX_EDGE = 1400
WEBP_QUALITY = 86


def resolve_source(rel: str) -> Path | None:
    base = PIC / rel.replace("/", "\\") if "\\" not in rel else PIC / rel
    if base.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
        return base if base.is_file() and base.stat().st_size > 5000 else None
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        candidate = base.with_suffix(ext)
        if candidate.is_file() and candidate.stat().st_size > 5000:
            return candidate
    return None


def export_webp(src: Path, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > MAX_EDGE:
            scale = MAX_EDGE / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        out = dest.with_suffix(".webp")
        img.save(out, "WEBP", quality=WEBP_QUALITY, method=6)
    return {
        "source": str(src.relative_to(ROOT)),
        "dest": str(out.relative_to(ROOT)),
        "size": out.stat().st_size,
    }


# dest path (without extension) -> PIc relative source (without extension)
# Не класть cleaning_* в hall_missing: уборка как работа снята; under_table там — другая сцена.
MAPPING: dict[str, str] = {
    # --- Amanda: ideal set (PIc/amanda/amanda_ideal_* from PIC/Новая папка) ---
    "images/girls/amanda/portrait": "amanda/amanda_ideal_portrait",
    "images/portraits/amanda/talk_calm": "amanda/amanda_ideal_portrait",
    "images/portraits/amanda/talk_happy": "amanda/amanda_ideal_portrait",
    "images/portraits/amanda/talk_angry": "amanda/amanda_lora_extended/amanda_angry_01",
    "images/portraits/amanda/talk_tired": "amanda/amanda_lora_extended/amanda_sad_02",
    "images/portraits/amanda/portrait1": "amanda/amanda_ideal_portrait",
    "images/portraits/amanda/portrait2": "amanda/amanda_ideal_fullbody",
    # --- Amanda: girl talk moods ---
    "images/events/girl_talk/amanda/calm_1": "amanda/amanda_ideal_portrait",
    "images/events/girl_talk/amanda/calm_2": "amanda/amanda_ideal_fullbody",
    "images/events/girl_talk/amanda/happy_1": "amanda/amanda_ideal_portrait",
    "images/events/girl_talk/amanda/happy_2": "amanda/amanda_lora_extended/amanda_02_happy_smile",
    "images/events/girl_talk/amanda/tired_1": "amanda/amanda_lora_extended/amanda_sad_02",
    "images/events/girl_talk/amanda/tired_2": "15_amanda_qsp/amanda_clean_0003",
    "images/events/girl_talk/amanda/angry_1": "amanda/amanda_lora_extended/amanda_angry_01",
    "images/events/girl_talk/amanda/angry_2": "15_amanda_qsp/amanda_clean_0038",
    # --- Amanda: hall events ---
    "images/events/amanda/hall_harass/waitress_1_base": "15_amanda_qsp/amanda_clean_0014",
    "images/events/amanda/hall_harass/waitress_2_base": "15_amanda_qsp/amanda_clean_0027",
    "images/events/amanda/hall_harass/reaction_ignore": "amanda/amanda_lora_extended/amanda_shy_03",
    "images/events/amanda/hall_harass/reaction_protect_hard": "amanda/amanda_lora_extended/amanda_angry_02",
    "images/events/amanda/hall_harass/reaction_watch": "02_amanda_interactions_optional/amanda_tavern_serving_03",
    "images/events/amanda/hall_lewd/lap_uniform0_base": "02_amanda_interactions_optional/amanda_intimate_lap_01",
    "images/events/amanda/hall_lewd/lap_uniform1_base": "02_amanda_interactions_optional/amanda_lap_sitting_03",
    "images/events/amanda/hall_lewd/bend_uniform0_base": "amanda/amanda_lora_extended/amanda_shortdress_flirty_01",
    "images/dance/amanda/dance_normal": "amanda/amanda_lora_extended/amanda_06_tavern_dancing",
    # --- Melissa (PIc/amanda/olia — brunette tavern set) ---
    "images/girls/melissa/portrait": "amanda/olia/685c4a3b-8968-4f6c-ba89-092d6fb0cd3c",
    "images/portraits/melissa/talk_calm": "amanda/olia/9124e9f4-86a9-428b-bdfd-ed276cc72608",
    "images/portraits/melissa/talk_happy": "amanda/olia/665622cf-eecd-4a28-b8a3-5a21beb8ce3f",
    "images/portraits/melissa/talk_tired": "amanda/olia/e0a88795-de76-4ef4-95f5-c8b75a0a38c2",
    "images/portraits/melissa/talk_angry": "amanda/olia/b2db3d53-d7b1-4484-8dae-75e574b231ad",
    "images/portraits/melissa/portrait1": "amanda/olia/685c4a3b-8968-4f6c-ba89-092d6fb0cd3c",
    "images/portraits/melissa/portrait2": "amanda/olia/25f5c603-a0e1-4426-b005-3d47796be318",
    "images/events/girl_talk/melissa/calm_1": "amanda/olia/685c4a3b-8968-4f6c-ba89-092d6fb0cd3c",
    "images/events/girl_talk/melissa/calm_2": "amanda/olia/9124e9f4-86a9-428b-bdfd-ed276cc72608",
    "images/events/girl_talk/melissa/happy_1": "amanda/olia/665622cf-eecd-4a28-b8a3-5a21beb8ce3f",
    "images/events/girl_talk/melissa/happy_2": "amanda/olia/9b050d13-5a5b-46c5-a643-80d45054db22",
    "images/events/girl_talk/melissa/tired_1": "amanda/olia/e0a88795-de76-4ef4-95f5-c8b75a0a38c2",
    "images/events/girl_talk/melissa/tired_2": "amanda/olia/9124e9f4-86a9-428b-bdfd-ed276cc72608",
    "images/events/girl_talk/melissa/angry_1": "amanda/olia/b2db3d53-d7b1-4484-8dae-75e574b231ad",
    "images/events/girl_talk/melissa/angry_2": "amanda/olia/55dad3e6-7af6-405f-a345-0a68cd6aa39e",
    "images/events/melissa/hall_harass/waitress_1_base": "amanda/olia/b2db3d53-d7b1-4484-8dae-75e574b231ad",
    "images/events/melissa/hall_harass/waitress_2_base": "amanda/olia/25f5c603-a0e1-4426-b005-3d47796be318",
    "images/events/melissa/hall_harass/reaction_ignore": "amanda/olia/9124e9f4-86a9-428b-bdfd-ed276cc72608",
    "images/events/melissa/hall_harass/reaction_watch": "amanda/olia/e0a88795-de76-4ef4-95f5-c8b75a0a38c2",
    "images/dance/melissa/dance_normal": "amanda/olia/9b050d13-5a5b-46c5-a643-80d45054db22",
}


def export_panel_png(src: Path, dest: Path, width: int = 256) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        img = img.convert("RGBA")
        w, h = img.size
        scale = width / w
        img = img.resize((width, int(h * scale)), Image.Resampling.LANCZOS)
        img.save(dest, "PNG", optimize=True)
    return {
        "source": str(src.relative_to(ROOT)),
        "dest": str(dest.relative_to(ROOT)),
        "size": dest.stat().st_size,
    }


def main() -> int:
    deployed: list[dict] = []
    missing: list[dict] = []

    for dest_rel, src_rel in MAPPING.items():
        src = resolve_source(src_rel)
        if src is None:
            missing.append({"dest": dest_rel, "source": src_rel})
            continue
        info = export_webp(src, ROOT / dest_rel.replace("/", "\\"))
        deployed.append(info)

    # UI mini-portrait Amanda
    amanda_panel_src = resolve_source("amanda/amanda_ideal_portrait")
    if amanda_panel_src:
        deployed.append(
            export_panel_png(
                amanda_panel_src,
                IMAGES / "common" / "ui" / "portraits" / "amanda.png",
            )
        )

    skipped_olia_dupes = [
        p.name
        for p in (PIC / "amanda" / "olia").glob("*.png")
        if " (" in p.name
    ]

    manifest = {
        "deployed_count": len(deployed),
        "missing_count": len(missing),
        "deployed": deployed,
        "missing": missing,
        "skipped_notes": {
            "olia_duplicates": skipped_olia_dupes,
            "not_used": [
                "PIc/** contact sheets, kohya datasets, npz, nude training sets",
                "olia: 090e162b, 98c97472, 9b050d13 duplicates — kept canonical UUID files only",
            ],
        },
    }

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Deployed: {len(deployed)}")
    print(f"Missing: {len(missing)}")
    if missing:
        for m in missing:
            print(f"  MISSING {m['dest']} <- {m['source']}")
    print(f"Manifest: {MANIFEST}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())