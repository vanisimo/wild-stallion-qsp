---
name: openrouter-text-gen
description: >-
  Use this skill when the user wants to generate, draft, or expand Russian narrative
  prose, 18+ scenes, dialogues, or quest scenes via OpenRouter models
  (deepseek/deepseek-v3.1-terminus, deepseek/deepseek-v4-pro, etc.) using
  scripts/generate_text.py or the openrouter-writer MCP tools.
---

# OpenRouter Text Generation Skill (Wild Stallion QSP)

Use this skill whenever the user asks to generate scenes, dialogues, 18+ prose, or expand briefs from `promt/` / `*_text.qsps` through OpenRouter.

## 1. Choosing the Right Mode & Model

- **18+ / sensual / uncensored scenes (`--mode nsfw`)**:
  - Default model: `deepseek/deepseek-v4-pro` (with `--reasoning off` by default so tokens go into prose, not hidden reasoning)
  - Fallback if a provider filters explicit content: `deepseek/deepseek-v3.1-terminus`, `sao10k/l3.1-euryale-70b`, or `thedrummer/skyfall-36b-v2`
- **Dialogues & character banter (`--mode dialog`)**:
  - Default model: `deepseek/deepseek-v4-pro` (with `--reasoning off` by default so tokens go into prose, not hidden reasoning)
  - Alternatives: `mistralai/mistral-large-4-0`, `deepseek/deepseek-v3.2`
- **Quest / plot scenes (`--mode quest`)**:
  - Default model: `deepseek/deepseek-v4-pro`
- **Cheap quick drafts (`--mode fast`)**:
  - Default model: `deepseek/deepseek-v4.1-flash`

## 2. Running via `scripts/generate_text.py` (or MCP tool `openrouter_generate_scene`)

Always pass:
- `--mode nsfw|dialog|quest|fast`
- `--char ...` for character canon (`stefan`, `amanda`, `melissa`, `sandra`, `gerhard`, `lizette`, `becky`, `clarissa`, `legare`)
- `--corruption 0..5` when `FamilyCorruptionStage` matters
- `--qsp` when output is meant for `.qsps` (`*pl '...'` formatting with `''` quote escaping)
- `--prompt "..."` or `--brief-file promt/...`

Example command:
```powershell
python scripts/generate_text.py --mode nsfw --char stefan amanda --corruption 3 --qsp --prompt "..."
```

If an MCP tool `openrouter_generate_scene` is available from the `openrouter-writer` plugin, you may call it directly with the same parameters.

## 3. Safety & Canon Rules

1. **API key:** Loaded automatically from `.env` (`OPENROUTER_API_KEY`). Never expose or echo `.env` secrets in chat.
2. **USER-OWNED TEXT files:** Never overwrite or silently rewrite `USER-OWNED TEXT` files (`AGENTS.md`). Save drafts to `scratch/` or present the generated `*pl '...'` lines to the user unless they explicitly asked to insert them.
3. **Post-check:** After inserting generated text into any `.qsps` file, run `scripts/check.ps1` and `scripts/lint_qsp_changes.py` per `qsp-workflow`.
