#!/usr/bin/env python3
"""Generate labeled webp placeholders for Amanda home intimacy steps."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

ROOM_NIGHTGOWN = [
    "hug",
    "kiss",
    "petting",
    "handjob",
    "blowjob",
    "cuni",
    "talk",
    "talk_done",
    "idle",
    "after_night",
    "evening_talk",
    "unlock",
]

ROOM_NAKED = [
    "sleep",
    "hug",
    "kiss",
    "petting",
    "handjob",
    "blowjob",
    "cuni",
    "talk",
    "talk_done",
    "idle",
    "after_night",
    "evening_talk",
    "unlock",
]

SEX_FILES = [
    ("foreplay", "undress"),
    ("foreplay", "touch"),
    ("vaginal", "missionary_enter"),
    ("vaginal", "missionary_slow"),
    ("vaginal", "missionary_orgasm"),
    ("vaginal", "missionary_repeat"),
    ("vaginal", "doggy_learn"),
    ("vaginal", "side_learn"),
    ("finish", "prompt"),
    ("finish", "inside"),
    ("finish", "outside"),
]


def load_font(size: int):
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


TIMES = ("morning", "day", "night")


def make_room_scene_placeholder(
    path: Path, time_key: str, outfit: str, pose: str, accent: tuple[int, int, int]
):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1024, 576), (28, 24, 32))
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 360, 1024, 576), fill=(42, 36, 48))
    draw.rectangle((520, 300, 920, 520), outline=accent, width=3)
    draw.rectangle((540, 320, 900, 500), fill=(56, 48, 62))

    title_font = load_font(30)
    sub_font = load_font(20)
    small_font = load_font(15)

    draw.text((512, 48), "AMANDA IN ROOM", fill=accent, font=title_font, anchor="mm")
    draw.text((512, 96), f"{time_key} / {outfit} / {pose}", fill=(245, 240, 230), font=sub_font, anchor="mm")
    draw.text((512, 540), "ROOM SCENE PLACEHOLDER", fill=(120, 115, 130), font=small_font, anchor="mm")

    img.save(path, format="WEBP", quality=82)
    print(path.relative_to(ROOT))


def make_placeholder(path: Path, title: str, subtitle: str, accent: tuple[int, int, int]):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (720, 960), (24, 22, 30))
    draw = ImageDraw.Draw(img)

    draw.rectangle((24, 24, 696, 936), outline=accent, width=4)
    draw.rectangle((40, 40, 680, 920), fill=(36, 32, 44))

    title_font = load_font(34)
    sub_font = load_font(22)
    small_font = load_font(16)

    draw.text((360, 120), "AMANDA HOME", fill=accent, font=title_font, anchor="mm")
    draw.text((360, 190), title, fill=(245, 240, 230), font=sub_font, anchor="mm")
    draw.text((360, 240), subtitle, fill=(170, 165, 180), font=small_font, anchor="mm")
    draw.text((360, 860), "PLACEHOLDER", fill=(110, 105, 120), font=small_font, anchor="mm")

    img.save(path, format="WEBP", quality=82)
    print(path.relative_to(ROOT))


def main():
    loc_dir = ROOT / "images" / "locations"
    room_dir = ROOT / "images" / "sex" / "amanda" / "room"
    sex_dir = ROOT / "images" / "sex" / "amanda"

    for time_key in TIMES:
        for pose in ROOM_NIGHTGOWN:
            make_room_scene_placeholder(
                loc_dir / f"amanda_room_{time_key}_nightgown_{pose}.webp",
                time_key,
                "nightgown",
                pose,
                (196, 168, 122),
            )

        for pose in ROOM_NAKED:
            make_room_scene_placeholder(
                loc_dir / f"amanda_room_{time_key}_naked_{pose}.webp",
                time_key,
                "naked",
                pose,
                (196, 122, 148),
            )

    for pose in ROOM_NIGHTGOWN:
        make_placeholder(
            room_dir / f"nightgown_{pose}.webp",
            "room / nightgown",
            pose,
            (196, 168, 122),
        )

    for pose in ROOM_NAKED:
        make_placeholder(
            room_dir / f"naked_{pose}.webp",
            "room / naked",
            pose,
            (196, 122, 148),
        )

    for category, pose in SEX_FILES:
        make_placeholder(
            sex_dir / category / f"{pose}.webp",
            f"sex / {category}",
            pose,
            (122, 168, 196),
        )


if __name__ == "__main__":
    main()