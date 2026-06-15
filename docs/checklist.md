# Change Checklist

Before committing a gameplay change:

- The project still builds into `game.qsp`.
- The game starts from `TraKtir.qsps`.
- The changed location or scene can be opened.
- Runtime profile is intentionally set in `TraKtir.qsps`.
- New long text has a paired `_text.qsps` file when practical.
- New shared state is documented in `docs/state.md`.
- No absolute local paths were added.
- Generated files such as `game.qsp`, `game.txt`, and workspace files are not staged.
