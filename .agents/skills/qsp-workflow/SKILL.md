---
name: qsp-workflow
description: >-
  Use this skill to validate QSP syntax, lint modified .qsps files, compile game.qsp,
  check location consistency, auto-update location indices, verify game-wide visual tags,
  and ensure compliance with project rules and USER-OWNED files.
---

# QSP Development & Validation Workflow

This skill provides step-by-step procedures for building, checking, and maintaining the "Wild Stallion QSP" («Дикий Жеребец») project.

## 1. Fast Linter for Modified `.qsps` Files & Canon Rules

Checks rule file sizes (< 24 KB), `#LocationName` vs `---` balance, `@qsp/converters` parse gaps (unclosed quotes), bare `act` without icons, `! [AI-WORKED]` headers, glued `*p` strings, and forbidden Christian terms:

```powershell
# Lint all git-modified .qsps files + rule file budgets
python scripts/lint_qsp_changes.py

# Lint specific .qsps files
python scripts/lint_qsp_changes.py modules/events/amanda/some_file.qsps
```

## 2. Project-Wide Syntax & Integrity Check

Always run this check after modifying `.qsps` files to catch missing target locations, duplicate `#LocationName` headers, or broken image references:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check.ps1
```

For strict checking with automatic regeneration of `docs/location-index.md` and `docs/location-analysis.md`:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/check.ps1 -Strict -UpdateIndex
```

## 3. Validating QSP Separators (`---`) Across All Modules

To verify that `@qsp/converters` parses every `#LocationName` across all 500+ files without swallowing locations:

```powershell
python scripts/validate_qsps_separators.py
```

## 4. Compiling the Game (`game.qsp`)

To build the project into `game.qsp` (automatically updates location indices, runs strict check, uses `.build/tools` `@qsp/cli`, and runs `verify_qsps_compile.py`):

```powershell
# Development build without overwriting root game.qsp (safe test build)
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Profile dev -NoCopy

# Development build (updates root game.qsp)
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Profile dev

# Release build
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Profile release
```

## 5. Visuals on Every Screen Audit

To verify that all screens have accompanying visual calls (`#SceneShowVisual` or location images):

```powershell
powershell -ExecutionPolicy Bypass -File tools/verify_gamewide_visuals.ps1
python scripts/verify_location_assets.py
```

## 6. USER-OWNED Files Safety Rule

Never overwrite or polish narrative prose in files marked `USER-OWNED TEXT` (defined in `AGENTS.md`).
- `hall_missing_amanda_text.qsps` and `hall_missing_agent_melissa_text.qsps` are **COMPLETED (`ЗАВЕРШЕНО`)** — never touch them without explicit user request.
- For other `USER-OWNED TEXT` files, only touch logic/flow/`if`/`end` gates when fixing bugs, preserving user strings verbatim.
