#!/usr/bin/env python3
"""Deploy dialogue images from D:/PIc/person into images/actions/dialogs/*.webp."""

from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PIC_PERSON = Path(r"D:\PIc\person")
DEST_DIR = ROOT / "images" / "actions" / "dialogs"
MAX_EDGE = 1400
WEBP_QUALITY = 86

DEST_DIR.mkdir(parents=True, exist_ok=True)

# Map target dialogue image (relative to DEST_DIR, without extension) -> source path
MAPPING: dict[str, Path] = {
    # --- Amanda ---
    "amanda_tavern": PIC_PERSON / "amanda" / "Ananda tavern" / "amanda_tavern_serving_03.jpg",
    "amanda_chat": PIC_PERSON / "amanda" / "Ananda tavern" / "amanda_01_tavern_standing.jpg",
    "amanda_smalltalk": PIC_PERSON / "amanda" / "Ananda tavern" / "amanda_03_tavern_sitting.jpg",
    "amanda_family": PIC_PERSON / "amanda" / "amanda portret" / "amanda_softsmile_03.jpg",
    "amanda_personal": PIC_PERSON / "amanda" / "amanda portret" / "amanda_shy_03.jpg",
    "amanda_compliment": PIC_PERSON / "amanda" / "Ananda tavern" / "amanda_shortdress_flirty_01.jpg",
    "amanda_gift": PIC_PERSON / "amanda" / "Amanda emotion" / "amanda_05_surprised.jpg",
    "amanda_important": PIC_PERSON / "amanda" / "Amanda emotion" / "amanda_neutral_01.jpg",

    # --- Melissa ---
    "melissa_tavern": PIC_PERSON / "Melissa" / "685c4a3b-8968-4f6c-ba89-092d6fb0cd3c.png",
    "melissa_chat": PIC_PERSON / "Melissa" / "9124e9f4-86a9-428b-bdfd-ed276cc72608.png",
    "melissa_smalltalk": PIC_PERSON / "Melissa" / "665622cf-eecd-4a28-b8a3-5a21beb8ce3f.png",
    "melissa_family": PIC_PERSON / "Melissa" / "25f5c603-a0e1-4426-b005-3d47796be318.png",
    "melissa_personal": PIC_PERSON / "Melissa" / "e0a88795-de76-4ef4-95f5-c8b75a0a38c2.png",
    "melissa_compliment": PIC_PERSON / "Melissa" / "9b050d13-5a5b-46c5-a643-80d45054db22.png",
    "melissa_gift": PIC_PERSON / "Melissa" / "8dfc0d65-db02-45b8-b6dc-c39cebaae86d.png",
    "melissa_important": PIC_PERSON / "Melissa" / "b2db3d53-d7b1-4484-8dae-75e574b231ad.png",

    # --- Sandra (from images/events/sandra/tavern/) ---
    "sandra_tavern": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress1.webp",
    "sandra_chat": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress2.webp",
    "sandra_smalltalk": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress3.webp",
    "sandra_family": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress4.webp",
    "sandra_personal": ROOT / "images" / "events" / "sandra" / "tavern" / "cleaning1.webp",
    "sandra_compliment": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress1.webp",
    "sandra_gift": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress3.webp",
    "sandra_important": ROOT / "images" / "events" / "sandra" / "tavern" / "waitress2.webp",

    # --- Clarissa ---
    "clarissa_tavern": PIC_PERSON / "Klarissa" / "0959f21d-1734-4ce6-9adb-131f9b485d91.png",
    "clarissa_chat": PIC_PERSON / "Klarissa" / "1c1c04d0-3adf-41ef-baf4-6d8535c511cf.png",
    "clarissa_smalltalk": PIC_PERSON / "Klarissa" / "32e656da-cc7f-4920-991e-84c8d1437c24.png",
    "clarissa_family": PIC_PERSON / "Klarissa" / "5fd432e0-11d9-40ec-88f1-8bfec8252572.png",
    "clarissa_personal": PIC_PERSON / "Klarissa" / "270db741-7f5c-478a-93d5-9ed21beb39f2.png",
    "clarissa_compliment": PIC_PERSON / "Klarissa" / "852e4c5b-d791-4d74-9708-295293b9279a.png",
    "clarissa_gift": PIC_PERSON / "Klarissa" / "6e3d5341-737f-4f90-ae3e-ce0f007ddb11.png",
    "clarissa_important": PIC_PERSON / "Klarissa" / "e24cb9c6-897c-426f-9979-719bc1b0c6bd.png",

    # --- Becky (rebeka) ---
    "becky_tavern": PIC_PERSON / "rebeka" / "0b8b7041-fcca-40f3-8e6a-2150d40e8f19.png",
    "becky_chat": PIC_PERSON / "rebeka" / "a3a554ca-2566-4fc0-869e-f7a1b7b298c7.png",
    "becky_smalltalk": PIC_PERSON / "rebeka" / "e984b623-439e-4766-80fc-bd40b8ed1104.png",
    "becky_family": PIC_PERSON / "rebeka" / "e6b1009a-5d87-4730-af5b-a7f39c6d6692.png",
    "becky_personal": PIC_PERSON / "rebeka" / "ChatGPT Image 3 мая 2026 г., 15_46_39.png",
    "becky_compliment": PIC_PERSON / "rebeka" / "ChatGPT Image 3 мая 2026 г., 15_46_48.png",
    "becky_gift": PIC_PERSON / "rebeka" / "ChatGPT Image 3 мая 2026 г., 15_46_53.png",
    "becky_important": PIC_PERSON / "rebeka" / "ChatGPT Image 3 мая 2026 г., 15_46_57.png",

    # --- Inga ---
    "inga_tavern": PIC_PERSON / "Inga" / "01ebded1-412b-48d9-a0e6-3456e1bc6716.png",
    "inga_chat": PIC_PERSON / "Inga" / "39eedbf1-971e-42b3-ae38-e37076e9121c.png",
    "inga_smalltalk": PIC_PERSON / "Inga" / "57266c8c-4b5d-4ec8-be03-69c9a594206c.png",
    "inga_personal": PIC_PERSON / "Inga" / "7ee38a1e-b203-41ec-93c4-56f17945ebca.png",
    "inga_compliment": PIC_PERSON / "Inga" / "b8af7b39-1a2a-4e63-971e-00ecf84239a8.png",
    "inga_gift": PIC_PERSON / "Inga" / "c0496525-b85f-42ed-8798-c80c788cece6.png",
    "inga_important": PIC_PERSON / "Inga" / "d34c8ae9-e54a-4271-b447-e69d59c8f51c.png",

    # --- Irma ---
    "irma_tavern": PIC_PERSON / "Irma" / "13873b52-e340-405c-a7a0-90221656db5f.png",
    "irma_chat": PIC_PERSON / "Irma" / "51ad0cac-54bc-4403-862c-aa516c525406.png",
    "irma_smalltalk": PIC_PERSON / "Irma" / "5f7b2739-55e6-4c53-a0c2-27032542ed5d.png",
    "irma_compliment": PIC_PERSON / "Irma" / "85bc1cbf-7b33-4439-ac85-2cd379a9e066.png",
    "irma_gift": PIC_PERSON / "Irma" / "3578e519-6bdf-4f4d-b754-d5b9a3e1ead1.png",
    "irma_important": PIC_PERSON / "Irma" / "592cca58-5256-41fd-aa26-f0a59cd71111.png",

    # --- Lizette ---
    "lizette_tavern": PIC_PERSON / "lizetta" / "127c8e50-04d5-48db-81a5-1e890c36c9a2.png",
    "lizette_chat": PIC_PERSON / "lizetta" / "263a4ae7-7942-443c-9229-75a01945d81f.png",
    "lizette_smalltalk": PIC_PERSON / "lizetta" / "9d5d8a56-33ab-4eca-ac18-7f2a335048c3.png",
    "lizette_personal": PIC_PERSON / "lizetta" / "ef2e6533-cb06-4131-8ea1-9152558ce93c.png",
    "lizette_compliment": PIC_PERSON / "lizetta" / "127c8e50-04d5-48db-81a5-1e890c36c9a2.png",
    "lizette_gift": PIC_PERSON / "lizetta" / "263a4ae7-7942-443c-9229-75a01945d81f.png",
    "lizette_important": PIC_PERSON / "lizetta" / "9d5d8a56-33ab-4eca-ac18-7f2a335048c3.png",

    # --- Eddie ---
    "eddie_tavern": PIC_PERSON / "eddy" / "12aeda5f-a7ba-4528-977a-b757721604cb.png",
    "eddie_chat": PIC_PERSON / "eddy" / "adac2708-6734-4f3a-bb4b-7a05dcdb9927.png",
    "eddie_smalltalk": PIC_PERSON / "eddy" / "dc26a9bd-d762-4360-8f3e-d0e6f84c8e54.png",
    "eddie_important": PIC_PERSON / "eddy" / "e9e69c8d-41d7-4f48-a654-4174f018f43f.png",

    # --- Gerhard ---
    "gerhard_tavern": PIC_PERSON / "gerhard" / "2853eb9c-34b5-4262-a249-c5eac041fabe.png",
    "gerhard_chat": PIC_PERSON / "gerhard" / "eb742328-f312-4c14-a7f8-4cf457abd914.png",
    "gerhard_smalltalk": PIC_PERSON / "gerhard" / "2853eb9c-34b5-4262-a249-c5eac041fabe.png",
    "gerhard_important": PIC_PERSON / "gerhard" / "eb742328-f312-4c14-a7f8-4cf457abd914.png",
}


def export_webp(src: Path, dest_base: Path) -> dict:
    with Image.open(src) as img:
        img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > MAX_EDGE:
            scale = MAX_EDGE / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        out = dest_base.with_suffix(".webp")
        img.save(out, "WEBP", quality=WEBP_QUALITY, method=6)
    return {
        "dest": out.name,
        "size": out.stat().st_size,
    }


def main():
    success = 0
    missing = 0
    for key, src in MAPPING.items():
        if not src.exists():
            print(f"[MISSING] {key} -> {src}")
            missing += 1
            continue
        dest_base = DEST_DIR / key
        res = export_webp(src, dest_base)
        print(f"[OK] {key}.webp ({res['size']} bytes)")
        success += 1
    print(f"\nDone: {success} deployed, {missing} missing.")


if __name__ == "__main__":
    main()
