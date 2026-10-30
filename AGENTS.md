# AGENTS.md

Instructions for Antigravity, ChatGPT, Codex, and other AI coding agents working on this repository.
*(Игровые системы, UI-правила, визуальный канон `#SceneShowVisual`, религия/лор и ветки персонажей — в файле `GEMINI.md`, который подгружается автоматически вместе с `AGENTS.md`).*

## Project identity

This repository contains the QSP project **«Дикий Жеребец»** / **Wild Stallion QSP**.

Primary repository:

- `vanisimo/wild-stallion-qsp`

Primary branch:

- `main`

Main project file:

- `qsp-project.json`

Start location file:

- `TraKtir.qsps`

Build output:

- `game.qsp`

QSP player:

- QSP 5.90

Editor environment:

- Sublime Text
- `QSP.sublime-package` v0.18
- build system: `qsp-build-and-run`

## Important rule

Do **not** change `qsp-project.json` unless the user explicitly asks for it.

The current project configuration uses:

- `TraKtir.qsps` as the start file
- `game.qsp` as the build target
- `qsps_to_qsp` as the converter
- `Hard-off` as the preprocessor

## Current connected folders

The project currently connects these folders through `qsp-project.json`:

- `modules/actions`
- `modules/core`
- `modules/menu`
- `modules/debug`
- `modules/events`
- `modules/locations`
- `modules/npc`

Do not assume that folders outside this list are compiled unless `qsp-project.json` is explicitly changed by the user.

## Important structure

Known structure of the project:

- `modules/core/init_npc/`
- `modules/core/time/npc_talk_limits.qsps`
- `modules/core/show_image/image_debug_random.qsps`
- `modules/core/show_image/show_image_helpers.qsps` — `#SceneShowVisual` (stub + [VIS] caption, no empty screens)
- `modules/events/kitchen/sandra_kitchen_hook.qsps` — kitchen notice→play→missing (α)
- `modules/core/tavern/tavern_event_state_core.qsps`
- `modules/core/family/` — offense days engine
- `modules/actions/tavern/`
- `modules/actions/sex/`
- `modules/menu/`
- `modules/events/kitchen/`
- `modules/events/hall/`
- `modules/events/tavern/`
- `modules/events/dance/`
- `modules/events/amanda/`
- `modules/events/melissa/`
- `modules/events/sandra/`
- `modules/events/becky/`
- `modules/events/inga/`
- `modules/events/eddie/`
- `modules/events/family/` — shared family arcs (act1, council, home first sex…)
- `modules/locations/`
- `modules/npc/` — init only (`npc/amanda/amanda.qsps`, `npc/family/*`, …)
- `modules/debug/`

The folder `archive/old` is considered old/disabled material and should not be connected or reused without explicit instruction.

The folder `modules/images` is not currently connected in `qsp-project.json`; images are handled separately.

## Coding style for QSP files

Follow the existing project style:

- Use a header at the top of new or replaced files:
  - `FILE: ...`
  - `MODULE: ...`
  - `! [AI-WORKED] Текст переработан / дополнен ассистентом DD.MM.YYYY` — обязательная метка с датой (числом работы с файлом) при любом создании, переработке или дополнении текстовых/сценарных файлов (`*_text.qsps`).
- QSP locations use this pattern:
  - `#LocationName`
  - code body
  - `---`
- Keep commands on separate lines.
- For one-line combined commands, use `&` only when it matches the existing style.
- Avoid unnecessary inline comments in QSP code.
- Big text blocks should usually go into separate `*_text.qsps` files.
- **Narrative output: `*p` vs `*pl` (no glued text):**
  - `*pl` — new line in the main text window. Use for separate paragraphs, each line of a document/record, dialogue lines, and any block that must not stick to the previous line.
  - `*p` — continues on the **same line** as the previous `*p` (no line break). Multiple `*p` in a row glue together; without a trailing space you get `читаемый:— Родился`, `ЛермонтЗасвидетельствовал`, etc.
  - Default for `*_text.qsps` and multi-sentence scenes: **`*pl` per paragraph**.
  - Use consecutive `*p` only for intentional inline flow (one long paragraph); then end each `*p` string with a **trailing space** before the next `*p`.
  - After a colon that introduces a quoted block or list (e.g. certificate text), add `*pl ' '` or switch following lines to `*pl`.
- Preserve existing variable naming conventions.
- Avoid renaming existing variables, locations, or files unless the user explicitly asks for a refactor.
- Always check that every `if` has its matching `end`.
- Avoid duplicate location names.
- **Обращение к ГГ (Стефану) в повествовании:**
  - Описание действий и мысли главного героя всегда строятся на **«ты»** (*«Ты подходишь»*, *«Ты поправил»*, *«Ты видишь»*).
  - Никакого «Вы / вы» при описании действий ГГ (*«Вы подошли»* $\rightarrow$ *«Ты подошёл»*).
- **Стилистика описаний и диалогов (канон нарратива):**
  - **Запрет на запахи окружения:** полностью исключать запахи («запах пива», «затхлый дух», «аромат мяса», «дух пыли и пота»). Вместо запахов — физические действия, движения и визуальные детали: что сделала (*поправила грудь, прижала поднос к бедру*), куда посмотрела (*на штаны между ног, на пояс, в глаза*).
  - **Минимум прилагательных (не более одного описательного прилагательного):** не нагромождать цепочки эпитетов. Использовать не более одного описательного прилагательного на предмет или действие (*«тяжёлая кружка»*, а не *«огромная, тяжёлая, пенная кружка»*). Текст должен быть ёмким, сухим и динамичным, с упором на глаголы действия.
  - **Вариативность по коррупции и откровению (не один вариант сцены):** не писать статичные тексты без развилок. В сценах и диалогах обязательно учитывать `FamilyCorruptionStage` (0–5) и уровень откровения (`otkroven[$npc]`):
    - *Низкая коррупция (Stage 0–1):* целомудренные, сдержанные реакции, строгие семейные границы, холодность к пошлостям и защита личного пространства.
    - *Средняя коррупция (Stage 2–3):* лёгкий флирт, намёки, раскованность, признания в сокровенных слабостях.
    - *Высокая коррупция (Stage 4–5):* раскованное поведение, демонстрация тела, откровенный разврат, похотливые взгляды на пах Стефана, отсутствие ложного стыда.
    - Всегда оценивать уместность по условиям сцены: определять, требуется ли в данный момент откровенный/похотливый диалог или, напротив, сдержанная реакция низкой коррупции.

### USER-OWNED TEXT (do not overwrite prose)

Files marked **`USER-OWNED TEXT`** in the header are authored/edited by the user for narrative tone.

| File | Notes |
|------|--------|
| `modules/actions/tavern/girl_work_policy_talk_text.qsps` | policy talk / thoughts / set |
| `modules/actions/tavern/girl_work_policy_assignment_reaction_text.qsps` | reactions to policy 1–3 |
| `modules/events/becky/becky_home_chain_text.qsps` | Becky home chain |
| `modules/events/becky/becky_dance_text.qsps` | Becky dances |
| `modules/actions/dialogs/girl_talk_becky_text.qsps` | Becky talk |
| `modules/events/eddie/eddie_arc_text.qsps` | Eddie arc |
| `modules/events/visits/sunday_amanda_lizette_text.qsps` | Amanda + Lizette overhear (moved to visits) |
| `modules/events/church/church_spy_lizette_text.qsps` | church spy Lizette |
| `modules/events/hall/hall_family_reactions_text.qsps` | family reactions to hall |
| `modules/events/hall/hall_family_state_text.qsps` | family state after hall choice |
| `modules/events/hall/hall_choice_family_talk_text.qsps` | family talk after hall choice |
| `modules/events/hall/hall_harassment_intro_text.qsps` | hall/kitchen harass intro T1–T3 (**WIP** — владелец допишет; не трогать prose) |
| `modules/events/hall/hall_harassment_text.qsps` | harass after / reaction / talk-recall |
| `modules/events/hall/hall_event_choice_thoughts_text.qsps` | Stefan thoughts before hall choice |
| `modules/events/hall/girl_policy_response_text.qsps` | policy response in scene |
| `modules/events/hall/girl_policy_response_consequences_text.qsps` | policy response thought tail |
| `modules/events/hall/girl_policy_scene_variations_text.qsps` | policy scene variation prose |
| `modules/events/hall/girl_policy_response_talk_text.qsps` | talk «как выполнила правило» |
| `modules/events/kitchen/kitchen_harassment_text.qsps` | kitchen harass entry / hall reaction |
| `modules/events/kitchen/kitchen_lewd_sandra_text.qsps` | kitchen lewd Sandra scenes |
| `modules/events/kitchen/kitchen_customer_event_text.qsps` | kitchen customer conflict |
| `modules/events/hall/noble_attack_text.qsps` | noble conflict in hall |
| `modules/actions/dialogs/girl_talk_sandra_text.qsps` | Sandra girl talk |
| `modules/actions/dialogs/girl_talk_personal_text.qsps` | personal talk |
| `modules/actions/dialogs/girl_talk_tavern_text.qsps` | tavern talk |
| `modules/actions/sex/sex_scene_text.qsps` | SexScene narratives (router & shared) |
| `modules/actions/sex/sex_scene_text_amanda.qsps` | SexScene Amanda narratives |
| `modules/actions/sex/sex_scene_text_clarissa.qsps` | SexScene Clarissa narratives |
| `modules/actions/sex/sex_scene_text_inga.qsps` | SexScene Inga narratives |
| `modules/events/amanda/home/amanda_home_first_sex_text.qsps` | Amanda home first sex |
| `modules/events/family/birth_certificate_text.qsps` | birth certificate |
| `modules/events/sandra/sandra_staff_girls_reaction_text.qsps` | staff hire reactions |
| `modules/events/family/act1_moral_unlock_text.qsps` | Act1 moral morning thoughts |
| `modules/actions/dialogs/sandra_birth_reveal_text.qsps` | Sandra reveals Stefan birth / Lermont |
| `modules/locations/town/mayor_office_text.qsps` | mayor office / clerk / first talk / magistrate |
| `modules/events/family/family_council_text.qsps` | family dinner council (6 screens) → liberation gate |
| `modules/events/hall/hall_missing_amanda_text.qsps` | Amanda missing scenes (**USER-OWNED / ЗАВЕРШЕНО** — не трогать без явного запроса пользователя; при любых изменениях, даже пакетных, спрашивать пользователя) |
| `modules/events/hall/hall_missing_agent_melissa_text.qsps` | Melissa missing scenes (**USER-OWNED / ЗАВЕРШЕНО** — не трогать без явного запроса пользователя; при любых изменениях, даже пакетных, спрашивать пользователя) |
| `modules/events/hall/hall_missing_agent_sandra_text.qsps` | Sandra missing scenes (USER-OWNED) |
| `modules/events/sandra/sandra_lermont_letter_text.qsps` | Sandra Lermont letter |
| `modules/actions/dialogs/sandra_lermont_letter_talk_text.qsps` | talk with Sandra about Lermont letter |
| `modules/locations/shops/irma_dance_dress_text.qsps` | Irma dance dress buy / try |
| `modules/locations/shops/irma_uniform_offer_text.qsps` | Irma uniform offer dialog |
| `modules/locations/shops/irma_uniform_orders_text.qsps` | Irma uniform orders dialog |
| `modules/events/dance/friday_dance_text.qsps` | Friday dance speeches and rumors |
| `modules/events/church/church_sunday_service_text.qsps` | Sunday morning church service texts |
| `modules/events/sandra/sandra_draupnir_friday_text.qsps` | Sandra Friday Draupnir visits |
| `modules/events/amanda/legare/amanda_legare_street_intercept_text.qsps` | street intercept / fight / police / wake-up texts |
| `modules/events/amanda/legare/amanda_legare_backyard_text.qsps` | backyard peeping behind barrels texts |
| `modules/events/amanda/legare/amanda_legare_dance_arc_text.qsps` | complete Legare Friday dance arc texts (notice, invite, dance, observe, after-dance, 5th Friday race) |
| `modules/events/amanda/legare/amanda_legare_talk_text.qsps` | talk about Legare aftermath texts (Amanda, Melissa, Clarissa) |
| `modules/events/amanda/legare/amanda_legare_spy_text.qsps` | backyard spy peeping on Amanda and Legare texts |
| `modules/events/amanda/neighbor_boys/amanda_neighbor_boys_text.qsps` | Amanda backyard neighbor boys encounters texts |
| `modules/events/amanda/neighbor_boys/amanda_boys_giant_text.qsps` | Peter the giant blacksmith encounters texts |
| `modules/events/amanda/neighbor_boys/amanda_boys_brothers_text.qsps` | Jens and Bruno brothers encounters texts |
| `modules/events/amanda/neighbor_boys/amanda_melissa_training_text.qsps` | Amanda and Melissa night stretch training texts (3 visits) |
| `modules/events/amanda/home/amanda_home_anal_text.qsps` | Amanda home anal arc texts (room talk, cucumber, peeping, first anal) |
| `modules/events/amanda/neighbor_boys/amanda_boys_curved_text.qsps` | Otto the curved boy encounters texts |

**Rules for agents:**

- Do **not** rewrite, “polish”, or regenerate the prose in these files without an explicit user ask («можно править тексты» / equivalent).
- **`hall_missing_amanda_text.qsps`** и **`hall_missing_agent_melissa_text.qsps`** полностью завершены: не трогать файлы без прямого запроса пользователя. Если требуются какие-либо изменения (даже пакетные/структурные), **обязательно сначала спросить пользователя**.
- Before any redesign or bulk rewrite of these files — **ask the user first**.
- If a bugfix must touch the file: change **only** structure/logic/`if`/`end`/gates; **keep the user’s strings** verbatim unless the user is fixing typos themselves.
- Prefer reporting typos/logic notes in chat over silent rewrites.
- When the user adds more files to this list — mark header `USER-OWNED TEXT` and extend this table.

## Patch delivery style

When giving file patches or replacement archives to the user, use this format:

- **Файл**
- **Архив** — path starting from `modules/...` when applicable
- **Класть с заменой**
- **Доп. инструкции**

Hooks, such as `#GirlTalk` insertion blocks, should be provided as text in the chat unless the user asks for a full archive or direct repository commit.

## Direct repository edits

When editing GitHub directly:

- Prefer small focused commits.
- Use clear commit messages in English or Russian.
- Do not mix unrelated changes in one commit.
- Do not change generated files unless the user asks.
- Do not delete files unless the user clearly approves it.
- After changing a file, summarize exactly what changed.

## Response style for agents

When answering the user:

- Answer in Russian unless the user asks otherwise.
- Be practical and step-by-step.
- For Git/GitHub questions, give exact PowerShell commands when useful.
- Do not ask unnecessary confirmation when the requested change is clear.
- If something is uncertain, say so clearly.
- Do not pretend a build or test was run unless it was actually run.

## Safety and quality

Before proposing or committing code:

- Check that location names are unique.
- Check for missing `end` statements.
- Check that new files are located in connected folders, unless the user intentionally wants inactive files.
- Do not break the current QSP build structure.
- Avoid changing story direction without user approval.
