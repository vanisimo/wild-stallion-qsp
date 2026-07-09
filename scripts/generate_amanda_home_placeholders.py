#!/usr/bin/env python3
"""Generate labeled webp placeholders for Amanda home intimacy arc."""

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

TIMES = ("morning", "day", "night")

TIME_BG = {
    "morning": ((48, 42, 56), (88, 72, 58)),
    "day": ((40, 44, 58), (62, 58, 72)),
    "night": ((18, 16, 28), (34, 28, 44)),
}


def load_font(size: int):
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_vertical_gradient(draw: ImageDraw.ImageDraw, size: tuple[int, int], top: tuple, bottom: tuple):
    width, height = size
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
        draw.line((0, y, width, y), fill=color)


def make_room_scene_placeholder(
    path: Path, time_key: str, outfit: str, pose: str, accent: tuple[int, int, int]
):
    """Full-frame room scene stub (no nested frame / picture-in-picture)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    size = (1024, 576)
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)

    top, bottom = TIME_BG.get(time_key, TIME_BG["day"])
    draw_vertical_gradient(draw, size, top, bottom)

    draw.rectangle((0, 470, 1024, 576), fill=(58, 48, 40))
    draw.polygon([(120, 470), (904, 470), (960, 420), (64, 420)], fill=(72, 60, 52))
    draw.rectangle((180, 300, 860, 470), fill=(86, 72, 64))
    draw.rectangle((220, 330, 820, 450), fill=(98, 82, 72))
    draw.ellipse((430, 250, 570, 360), fill=(112, 88, 96) if outfit == "naked" else (92, 108, 128))

    title_font = load_font(34)
    sub_font = load_font(22)
    small_font = load_font(16)

    outfit_label = "NIGHTGOWN" if outfit == "nightgown" else "NAKED"
    draw.text((512, 40), "AMANDA ROOM SCENE", fill=accent, font=title_font, anchor="mm")
    draw.text((512, 82), f"{time_key.upper()}  |  {outfit_label}  |  {pose}", fill=(245, 240, 230), font=sub_font, anchor="mm")
    draw.text((512, 548), "REPLACE: one full scene image (girl on bed in room)", fill=(150, 145, 160), font=small_font, anchor="mm")

    img.save(path, format="WEBP", quality=82)
    print(path.relative_to(ROOT))

    png_path = path.with_suffix(".png")
    img.save(png_path, format="PNG")
    print(png_path.relative_to(ROOT))


def make_empty_room_png(path: Path, time_key: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    size = (1024, 576)
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)

    top, bottom = TIME_BG.get(time_key, TIME_BG["day"])
    draw_vertical_gradient(draw, size, top, bottom)

    draw.rectangle((0, 470, 1024, 576), fill=(58, 48, 40))
    draw.polygon([(120, 470), (904, 470), (960, 420), (64, 420)], fill=(72, 60, 52))
    draw.rectangle((180, 300, 860, 470), fill=(86, 72, 64))
    draw.rectangle((220, 330, 820, 450), fill=(98, 82, 72))

    title_font = load_font(34)
    sub_font = load_font(20)
    draw.text((512, 48), "AMANDA ROOM (EMPTY)", fill=(170, 160, 140), font=title_font, anchor="mm")
    draw.text((512, 92), time_key.upper(), fill=(220, 215, 205), font=sub_font, anchor="mm")

    img.save(path, format="PNG")
    print(path.relative_to(ROOT))


def make_sex_room_stub(path: Path, outfit: str, pose: str, accent: tuple[int, int, int]):
    """Compact landscape stub for SexScene (images/sex/amanda/room/*)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    size = (1024, 576)
    img = Image.new("RGB", size, (22, 20, 30))
    draw = ImageDraw.Draw(img)
    draw_vertical_gradient(draw, size, (28, 24, 36), (44, 36, 52))

    draw.rectangle((0, 430, 1024, 576), fill=(58, 48, 40))
    draw.polygon([(120, 430), (904, 430), (960, 380), (64, 380)], fill=(72, 60, 52))
    draw.rectangle((180, 280, 860, 430), fill=(86, 72, 64))
    draw.rectangle((220, 310, 820, 410), fill=(98, 82, 72))
    draw.ellipse((430, 210, 570, 310), fill=(112, 88, 96) if outfit == "naked" else (92, 108, 128))

    title_font = load_font(30)
    sub_font = load_font(22)
    small_font = load_font(16)

    draw.text((512, 52), "AMANDA · room", fill=accent, font=title_font, anchor="mm")
    draw.text((512, 92), f"{outfit} / {pose}", fill=(245, 240, 230), font=sub_font, anchor="mm")
    draw.text((512, 548), "PLACEHOLDER", fill=(110, 105, 120), font=small_font, anchor="mm")

    img.save(path, format="WEBP", quality=82)
    print(path.relative_to(ROOT))


def make_sex_placeholder(path: Path, title: str, subtitle: str, accent: tuple[int, int, int]):
    """Sex-step stub for first-night arc (separate from room location scenes)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1024, 576), (22, 20, 30))
    draw = ImageDraw.Draw(img)
    draw_vertical_gradient(draw, (1024, 576), (28, 24, 36), (44, 36, 52))

    title_font = load_font(32)
    sub_font = load_font(22)
    small_font = load_font(16)

    draw.text((512, 72), "AMANDA FIRST SEX", fill=accent, font=title_font, anchor="mm")
    draw.text((512, 120), title, fill=(245, 240, 230), font=sub_font, anchor="mm")
    draw.text((512, 156), subtitle, fill=(180, 175, 190), font=small_font, anchor="mm")
    draw.text((512, 540), "SEX SCENE PLACEHOLDER", fill=(110, 105, 120), font=small_font, anchor="mm")

    img.save(path, format="WEBP", quality=82)
    print(path.relative_to(ROOT))


def main():
    loc_dir = ROOT / "images" / "locations"
    sex_dir = ROOT / "images" / "sex" / "amanda"

    for time_key in TIMES:
        for pose in ROOM_NIGHTGOWN:
            make_room_scene_placeholder(
                loc_dir / f"amanda_room_{time_key}_nightgown_{pose}.webp",
                time_key,
                "nightgown",
                pose,
                (210, 180, 130),
            )

        for pose in ROOM_NAKED:
            make_room_scene_placeholder(
                loc_dir / f"amanda_room_{time_key}_naked_{pose}.webp",
                time_key,
                "naked",
                pose,
                (210, 130, 158),
            )

        make_empty_room_png(loc_dir / f"amanda_room_{time_key}.png", time_key)

    for category, pose in SEX_FILES:
        make_sex_placeholder(
            sex_dir / category / f"{pose}.webp",
            f"sex / {category}",
            pose,
            (130, 175, 210),
        )

    room_dir = sex_dir / "room"
    for pose in ROOM_NIGHTGOWN:
        make_sex_room_stub(room_dir / f"nightgown_{pose}.webp", "nightgown", pose, (210, 180, 130))
    for pose in ROOM_NAKED:
        make_sex_room_stub(room_dir / f"naked_{pose}.webp", "naked", pose, (210, 130, 158))


if __name__ == "__main__":
    main()