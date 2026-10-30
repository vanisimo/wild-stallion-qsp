---
name: qsp-visuals-and-assets
description: >-
  Use this skill when adding, auditing, or deploying visual assets, images,
  #SceneShowVisual calls, HallMissingGirlShowImage, SandraKitchenShowImage,
  location day/night images, or 32x32 UI action/item icons in the Wild Stallion QSP project.
---

# QSP Visuals, Art Keys & UI Icons Guide

In **«Дикий Жеребец» (Wild Stallion QSP)**, the rule **VISUAL ON EVERY SCREEN (no empty screens)** is strictly enforced across the entire game.

## 1. `#SceneShowVisual` Signature & Usage

Defined in `modules/core/show_image/show_image_helpers.qsps`:
- `ARGS[0]` — future asset path **without extension** (e.g., `'images/events/sandra/kitchen_hook/notice_door_enter'`)
- `ARGS[1]` — mandatory Russian caption describing what is on screen (e.g., `'notice: клиент входит на кухню'`)
- `ARGS[2]` — size: `'small' | 'medium' | 'large' | 'portrait'` (default: `'large'`)
- `ARGS[3]` — preferred real extension: `'webp' | 'png' | 'jpg'` (default: `'webp'`)

Example:
```qsp
gs 'SceneShowVisual', 'images/events/sandra/kitchen_hook/notice_door_enter', 'notice: клиент входит на кухню'
```

### Key Rules:
1. **Place before `*pl` narrative:** Call `SceneShowVisual` in the dispatcher/location logic or at the top of the `PrintText` block before the narrative paragraphs, never scattered inside `USER-OWNED TEXT` prose.
2. **Stub vs Real Art:** By default, `#SceneShowVisual` displays `images/common/hall_scene_stub.png` + `[VIS] caption`. Setting `SceneArtUseReal = 1` before calling `SceneShowVisual` renders the real asset at `ARGS[0]`.
3. **Domain-Specific Wrappers:**
   - Hall missing scenes: `gs 'HallMissingGirlShowImage', ...` (uses `HallMissingArtUseReal`)
   - Sandra kitchen hook: `gs 'SandraKitchenShowImage', ...` (uses `SandraKitchenArtUseReal`)
   - GirlTalk context portraits: `gs 'ShowGirlTalkContextImage', $girl, 'large', $topic`

## 2. UI Action & Item Icons (32×32 px)

- Every `act` must have an icon path as its second argument:
  ```qsp
  gs 'ActUiPrepare', 'Текст действия', 'icon_key'
  act $ActUiLabel, $ActUiIconPath:
      ...
  end
  ```
- Action icons live in `images/common/ui/actions/*.png` (**32×32 px**).
- Item panel buttons (`addobj`) must use `#PanelUiAddGlobalButton` / `#PanelUiIconPath` (group `'item'`, assets in `images/common/ui/*.png`, **32×32 px**).

## 3. Auditing & Deploying Visual Assets

Run these scripts when checking or deploying images:

```powershell
# Game-wide audit of visual calls on every screen
powershell -ExecutionPolicy Bypass -File tools/verify_gamewide_visuals.ps1

# Hall & kitchen visual coverage check
powershell -ExecutionPolicy Bypass -File tools/verify_hall_kitchen_visuals.ps1

# Verify SFW batch art files against key lists
powershell -ExecutionPolicy Bypass -File tools/verify_art_batch_files.ps1

# Verify location day/night and prop assets
python scripts/verify_location_assets.py
python scripts/audit_location_images.py

# Deploy source images from PIc/ into images/
python scripts/deploy_pic_assets.py
```

## 4. Asset Documentation & Registries

- Hall event visual keys: [ASSET-hall-events-visual.md](../../../docs/ASSET-hall-events-visual.md)
- Location day/night props audit: [AUDIT-location-daynight-props.md](../../../docs/AUDIT-location-daynight-props.md)
- Game-wide visual report: [visual_gamewide_report.txt](../../../tools/visual_gamewide_report.txt)
