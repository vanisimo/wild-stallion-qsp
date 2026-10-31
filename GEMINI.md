# GEMINI.md — Игровые системы, UI, визуальный канон, лор и персонажи «Дикий Жеребец»

Дополнение к `AGENTS.md` (разделено на два файла для соблюдения лимита Antigravity 24 КБ на один файл правил с запасом ~10 КБ в каждом файле).

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
- **Религия и лексика по лору:**
  - Верховное божество: **Ильматер** (церковь Ильматера, слуга Ильматера, благословение Ильматера).
  - Никаких христианских терминов и слов вроде «боже», «ради бога», «о боги», «Господи» — вместо них используются **«Ильматер»**, **«Ильматер всеблагой»**, **«ради Ильматера»**, **«видит Ильматер»**.
  - Священный символ и ритуальный жест: **святой / священный круг**, **знак Круга** (не крест / не креститься / не осенять крестом; персонажи **«осеняют себя святым кругом»**, **«очерчивают круг»**).
  - **Чистота и бритьё (порошок «Таро» / благословение Ильматера):**
    - Серый порошок, пахнущий травой и щёлочью. Разводится водой, намазывается на тело — и любые нежелательные волосы бесследно пропадают, оставляя кожу идеально чистой и гладкой без бритв и порезов.
    - Дар Ильматера: каждый житель может свободно и бесплатно взять его в храме из глиняных кувшинов у алтаря (Ильматер не только заповедал держать всё в чистоте, но и дал для этого средство).
    - Канон чистоты: женщинам заповедано снимать волосы на теле полностью; мужчинам — лицо начисто, на теле только аккуратная полоска/треугольник на лобке над удом. Неряшливость и лень считаются дикостью и отступлением от чистоты Ильматера.
- **Город, власть, церковь и вектор герцогини (канон фронтира):**
  - **Настроение города и фронтира:** здесь чужды упадничество, ханжество, чувство вины за плотские радости и столичное показное пуританство. Люди не осуждают друг друга, радуются каждому дню и живут жадно, как будто завтра не настанет.
  - **Авторитет церкви:** прихожане и простые горожане воспринимают церковь Ильматера как абсолютный, непререкаемый авторитет. Слова священника с амвона принимаются на веру безоговорочно, без критики и сомнений.
  - **Вектор герцогини и гибкость церкви:** герцогиня задаёт генеральный вектор освоения фронтира — бурный рост населения, плодовитость, скрещивание и смешение семени на новых землях. Поэтому церковь Ильматера на фронтире не воюет с местными религиями гномов, орков и эльфов, а гибко приспосабливает их под себя, выдавая за священное наследие Ильматера.
  - **Истинная цель отца Герхарда:** священник вовсе не намерен осесть в глуши; он всеми силами стремится выслужиться перед герцогиней, чтобы **вернуться в столицу**. На проповедях он рьяно продвигает заветы Ильматера о скрещивании и союзе плоти, а попутно пользуется покорностью паствы, стремясь **оприходовать всех красивых горожанок** в округе.
  - **Священник и мэр (конфликт властей):** на почве аппетитов Герхарда к местным женщинам у него возник конфликт с мэром города. Однако мэр отступил и не стал вступать в войну: он трезво рассудил, что священник здесь — **временщик** (скоро уедет назад в столицу), а **с горожанок не убудет**.

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
