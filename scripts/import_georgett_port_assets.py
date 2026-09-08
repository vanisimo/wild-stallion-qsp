import os
import shutil
from pathlib import Path
from PIL import Image

LEGACY_SRC = Path(r"F:\Games\Albedo\Traktir Wild Stallion 0.05\images")
TARGET_DIR = Path(r"D:\traktir\images")

MAX_EDGE = 1400
WEBP_QUALITY = 86

def export_asset(src_path: Path, dest_base_without_ext: Path):
    dest_base_without_ext.parent.mkdir(parents=True, exist_ok=True)
    
    dest_jpg = dest_base_without_ext.with_suffix(".jpg")
    if not dest_jpg.exists():
        shutil.copy2(src_path, dest_jpg)
        
    dest_webp = dest_base_without_ext.with_suffix(".webp")
    dest_png = dest_base_without_ext.with_suffix(".png")
    
    if not dest_webp.exists() or not dest_png.exists():
        try:
            with Image.open(src_path) as img:
                img_rgb = img.convert("RGB")
                w, h = img_rgb.size
                if max(w, h) > MAX_EDGE:
                    scale = MAX_EDGE / max(w, h)
                    img_rgb = img_rgb.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                
                if not dest_webp.exists():
                    img_rgb.save(dest_webp, "WEBP", quality=WEBP_QUALITY, method=6)
                if not dest_png.exists():
                    img_rgb.save(dest_png, "PNG", optimize=True)
        except Exception as e:
            print(f"Error converting {src_path}: {e}")

def main():
    if not LEGACY_SRC.exists():
        print(f"Error: source {LEGACY_SRC} does not exist!")
        return

    print("Starting Georgette & Lizette port asset import...")

    georgett_src = LEGACY_SRC / "georgett"
    liza_src = LEGACY_SRC / "Liza"
    amanda_src = LEGACY_SRC / "amanda"
    eddie_src = LEGACY_SRC / "eddie"

    # 1. Portraits: Georgette
    portraits_geo = georgett_src / "portraits"
    if portraits_geo.exists():
        for p in portraits_geo.glob("*.jpg"):
            stem = p.stem
            dest_base = TARGET_DIR / "portraits" / "georgett" / stem
            export_asset(p, dest_base)
            export_asset(p, TARGET_DIR / "events" / "georgett" / "portraits" / stem)
        
        p1 = portraits_geo / "portrait1.jpg"
        p2 = portraits_geo / "portrait2.jpg"
        p3 = portraits_geo / "portrait3.jpg"
        p4 = portraits_geo / "portrait4.jpg"
        if p1.exists():
            export_asset(p1, TARGET_DIR / "portraits" / "georgett" / "talk_calm")
            export_asset(p1, TARGET_DIR / "locations" / "georgett" / "normal" / "normal")
        if p2.exists():
            export_asset(p2, TARGET_DIR / "portraits" / "georgett" / "talk_happy")
        if p3.exists():
            export_asset(p3, TARGET_DIR / "portraits" / "georgett" / "talk_angry")
        if p4.exists():
            export_asset(p4, TARGET_DIR / "portraits" / "georgett" / "talk_tired")

    # 2. Portraits: Lizette
    lizatalk1 = amanda_src / "tavern" / "lizatalk1.jpg"
    lizatalk2 = amanda_src / "tavern" / "lizatalk2.jpg"
    liza_naked = liza_src / "portraits" / "naked.jpg"
    liza_nakedtits = liza_src / "portraits" / "nakedtits1.jpg"

    if lizatalk1.exists():
        export_asset(lizatalk1, TARGET_DIR / "portraits" / "lizette" / "portrait1")
        export_asset(lizatalk1, TARGET_DIR / "portraits" / "lizette" / "talk_calm")
        export_asset(lizatalk1, TARGET_DIR / "portraits" / "lizette" / "talk_tired")
    elif liza_naked.exists():
        export_asset(liza_naked, TARGET_DIR / "portraits" / "lizette" / "portrait1")
        export_asset(liza_naked, TARGET_DIR / "portraits" / "lizette" / "talk_calm")

    if lizatalk2.exists():
        export_asset(lizatalk2, TARGET_DIR / "portraits" / "lizette" / "portrait2")
        export_asset(lizatalk2, TARGET_DIR / "portraits" / "lizette" / "talk_happy")
    if liza_nakedtits.exists():
        export_asset(liza_nakedtits, TARGET_DIR / "portraits" / "lizette" / "talk_angry")

    # 3. Georgette Port images
    port_dir = georgett_src / "Port"
    if port_dir.exists():
        for p in port_dir.glob("*.jpg"):
            stem = p.stem
            dest_base = TARGET_DIR / "events" / "georgett" / "port" / stem
            export_asset(p, dest_base)
            export_asset(p, TARGET_DIR / "locations" / "georgett" / "port" / stem)

    if (port_dir / "port1.jpg").exists():
        export_asset(port_dir / "port1.jpg", TARGET_DIR / "events" / "georgette" / "georgette_port_night" / "georgette_port_after_sex")
    if (port_dir / "port2.jpg").exists():
        export_asset(port_dir / "port2.jpg", TARGET_DIR / "events" / "port" / "port_prost_night" / "port_prost_night_after_georg")
    if (port_dir / "lizaminet.jpg").exists():
        export_asset(port_dir / "lizaminet.jpg", TARGET_DIR / "events" / "port" / "port_prost_night" / "port_prost_night_after_liz")

    withliza1 = georgett_src / "church" / "withliza1.jpg"
    if withliza1.exists():
        export_asset(withliza1, TARGET_DIR / "events" / "port" / "georgette_seek" / "lizette_peek_1")
    elif (port_dir / "wait.jpg").exists():
        export_asset(port_dir / "wait.jpg", TARGET_DIR / "events" / "port" / "georgette_seek" / "lizette_peek_1")

    if lizatalk1.exists():
        export_asset(lizatalk1, TARGET_DIR / "events" / "port" / "amanda_lizette" / "morning")
        export_asset(lizatalk1, TARGET_DIR / "events" / "port" / "amanda_lizette" / "day")
    if lizatalk2.exists():
        export_asset(lizatalk2, TARGET_DIR / "events" / "port" / "amanda_lizette" / "evening")
        export_asset(lizatalk2, TARGET_DIR / "events" / "port" / "amanda_lizette" / "night")

    # 4. Port Night Alley Scenes (18 scenes)
    alley_mappings = {
        "georgett_sailors": georgett_src / "portevents" / "event1_1.jpg",
        "georgett_townsman": georgett_src / "portevents" / "event2_1.jpg",
        "georgett_oral": georgett_src / "sex" / "minet1.jpg",
        "georgett_wall": georgett_src / "portevents" / "event3_1.jpg",
        "georgett_anal": georgett_src / "sex" / "doggy1.jpg",
        "georgett_dp": georgett_src / "portevents" / "event4_1.jpg",
        "georgett_priest": georgett_src / "church" / "doggy1.jpg",
        "georgett_eddie": eddie_src / "sexeddie" / "doubleeddie.jpg" if (eddie_src / "sexeddie" / "doubleeddie.jpg").exists() else georgett_src / "sex" / "cowgirl1.jpg",
        "georgett_eddie_mommy": eddie_src / "sexeddie" / "grope.jpg" if (eddie_src / "sexeddie" / "grope.jpg").exists() else georgett_src / "sex" / "grope.jpg",
        "lizette_sailors": liza_src / "portevents" / "event1_1.jpg",
        "lizette_young": liza_src / "portevents" / "event2_1.jpg",
        "lizette_townsman": liza_src / "portevents" / "event3_1.jpg",
        "lizette_oral": liza_src / "sexstreet" / "minet1.jpg",
        "lizette_wall": liza_src / "sexstreet" / "rakom1.jpg",
        "lizette_barrel": liza_src / "portevents" / "event4_1.jpg",
        "lizette_legare": liza_src / "sexstreet" / "fuck1.jpg",
        "lizette_legare_oral": liza_src / "sexstreet" / "minet2.jpg",
        "lizette_legare_take": liza_src / "sexstreet" / "fuck2.jpg",
    }

    for scene_id, src_file in alley_mappings.items():
        if src_file.exists():
            dest_base = TARGET_DIR / "events" / "port" / "night_alley" / f"{scene_id}_1"
            export_asset(src_file, dest_base)

    # 5. Mirror legacy georgett folder
    for root, dirs, files in os.walk(georgett_src):
        rel_dir = Path(root).relative_to(georgett_src)
        for f in files:
            if f.lower().endswith(".jpg"):
                src_f = Path(root) / f
                dest_base = TARGET_DIR / "georgett" / rel_dir / src_f.stem
                export_asset(src_f, dest_base)

    print("Import finished successfully!")

if __name__ == "__main__":
    main()
