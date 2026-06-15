# TraKtir

QSP interactive fiction project. Entry point: `TraKtir.qsps`.

## Structure

- `modules/actions` - player actions grouped into dialogs, flirts, sex, and tavern workflows.
- `modules/core` - base systems: initialization, time, economy, images, tavern state, character data.
- `modules/events` - event chains and reactions.
- `modules/locations` - playable locations grouped into tavern, rooms, town, and shops.
- `modules/menu` - panels, girl menus, NPC UI helpers, and global menu handlers.
- `modules/npc` - NPC initialization and NPC-specific logic grouped by family, shops, port, town, and story arcs.
- `modules/debug` - debug panels and tools.
- `modules/story` - reserved for larger story arcs.
- `modules/system` - reserved for low-level technical helpers.
- `archive` - old code kept outside the active build.
- `images` - location images and portraits.

More details:

- `docs/structure.md` - project folder map.
- `docs/naming.md` - naming rules for files, locations, and variables.
- `docs/state.md` - main global state notes.
- `docs/runtime.md` - runtime/debug profile notes.
- `docs/location-index.md` - generated index of active QSP locations.
- `docs/location-analysis.md` - generated report of direct incoming location calls.
- `docs/checklist.md` - short pre-commit checklist.

## Build And Run

Check the project manually with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check.ps1 -Strict
```

Regenerate the location index with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\generate-location-index.ps1
```

Regenerate the location analysis with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\analyze-locations.ps1
```

Build `game.qsp` with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build.ps1
```

Build a release profile with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Profile release
```

The build script runs the strict project check before converting sources. For a quick converter-only run, pass `-SkipCheck`.

Run the compiled game with:

```bat
run_game.bat
```

`run_game.bat` looks for `qspgui.exe` in `PATH`, then in common local install paths. If QSP is installed elsewhere, add the folder with `qspgui.exe` to `PATH` or update `run_game.bat`.

## Project Rules

- Source files live in `.qsps`; `game.qsp` and `game.txt` are generated build outputs.
- Long scene text should use a paired `*_text.qsps` file when practical.
- Large new systems should get their own subfolder inside the appropriate `modules` section.
- Editor workspace files and temporary files should not be committed.
