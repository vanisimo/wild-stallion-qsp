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

- `modules/core/init/`
- `modules/core/time/npc_talk_limits.qsps`
- `modules/core/show_image/image_debug_random.qsps`
- `modules/core/tavern/tavern_event_state_core.qsps`
- `modules/actions/tavern/`
- `modules/actions/sex/`
- `modules/menu/`
- `modules/events/kitchen/`
- `modules/events/hall/`
- `modules/events/tavern/`
- `modules/events/lizette/`
- `modules/locations/`
- `modules/npc/`
- `modules/npc/girls/amanda/`
- `modules/npc/girls/melissa/`
- `modules/npc/girls/sandra/`
- `modules/debug/`

The folder `modules/old` is considered old/disabled material and should not be connected or reused without explicit instruction.

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
- Preserve existing variable naming conventions.
- Avoid renaming existing variables, locations, or files unless the user explicitly asks for a refactor.
- Always check that every `if` has its matching `end`.
- Avoid duplicate location names.

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
