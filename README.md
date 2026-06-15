# TraKtir

QSP interactive fiction project. Entry point: `TraKtir.qsps`.

## Structure

- `modules/actions` - player actions, dialogs, intimacy scenes, tavern actions.
- `modules/core` - base systems: initialization, time, economy, images, character data.
- `modules/events` - event chains and reactions.
- `modules/locations` - playable locations grouped into tavern, rooms, town, and shops.
- `modules/menu` - panels, girl menus, NPC UI helpers, and global menu handlers.
- `modules/npc` - NPC initialization and NPC-specific logic.
- `modules/debug` - debug panels and tools.
- `modules/story` - reserved for larger story arcs.
- `modules/system` - reserved for low-level technical helpers.
- `archive` - old code kept outside the active build.
- `images` - location images and portraits.

More details:

- `docs/structure.md` - project folder map.
- `docs/naming.md` - naming rules for files, locations, and variables.
- `docs/state.md` - main global state notes.
- `docs/checklist.md` - short pre-commit checklist.

## Build And Run

The project is built through `qsp-project.json` into `game.qsp`.

Run the compiled game with:

```bat
run_game.bat
```

The script looks for `qspgui.exe` in `PATH`, then in common local install paths. If QSP is installed elsewhere, add the folder with `qspgui.exe` to `PATH` or update `run_game.bat`.

## Project Rules

- Source files live in `.qsps`; `game.qsp` and `game.txt` are generated build outputs.
- Long scene text should use a paired `*_text.qsps` file when practical.
- Large new systems should get their own subfolder inside the appropriate `modules` section.
- Editor workspace files and temporary files should not be committed.
