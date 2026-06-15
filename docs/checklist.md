# Change Checklist

Before committing a gameplay change:

- `scripts\check.ps1 -Strict` passes.
- `scripts\build.ps1` builds `game.qsp`.
- `docs\location-index.md` is regenerated after adding, removing, or renaming locations.
- `docs\location-analysis.md` is regenerated after changing location call flow.
- The game starts from `TraKtir.qsps`.
- The changed location or scene can be opened.
- Runtime profile is intentionally set in `TraKtir.qsps`.
- Release builds use `scripts\build.ps1 -Profile release`.
- New long text has a paired `_text.qsps` file when practical.
- New shared state is documented in `docs/state.md`.
- No absolute local paths were added.
- Generated files such as `game.qsp`, `game.txt`, and workspace files are not staged.
