---
name: qsp-workflow
description: >-
  Use this skill to validate QSP syntax, compile game.qsp, check location consistency,
  verify game-wide visual tags, and ensure compliance with project rules and USER-OWNED files.
---

# QSP Development & Validation Workflow

This skill provides step-by-step procedures for building, checking, and maintaining the "Wild Stallion QSP" project.

## 1. Syntax & Project Integrity Check

Always run this check after modifying any `.qsps` files to catch missing `end` statements, duplicate locations, or syntax errors:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check.ps1
```

For strict checking (treats warnings as errors):
```powershell
powershell -ExecutionPolicy Bypass -File scripts/check.ps1 -Strict
```

## 2. Compiling the Game

To build the project into `game.qsp`:

```powershell
# Development build (faster)
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Profile dev

# Release build
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Profile release
```

## 3. Visuals on Every Screen Audit

To verify that all screens have accompanying visual calls (`#SceneShowVisual` or images):

```powershell
powershell -ExecutionPolicy Bypass -File tools/verify_gamewide_visuals.ps1
```

## 4. USER-OWNED Files Safety Rule

Never overwrite or polish narrative prose in files marked `USER-OWNED TEXT` (defined in `AGENTS.md`). Only touch logic/flow/`if`/`end` gates if explicitly fixing bugs.
