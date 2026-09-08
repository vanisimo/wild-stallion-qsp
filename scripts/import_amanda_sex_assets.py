import os
import shutil
from pathlib import Path
from PIL import Image

LEGACY_SRC = Path(r"F:\Games\Albedo\Traktir Wild Stallion 0.05\images\amanda")
TARGET_DIR = Path(r"D:\traktir\images")

MAX_EDGE = 1400
WEBP_QUALITY = 86

def export_asset(src_path: Path, dest_base_without_ext: Path, overwrite=True):
    dest_base_without_ext.parent.mkdir(parents=True, exist_ok=True)
    
    dest_jpg = dest_base_without_ext.with_suffix(".jpg")
    dest_webp = dest_base_without_ext.with_suffix(".webp")
    dest_png = dest_base_without_ext.with_suffix(".png")
    
    if overwrite or not dest_jpg.exists():
        try:
            shutil.copy2(src_path, dest_jpg)
        except Exception as e:
            print(f"Error copying {src_path} to {dest_jpg}: {e}")

    if overwrite or not dest_webp.exists() or not dest_png.exists():
        try:
            with Image.open(src_path) as img:
                img_rgb = img.convert("RGB")
                w, h = img_rgb.size
                if max(w, h) > MAX_EDGE:
                    scale = MAX_EDGE / max(w, h)
                    img_rgb = img_rgb.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                
                img_rgb.save(dest_webp, "WEBP", quality=WEBP_QUALITY, method=6)
                img_rgb.save(dest_png, "PNG", optimize=True)
        except Exception as e:
            print(f"Error converting {src_path}: {e}")

def main():
    if not LEGACY_SRC.exists():
        print(f"Error: {LEGACY_SRC} does not exist!")
        return

    print("Starting Amanda & Stefan sex assets import...")

    sexroom = LEGACY_SRC / "sexroom"
    room = LEGACY_SRC / "Room"
    randomsex = LEGACY_SRC / "RandomSex"
    sexafterdance = LEGACY_SRC / "sexafterdance"
    gloryfirst = LEGACY_SRC / "gloryfirst"

    # 1. Replace placeholders in images/sex/amanda/
    sex_amanda = TARGET_DIR / "sex" / "amanda"

    # Foreplay
    if (sexroom / "grope1.jpg").exists():
        export_asset(sexroom / "grope1.jpg", sex_amanda / "foreplay" / "touch")
    if (sexroom / "naked1.jpg").exists():
        export_asset(sexroom / "naked1.jpg", sex_amanda / "foreplay" / "undress")

    # Vaginal
    vaginal_map = {
        "missionary_enter": sexroom / "fuckstart.jpg",
        "missionary_slow": sexroom / "fuck1.jpg",
        "missionary_orgasm": sexroom / "fuck2.jpg",
        "missionary_repeat": sexroom / "fuck3.jpg",
        "doggy_learn": sexroom / "fuck5.jpg",
        "side_learn": sexroom / "fuck6.jpg",
    }
    for pose, src_file in vaginal_map.items():
        if src_file.exists():
            export_asset(src_file, sex_amanda / "vaginal" / pose)

    # Finish
    finish_map = {
        "prompt": sexroom / "come1.jpg",
        "inside": sexroom / "cumpussy1.jpg",
        "outside": sexroom / "comeface.jpg",
    }
    for pose, src_file in finish_map.items():
        if src_file.exists():
            export_asset(src_file, sex_amanda / "finish" / pose)

    # Room Nightgown & Naked
    room_nightgown_map = {
        "nightgown_idle": room / "wakedress.jpg" if (room / "wakedress.jpg").exists() else sexroom / "amanda.jpg",
        "nightgown_kiss": sexroom / "kiss.jpg",
        "nightgown_petting": sexroom / "grope1.jpg",
        "nightgown_hug": sexroom / "kiss.jpg",
        "nightgown_blowjob": sexroom / "minet1.jpg",
        "nightgown_cuni": sexroom / "cuni.jpg",
        "nightgown_handjob": sexroom / "grope1.jpg",
        "nightgown_talk": sexroom / "amanda.jpg",
        "nightgown_talk_done": sexroom / "amanda.jpg",
        "nightgown_after_night": room / "wakedress.jpg" if (room / "wakedress.jpg").exists() else sexroom / "amanda.jpg",
        "nightgown_evening_talk": sexroom / "amanda.jpg",
        "nightgown_unlock": room / "wakedress.jpg" if (room / "wakedress.jpg").exists() else sexroom / "amanda.jpg",
    }
    for pose, src_file in room_nightgown_map.items():
        if src_file.exists():
            export_asset(src_file, sex_amanda / "room" / pose)

    room_naked_map = {
        "naked_idle": room / "amandanaked.jpg" if (room / "amandanaked.jpg").exists() else sexroom / "naked1.jpg",
        "naked_sleep": room / "wakenaked.jpg" if (room / "wakenaked.jpg").exists() else sexroom / "naked1.jpg",
        "naked_kiss": sexroom / "kissnaked.jpg" if (sexroom / "kissnaked.jpg").exists() else sexroom / "kiss.jpg",
        "naked_petting": sexroom / "grope2.jpg",
        "naked_hug": sexroom / "kissnaked.jpg" if (sexroom / "kissnaked.jpg").exists() else sexroom / "kiss.jpg",
        "naked_blowjob": sexroom / "minet2.jpg",
        "naked_cuni": sexroom / "cuni.jpg",
        "naked_handjob": sexroom / "grope2.jpg",
        "naked_talk": sexroom / "naked1.jpg",
        "naked_talk_done": sexroom / "naked2.jpg",
        "naked_after_night": sexroom / "nakedexcited1.jpg",
        "naked_evening_talk": sexroom / "naked3.jpg",
        "naked_unlock": sexroom / "nakedexcited2.jpg",
    }
    for pose, src_file in room_naked_map.items():
        if src_file.exists():
            export_asset(src_file, sex_amanda / "room" / pose)

    # Kiss, touch, oral, anal, after
    if (sexroom / "kiss.jpg").exists():
        export_asset(sexroom / "kiss.jpg", sex_amanda / "kiss" / "kiss")
    if (sexroom / "kissnaked.jpg").exists():
        export_asset(sexroom / "kissnaked.jpg", sex_amanda / "kiss" / "kissnaked")

    if (sexroom / "grope1.jpg").exists():
        export_asset(sexroom / "grope1.jpg", sex_amanda / "touch" / "grope1")
        export_asset(sexroom / "grope1.jpg", sex_amanda / "touch" / "touch")
    if (sexroom / "grope2.jpg").exists():
        export_asset(sexroom / "grope2.jpg", sex_amanda / "touch" / "grope2")

    if (sexroom / "cuni.jpg").exists():
        export_asset(sexroom / "cuni.jpg", sex_amanda / "oral" / "cuni")
    for i in range(1, 13):
        m = sexroom / f"minet{i}.jpg"
        if m.exists():
            export_asset(m, sex_amanda / "oral" / f"minet{i}")
            if i == 1:
                export_asset(m, sex_amanda / "oral" / "blowjob")

    if (sexroom / "fuck4.jpg").exists():
        export_asset(sexroom / "fuck4.jpg", sex_amanda / "anal" / "enter")
    if (sexroom / "fuck5.jpg").exists():
        export_asset(sexroom / "fuck5.jpg", sex_amanda / "anal" / "slow")
        export_asset(sexroom / "fuck5.jpg", sex_amanda / "anal" / "doggy")
    if (sexroom / "fuck6.jpg").exists():
        export_asset(sexroom / "fuck6.jpg", sex_amanda / "anal" / "missionary")

    if (sexroom / "nakedexcited1.jpg").exists():
        export_asset(sexroom / "nakedexcited1.jpg", sex_amanda / "after" / "after_sex")
    if (sexroom / "angry.jpg").exists():
        export_asset(sexroom / "angry.jpg", sex_amanda / "after" / "angry")
    if (sexroom / "cumpussy1.jpg").exists():
        export_asset(sexroom / "cumpussy1.jpg", sex_amanda / "after" / "cumpussy")
    if (sexroom / "cumpussyangry.jpg").exists():
        export_asset(sexroom / "cumpussyangry.jpg", sex_amanda / "after" / "cumpussyangry")

    # 2. Location room presence images (amanda_room_{time}_{outfit}_{pose})
    loc_dir = TARGET_DIR / "locations"
    times = ["morning", "day", "night"]
    for t in times:
        for pose, src_file in room_nightgown_map.items():
            short_pose = pose.replace("nightgown_", "")
            export_asset(src_file, loc_dir / f"amanda_room_{t}_nightgown_{short_pose}")
        for pose, src_file in room_naked_map.items():
            short_pose = pose.replace("naked_", "")
            export_asset(src_file, loc_dir / f"amanda_room_{t}_naked_{short_pose}")

    # 3. Mirror complete amanda subfolders into images/amanda/ and images/events/amanda/
    subfolders = ["sexroom", "Room", "RandomSex", "sexafterdance", "gloryfirst"]
    for sub in subfolders:
        sub_path = LEGACY_SRC / sub
        if sub_path.exists():
            for f in sub_path.glob("*.jpg"):
                export_asset(f, TARGET_DIR / "amanda" / sub / f.stem)
                export_asset(f, TARGET_DIR / "events" / "amanda" / sub.lower() / f.stem)

    print("Amanda & Stefan sex assets import finished successfully!")

if __name__ == "__main__":
    main()
