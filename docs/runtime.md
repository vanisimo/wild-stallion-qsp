# Runtime Profiles

The game currently starts in the `dev` runtime profile.

Runtime profile is set in `TraKtir.qsps`:

```qsp
$RuntimeProfile = 'dev'
```

## Profiles

- `dev` - debug panels, debug output, and image debug helpers are enabled.
- `release` - debug output and image debug helpers are disabled.

## Switching To Release

Change the start file to:

```qsp
$RuntimeProfile = 'release'
```

Then rebuild `game.qsp` and do a short smoke test.

## Notes

- `GameInit` reads `$RuntimeProfile` and sets `debug` and `debug_images`.
- If `$RuntimeProfile` is empty, `GameInit` falls back to `dev`.
- Keep new debug-only UI behind `if debug = 1`.
