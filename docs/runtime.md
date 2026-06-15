# Runtime Profiles

The game currently starts in the `dev` runtime profile.

Runtime profile is set in `TraKtir.qsps`:

```qsp
$RuntimeProfile = 'dev'
```

## Profiles

- `dev` - debug panels, debug output, and image debug helpers are enabled.
- `release` - debug output and image debug helpers are disabled.

## Building Release

Build the release profile with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Profile release
```

The build script changes the runtime profile only in the temporary combined source under `.build`; `TraKtir.qsps` stays in the development profile.

## Notes

- `GameInit` reads `$RuntimeProfile` and sets `debug` and `debug_images`.
- If `$RuntimeProfile` is empty, `GameInit` falls back to `dev`.
- Keep new debug-only UI behind `if debug = 1`.
