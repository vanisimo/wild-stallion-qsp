# AGENTS.md

Instructions for ChatGPT, Codex, and other AI coding agents working on this repository.

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

### USER-OWNED TEXT (do not overwrite prose)

Files marked **`USER-OWNED TEXT`** in the header are authored/edited by the user for narrative tone.

| File | Notes |
|------|--------|
| `modules/actions/tavern/girl_work_policy_talk_text.qsps` | policy talk / thoughts / set |
| `modules/actions/tavern/girl_work_policy_assignment_reaction_text.qsps` | reactions to policy 1–3 |
| `modules/events/becky/becky_home_chain_text.qsps` | Becky home chain |
| `modules/events/becky/becky_dance_text.qsps` | Becky dances |
| `modules/events/becky/becky_talk_text.qsps` | Becky talk |
| `modules/events/eddie/eddie_arc_text.qsps` | Eddie arc |
| `modules/events/amanda/amanda_liza_talk_text.qsps` | Amanda + Lizette overhear |
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
| `modules/actions/dialogs/girl_talk_family_text.qsps` | family talk |
| `modules/actions/sex/sex_scene_text.qsps` | SexScene narratives |
| `modules/core/gifts/gift_simple_text.qsps` | gifts cheap/expensive |
| `modules/events/family/amanda_home_first_sex_text.qsps` | Amanda home first sex |
| `modules/events/family/birth_certificate_text.qsps` | birth certificate |
| `modules/events/sandra/sandra_staff_girls_reaction_text.qsps` | staff hire reactions |
| `modules/events/family/act1_moral_unlock_text.qsps` | Act1 moral morning thoughts |
| `modules/actions/dialogs/sandra_birth_reveal_text.qsps` | Sandra reveals Stefan birth / Lermont |
| `modules/locations/town/mayor_office_text.qsps` | mayor office / clerk / first talk / magistrate |
| `modules/events/family/family_council_text.qsps` | family dinner council (6 screens) → liberation gate |
| `modules/events/hall/hall_missing_amanda_text.qsps` | Amanda missing scenes (**USER-OWNED / ЗАВЕРШЕНО** — не трогать без явного запроса пользователя; при любых изменениях, даже пакетных, спрашивать пользователя) |
| `modules/events/hall/hall_missing_agent_melissa_text.qsps` | Melissa missing scenes (USER-OWNED) |
| `modules/events/hall/hall_missing_agent_sandra_text.qsps` | Sandra missing scenes (USER-OWNED) |

**Rules for agents:**

- Do **not** rewrite, “polish”, or regenerate the prose in these files without an explicit user ask («можно править тексты» / equivalent).
- **`hall_missing_amanda_text.qsps`** полностью завершён: не трогать файл без прямого запроса пользователя. Если требуются какие-либо изменения (даже пакетные/структурные), **обязательно сначала спросить пользователя**.
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

## Game systems and current design constraints

The project is a medieval tavern management and character-event QSP game.

Current core design constraints:

- The tavern hall workers are Amanda, Melissa, and Sandra.
- Georgette and Lizette may appear later, but they are not regular hall workers.
- Player energy was removed.
- Player orgasm limit system exists:
  - `max_daily_cum`
  - `daily_cum_count`
  - `RegisterPlayerCum`
- Useful conversations are limited:
  - 1 important conversation per part of day
  - maximum 3 important conversations with one NPC per day
  - normal small talk remains available
- NPC menu should not use a manual “Close” button; it closes on cursor leave.
- Dropdown `GirlTalk*Menu` lists must not include a manual «Вернуться» / «Закрыть» item; exit is cursor-leave only (`GirlTalkSessionEnd`).
- NPC talk buttons fall into three classes:
  - **Arc one-shot** — story beat fires once (`*Done = 1`), button hidden afterward (example: Lizette spy talks, Eddie).
  - **Lore pool** — button stays; each visit rotates `GeorgetteTalk*Story` counter and picks the next text (port, clients, sex, family, children, bio).
  - **Georgette church** — single button «О церкви и отце Герхарде»: intro once, after first spy E once, then weekly recap after Sunday spy scenes 2–7 (`GeorgetteChurchRecapPending`), night port only for recap.
- Game calendar week: `week` 1 = Monday … 7 = Sunday (`get_date_time_names.qsps`).
- **Action panel (`act`) and item panel (`addobj`):**
  - Every `act` must have an icon (second argument). Prefer `gs 'ActUiPrepare', 'Label', 'key'` then `act $ActUiLabel, $ActUiIconPath:` — keys via `#PanelUiIconPath` group `act`; unknown → `generic`.
  - Item panel buttons (`addobj`) must use an icon — via `#PanelUiAddGlobalButton` / `#PanelUiIconPath` group `item`, not bare `addobj` without image.
  - Icon assets: `images/common/ui/actions/*.png` and `images/common/ui/*.png` (items) — **32×32 px** (was 48×48).
  - Dropdown `MenuUiAdd` menus are **not** covered by this rule (they already use menu icons separately).
  - After talk text screens may keep `act` «Вернуться» via `#GirlTalkAddReturnButton` (`return` icon).
- **VISUAL ON EVERY SCREEN (no empty screens) — канон для всей игры:**
  - **Нет экранов без картинки.** Открыли сундук → картинка сундука; окно → окно; секс на улице → кадр секса; клиент на кухню → дверь/занавеска с входящим; уговор / missing / harass / talk outcome — всегда visual.
  - **Пока ассета нет** — **заглушка** `images/common/hall_scene_stub.png` (или тематический stub), **не** пустой main text.
  - **Потом** подменить path на real webp/png — логику экрана не ломать.
  - **Подпись / ключ ассета обязателен**, чтобы не терять смысл кадра: `gs 'SceneShowVisual', 'images/…/key_path', 'короткая подпись: что на кадре'`.
  - Helper: `#SceneShowVisual` in `modules/core/show_image/show_image_helpers.qsps` — stub + `[VIS] caption` + debug future path. Real art: `SceneArtUseReal = 1` (или per-system `HallMissingArtUseReal` / `SandraKitchenArtUseReal`).
  - **Код (logic/dispatch), не USER-OWNED prose:** image call **до** `*pl` сцены (`PrintText` / location body / resolve), не размазывать `ShowImage` по строкам narrative без нужды.
  - **Новые сцены / agent / events:** в header файла или ASSET-*.md — список ключей (path + подпись). Неизвестный кадр — **спросить владельца**, не выдумывать сюжет арта.
  - **Locations** (`TavernMain`, `Kitchen`, street…): на входе location image / work image уже есть; **event overlays** (notice, chest, window, sex) — отдельный `SceneShowVisual` на каждый *clr-экран события.
  - Agent missing: `HallMissingGirlShowImage` + caption; kitchen hook Сандры: `SandraKitchenShowImage` → `SceneShowVisual`.
- Work assignment:
  - maximum 2 jobs per girl
  - efficiency drops when a girl has 2 jobs
  - income and reputation depend on efficiency

## Main character

Main character file:

- `modules/npc/town/steve.qsps`

Character voice and boundaries (canon):

- `docs/design-stefan-voice.md`

Main character:

- Stefan Longcock / Стефан Лонгкок
- age: 20
- start location: `TavernMain`
- archetype: young former slacker, rough-humorous, status-proud inn owner; Act 1 not yet bold — testing boundaries; women notice his status but he cannot use it well yet; lewd thoughts OK, actions slower; alcohol background only, not narrative focus; friendly but does not give away what is his without being convinced

Known stats include:

- `strength = 65`
- `stamina = 70`
- `penis_size = 18`
- `sexual_endurance = 0`
- `max_daily_cum = 2`
- `daily_cum_count = 0`
- `management = 20`
- `trading = 15`
- `charisma = 40`
- `drunk = 0`
- `tired = 0`

## Calendar and schedule

Current game calendar:

- year: 1100
- start date: Monday, January 1
- parts of day:
  - morning
  - noon
  - evening
  - night

Rules:

- Tavern is closed at night.
- Most business works from morning to evening.
- Friday evening: dances; shops/businesses are closed, the mayor speaks before dances.
- Sunday: ordinary business is closed; morning church service and NPC socializing; confession around noon.

## Tavern systems

Important tavern values include:

- money
- reputation
- scandal
- visitors
- kitchen quality
- hall quality
- cleanliness
- staff efficiency
- stock of food, wine, and beer

Daily summary should include:

- food income
- wine income
- beer income
- expenses
- final profit
- stock spent
- remaining stock
- staff efficiency
- money
- tavern reputation

## Story map

Current act structure:

1. Tavern and family
   - work assignment
   - bar counter
   - harassment
   - reaction choices
   - family trust and tension
   - first intimate stages
   - conversations about the past

2. Town connections
   - Becky
   - Legare
   - Clarissa
   - Inga
   - Eddie
   - Irma
   - carpenter
   - dances

3. Dirty side of town
   - church
   - confession
   - spying
   - priest
   - Georgette
   - Lizette
   - musicians
   - rumor and scandal systems

4. Nobility
   - paper about the real father
   - mayor office
   - taxes
   - clothing/status paths
   - clean/social/dirty paths

## Family systems

Global family-related variables and ideas:

- `FamilyTrust`
- `FamilyTension`
- `FamilyCorruptionStage` from 0 to 5

General meaning:

- stage 0: decent/respectable family boundaries
- stage 5: family boundaries are broken

Early NPC/NTR content should increase tension. Later systems may increase tolerance depending on prior choices.

## Character branches

### Amanda

Amanda is central in Act 1.

Known Amanda scales:

- `AmandaTrustStefan`
- `AmandaRebellion`
- `AmandaLizaInfluence`
- `AmandaLegareInterest`
- `AmandaPublicAttention`
- `AmandaWorkDiscipline`
- `AmandaSecretiveness`
- `AmandaPlayerPath`
- `AmandaNpcPath`
- `AmandaScandalLevel`

Important Amanda event themes:

- first harassment
- aftermath conversation
- Lizette first conversation
- secret Lizette visit
- first dance with Stefan
- Legare notices Amanda
- dance with Legare
- risk of leaving
- revealing uniform
- escape from work
- confession
- first player/NPC path choice
- player learns about NPC path
- family conversation

### Melissa

Voice (canon, hall/clients): **bookish know-it-all like Hermione Granger (Harry Potter)** — type only, not a crossover; not a mean “prostitute bitch”. Finds male lust **funny, predictable, naive**; eye-rolls; ironic digs at crude euphemisms; bargains with a light smirk; takes silver **for paper, books, poetry**. Full write-up: `docs/design-npc-voices.md` §3.

Known Melissa scales:

- `MelissaTrustStefan`
- `MelissaRespectStefan`
- `MelissaJealousy`
- `MelissaControlNeed`
- `MelissaClarissaBond`
- `MelissaScandalTolerance`
- `MelissaMusicianInterest`
- `MelissaPlayerPath`
- `MelissaNpcPath`
- `MelissaFamilyConcern`

Important Melissa event themes:

- protection in the hall
- ignoring her concerns
- anxiety about Amanda
- warning about Legare
- Clarissa conversation
- jealousy
- musician attention
- back room/subsidiary room scenes
- first player/NPC path choice
- hall bargain / missing — ironic client talk (not cruel whore voice)

### Sandra

Known Sandra scales:

- `SandraTrust`
- `SandraRespect`
- `SandraFamilyConcern`
- `SandraMoralResistance`
- `SandraPragmatism`
- `SandraBeckyBond`
- `SandraChurchPressure`
- `SandraCarpenterSecret`
- `SandraPast`

Sandra arc:

- moral control
- church
- hypocrisy
- Becky
- father secret
- acceptance

### Lizette

Lizette should enter through the port.

Current premise:

- once per week a ship from the capital arrives in the small town
- it brings exotic goods and gifts for NPCs
- this creates a natural way for Lizette to meet Amanda

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
