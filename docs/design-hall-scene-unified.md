# Design: единый паттерн сцен зала (harassment / play / missing)

**Статус:** **канон v2 утверждён + код core готов (2026-07)** — сквозное приставание; lewd/missing auto сняты; play coach; memory/rumor/knowledge probe **PASS**.  
**Тексты:** intro play-хвосты есть; base T1–T3 / resolve play — доработка prose.  
**Связь:** `docs/economy.md` §0c, `docs/design-hall-harassment.md`, `docs/state.md`

---

## 0. КАНОН v2 — сквозное приставание (утверждено)

### 0.1 Суть

Один поток **приставания** (зал / кухня).  
**Play** (подыгрывание) — stance внутри сцены, **не** отдельный event-roll.  
**Missing** — только исход из **play** (путь **α**).  
Отдельный `HallLewdBehaviorTryAutoStart` / lewd в dispatcher — **не канон** (снять при миграции).

```
ROLL harass
  → girl + client type + gesture + form
  → pleasant? (таблица type × girl)
  → stance: resist | endure | play
  → intro + thoughts
  → ОДИН раз: Защитить / [Наблюдать / Отвернуться]
  → resolve на виду
  → если play + gейты + RAND → MISSING-меню → missing resolve → БЕЗ policy (P0)
  → иначе → policy 1/2/3 (после ужина) → Вернуться
```

**Harass не выключается** при высоком уровне — меняются stance, жест, форма.  
**Не:** `if play_unlocked: harassment = OFF`.

### 0.2 Форма (видимость)

Два типа формы + nop на короткой (**не** «u2» как третий костюм):

| Код | Вид | При наклоне / руке / юбке |
|-----|-----|---------------------------|
| **u0** | подол ниже колена, середина голени | талия, край; попа почти не «объект» |
| **u1** | подол выше колена, середина бедра (**после** появления/покупки короткой формы) | **попа**, бедро; при задирании — бельё если есть |
| **u1+nop** | та же u1 **без трусиков** (поздний этап) | **промежность**; тон **не** паника Act1 |

Слой тела — **модификатор** везде, где длина подола / отсутствие трусиков видно.

### 0.3 Stance

| Stance | Смысл | Когда |
|--------|--------|--------|
| **resist** | возмущение | early / unpleasant / policy1 |
| **endure** | терпение | mid+; **до coach — потолок** |
| **play** | подыгрывание (**редко**) | `PlayCoached[girl]` + **pleasant** client + rare roll + personal/FamCorrupt |

До **PlayCoached:** play **запрещён** (даже high slut) — только resist \| endure.  
Policy 3 без coach **не** открывает play.

Старый код: `resist` / `mixed`≈endure / `provoke`≈play.

### 0.4 Обучение play (зал не обгоняет ГГ)

Play unlock — **подслушанные разговоры пар** (не диалог ГГ с «наставником»).  
**Когда:** воскресенье, фаза `sunday_visits` (день / вечер).  
**Как:** ГГ подслушивает у двери / у закрытой лавки; one-shot; порядок жёсткий.

| Порядок | Пара | Где | Смысл | Флаг |
|---------|------|-----|--------|------|
| 1 | **Аманда ↔ Лизетта** | комната Аманды (`AmandaLizaRoomDoorPeek`) | ниже наклонись / чуть сисек / покрути попой | `PlayCoached['amanda']` |
| 2 | **Мелисса ↔ Кларисса** (после Аманды) | лавка Легаре (`SundayVisitClarissaMelissa`) | «эта **мелкая** крутит жопой» → «ещё посмотрим, кто лучше» | `PlayCoached['melissa']` |
| 3 | **Сандра ↔ Бекки** (после Мелиссы) | лавка Бекки (`SundayVisitBeckySandra`) | «девки стыд потеряли» / «у тебя тоже есть чем покрутить» у плиты | `PlayCoached['sandra']` |

Тексты: `hall_play_coach_text.qsps`. Apply: `HallPlayCoachApply`.  
Debug: `gt 'HallPlayCoachStart', 'amanda'` (replay сцены).  
**Не:** кнопки в GirlTalk у Лизетты / Клариссы / Бекки.

Случайный клиент **не** учит play.

### 0.5 Клиенты и «приятный»

Только **таблица** type × girl (без истории чаевых).  
Один client type на сцену.

| id | Кто | Поведение | Pleasant |
|----|-----|-----------|----------|
| **drunk_guest** | **пьяный горожанин** | грубо, шумно, без предлога | **всегда нет (−−)** — антипатия у **всех** девушек; play/missing **никогда** |
| **rich_merchant** | **купец / торговец** | монета, уверенность, «право внимания» | по таблице |
| **craftsman** | **мастеровой / горожанин** | запанибрата, «свой» | по таблице |
| **traveler** | **военный / моряк** | чужой, проверяет границы дома | по таблице |

**Веса roll клиента — разные** (не 25/25/25/25). Ориентир:

| Этап | drunk | merchant | craftsman | traveler |
|------|-------|----------|-----------|----------|
| Early (до/сразу после ужина) | выше (~35–40%) | mid | mid | ниже |
| Mid (FamCorrupt≥2–3) | mid | mid–high | mid | mid |
| Late / play-era | ниже (~15–20%) | high | mid | mid–high |

Плейтест: крутить; **drunk** остаётся частым «хамом», но **никогда** не ведёт в play.

Таблица pleasant (play/missing только при **+**):

| | drunk | merchant | craftsman | traveler |
|--|-------|----------|-----------|----------|
| **Аманда** | −− | ± | + | + |
| **Мелисса** | −− | + | − / ± | ± |
| **Сандра** | −− | + | + | − / ± |

± = endure возможен; play только если roll «как +» с низким шансом **или** трактовать ± как endure-only (жёстче: **± = не play**).  
**Канон по умолчанию:** play/missing только явный **+**; ± и − → max endure.

### 0.6 Missing — путь α + policy P0 (**утверждено**)

```
play на виду
  → один выбор protect / watch / ignore
  → resolve play
  → если gейты + RAND → MISSING
       → Вмешаться / Подсмотреть / Не вмешиваться
       → missing resolve
       → БЕЗ policy (P0)
       → Вернуться
  → иначе → policy 1/2/3
```

| Правило | |
|---------|--|
| Missing **только** из play | да |
| Отдельный rare missing без play | **нет** (канон v2) |
| Policy после missing | **нет (P0)** |
| **Protect** на play | missing chance **0%** |
| **Watch / ignore** на play | missing chance **~15–25%** (плейтест) + gейты |
| Хвост вместо policy | 1–2 абзаца / мысль; правило — later talk |

### 0.7 Кнопки по этапам

| Этап | Stance | Кнопки | Policy after |
|------|--------|--------|--------------|
| До ужина | resist | **только Защитить** | только «сдержанно» |
| После ужина, до coach | resist \| endure | **3 кнопки** | 1/2/3 |
| После PlayCoached | + rare **play** | **те же 3** (не второе lewd-меню) | 1/2/3 если **не** missing |
| Play → missing (α) | — | **missing-меню** | **нет (P0)** |

Отдельной кнопки «profit» **нет**.  
Play на виду = другой **текст / мысли / ставки**, не второй опросник.

| UI | Код | Тон |
|----|-----|-----|
| **Защитить** | `protect_hard` | harass: оборона; play: оборвать номер; missing: вмешаться |
| **Наблюдать** | `watch` | смотреть; missing: подсмотреть |
| **Отвернуться** | `ignore` | не вмешиваться |

Legacy: lewd `stop`→protect, `encourage`→ignore; missing `interrupt`→protect, `peek`→watch.

### 0.8 Где кто

| Место | Harass / play | Missing |
|-------|---------------|---------|
| **Зал** | Аманда, Мелисса | under_table, storage, stairs… |
| **Кухня** | Сандра | kitchen only |

Сёстры ≠ kitchen-play. Сандра ≠ hall-play. Cleaning-позы **нет**.

### 0.9 Pipeline UI

```
ЭКРАН 1 intro:
  header → image → сцена (artistic)
  → policy tint 1 строка (stats calc, без полной перепечати)
  → thoughts → кнопки
  НЕ: PolicyReaction + SceneVariation целиком (ломали структуру)

ЭКРАН 2 after:
  header → image (reaction) → итог выбора
  → offense → --- → policy talk + menu

play → missing: отдельный UI, без policy (P0)
```

### 0.10 Клиенты, жесты, перетекание (утверждено)

#### A. Общий поток

```
ROLL harass (зал | кухня)
  → girl + client + gesture(tier) + form(u0|u1|u1+nop)
  → pleasant? (drunk = всегда нет)
  → stance: resist | endure | play
  → на виду → 1× кнопки
  → resolve
       protect → никогда missing; policy если не missing-path
       watch/ignore + play → 15–25% missing (α) → missing UI → P0
       иначе → policy 1/2/3
```

**T3 (жёсткие жесты):** только при **FamCorrupt mid+** (ориентир `FamilyCorruptionStage >= 2` или `>= 3` — выровнять с кодом; **не** T3 в самом early Act1).  
**Under-table cock:** отдельная **harass**-ветка после `drop_coin` под столом → **flee | coin** only; touch/hold → high/missing, не early harass. **Да, оставляем.**

#### B. Зал — каталог жестов (Аманда / Мелисса)

| Tier | id | Жест | Form notes |
|------|-----|------|------------|
| 1 | `wrist` | за запястье / тянет к столу | u0+ |
| 1 | `waist` | талия при подаче | u0+ |
| 1 | `look` | взгляд (А: попа / М: декольте) | u1 сильнее |
| 1 | `pinch` | щипок бок / попа | u1 → попа |
| 2 | `ass_hand` | ладонь на попе | u1 / nop |
| 2 | `lap_pull` | тянет **на колени** (он сидит) | зал ok |
| 2 | `chest` | прижал к груди / декольте | |
| 2 | `behind` | сзади, трётся | |
| 3 | `skirt_up` | задрал юбку | u1 бельё / nop кожа |
| 3 | `wall` | прижал к стойке/стене, рука под юбкой | T3 mid+; **play → сильный шанс missing** |
| 3 | `drop_coin` | монета **под стол** → наклон → лапает | + cock sub-ветка gейты |
| 3 | `crotch_pull` | схватил / утянул → падение **сверху** | sub: `on_crotch` \| `on_face` (T3 mid+) |

**`crotch_pull` — два sub-исхода (roll или stage):**

| Sub | Кадр | resist / endure | **play** |
|-----|------|-----------------|----------|
| **`on_crotch`** | упала **сверху на пах** клиента (наездница к паху, не «лицо в пах как oral-поза по умолчанию») | резко вскочила / неловко отстранилась | сидит/елозит на паху; late — не паникует |
| **`on_face`** | упала **сверху на лицо** клиента | сразу слезла, стыд/злость | **поерзала на лице**; клиент **засунул язык**; **мокрое лицо** клиента; тон «весёлые / вкусные девчонки» (зал как кураж, не ужас) |

**Мелисса + `on_face` play (отдельный канон):**  
откидывается **назад**, чтобы язык клиента попал **в попу** / на анус; ей это **нравится** (как drop-nop); отдельные реплики; не «сломалась», а **участвует в веселье**.

Аманда на `on_face` play — мягче/смущённее куража, но при high play тоже может «не слезать сразу» (без обязательного анал-языка; то можно позже/выше stage).

#### C. Play-ответы на жест (зал) — канон тона

Один и тот же gesture; **play** меняет **её** действия:

| Жест | resist (кратко) | endure | **play** |
|------|-----------------|--------|----------|
| **щипок / попа** | одёрнула, осадила | терпит, уходит | **обернулась, улыбнулась, покрутила попой**; **наклонилась ниже**, чтобы было лучше видно |
| **колени** (`lap_pull`) | спрыгнула | секунда и встаёт | **сидит на коленях**, разговаривает, **крутит попой**, **задирает юбку выше**, **рука под юбкой**, **ноги шире** → **сильный шанс missing** (из watch/ignore) |
| **drop** | вылезла злая | монета и ушла | **покрутила попой**, **выгнула спину** для доступа; при **nop** трогают и **анус**; **Мелисса** — **отдельные реплики, ей это очень нравится** |
| **wall** | оттолкнула | терпит до «хватит» | **рука между ног**, **подмахивает**, **стоны**; при **nop** — **мокрые пальцы** → **сильный шанс missing** (кладовая / stairs / «увели») |
| **crotch_pull `on_crotch`** | резко вскочила | отстранилась | елозит сверху на паху; кураж зала |
| **crotch_pull `on_face`** | слезла, одёрнула юбку | коротко, стыд | **поерзала на лице**, язык клиента, **мокрые лица**, «вкусные девочки», **общее веселье**; Мелисса — **откинулась, язык в попу** |

**Тон late play (зал):** не «жертва в аду», а **распущенное веселье** витрины — смех соседей, мокрые рты/лица клиентов, девчонки «вкусные», хозяин решает: оборвать кутёж / смотреть / отвернуться.

#### D. Кухня — жесты (Сандра) и перетекание

| Tier | id | Жест |
|------|-----|------|
| 1 | `wrist_pass` / `lean_look` / `waist_stove` / `pinch_side` | проход, взгляд, плита, щипок |
| 2 | `hip_counter` / `corner_block` | к столу / угол |
| 3 | `skirt_up` / `wall_pantry` / **`drop_coin` (пол)** | без члена; visibility u1/nop |
| — | ~~lap как в зале~~ | **нет** |
| hard play | `hand_under` / `counter_sit` (late) / `rider_fall` | play only |

Перетекание кухни = то же, что зал: play → 15–25% missing → place **`kitchen` only** → P0.  
Drunk на кухне: harass resist/endure only.

#### E. Куда перетекает (сводка)

| Из | Условие | Во |
|----|---------|-----|
| T1–T3 + resist/endure | выбор Стефана | resolve на виду → **policy** |
| T1–T3 + play | protect | оборвал номер → **policy**, missing 0 |
| T1–T3 + play | watch/ignore | resolve play → **15–25% missing** (база) |
| **wall + play** | watch/ignore | missing chance **выше базы** (ориентир **~30–40%**) → storage / stairs |
| **lap_pull + play** | watch/ignore | missing chance **выше базы** (как §C) |
| **crotch_pull + play** | watch/ignore | чаще **дожать на виду** (веселье зала); missing **ниже** или 0 — сцена уже «шоу»; при roll — storage |
| missing | α | 2-е меню → resolve → **без policy** |
| drop_coin + under table + cock gейты | harass sub | **flee \| coin** (не play-обязателен) |
| drop/wall/lap + play | high | missing place по клиенту/локации |

**Wall → missing (канон):** play у стены (рука между ног / стоны) + Стефан не оборвал → логичный увод в **storage / stairs / полутёмное** (не обязательно under_table). Текст: «увела / увели», мокрые пальцы, продолжение без витрины → missing-меню.

**Missing place × клиент (ориентир):**

| Client | Зал | Кухня |
|--------|-----|-------|
| drunk | — (нет play) | — |
| merchant | under_table, storage | kitchen / pantry |
| craftsman | storage | kitchen |
| traveler (военный/моряк) | stairs, storage | kitchen rare |

#### F. Form × жест (везде, где видно)

| Form | Типично видно / трогают |
|------|-------------------------|
| u0 | талия, край, мало попы |
| u1 | **попа**, бельё при задирании/наклоне |
| u1+nop | **промежность**; drop play + **анус**; wall play **мокрые пальцы** |

Тон nop — поздний, не Act1-истерика.  
**Мелисса + стимуляция ануса (drop play nop)** — отдельные строки, **нравится**.

#### G. Утверждённые числа / флаги (блок 9)

| # | Решение |
|---|---------|
| 1 | Веса клиентов **разные** (см. §0.5) |
| 2 | **T3 только mid+ FamCorrupt** |
| 3 | Under-table cock = отдельный harass flee/coin — **да** |
| 4 | Missing из play: protect **0%**, watch/ignore **~15–25%** |
| 5 | Этот блок — канон в доке |

---

## 1. Три слоя UI

| Слой | Что | Когда |
|------|-----|--------|
| **Сцена** | harass (+ stance play) / missing из play | look / кухня / dispatcher |
| **Кнопки** | реакция Стефана | **один** раз на «на виду»; +missing если α |
| **Policy** | правило на будущее | после resolve **на виду**; **не** после missing (P0) |

Policy values: 1 сдержанно / 2 сама / 3 расковано.  
До ужина policy >1 режется. OffenseDays: AfterHarassApply (K=3).

---

## 2. HARASSMENT

| | |
|--|--|
| **Смысл** | Клиент лезет; она resist / endure / play (play после coach) |
| **Файлы** | `hall_harassment.qsps`, `kitchen_harassment.qsps` (+ слияние бывшего lewd) |
| **Кто** | зал: Аманда, Мелисса; кухня: Сандра |

Детали жестов/tier: `docs/design-hall-harassment.md` (обновить под v2 при миграции).

**Член:** монета под столом → flee \| coin (harass); touch/hold → high / missing path.

---

## 3. PLAY (бывший «lewd» на виду)

### 3.1 Смысл (v2)

Stance **play**: задержалась, не убрала руку, дольше наклон…  
**Не** отдельный auto-start.  
`hall_lewd_behavior*` / `kitchen_lewd_*` — **legacy до миграции**.

### 3.2 Где и кто

| Место | Кто |
|-------|-----|
| Зал | Аманда, Мелисса (после своих PlayCoached) |
| Кухня | Сандра (после Бекки) |
| Cleaning | **нет** |

### 3.3 Условия play (замена «soft-lewd gate»)

```
PlayCoached[girl] = 1
AND pleasant(client, girl)
AND FamilyLiberationGateOpen = 1
AND Act1MoralUnlocked = 1   (как семейная рамка)
AND FamilyCorruptionStage >= 3   (ориентир; уточнить при коде)
AND rare roll
AND (personal: slut / NpcPath / policy3+agr — веса, не замена coach)
```

Без coach → play chance = 0.

### 3.4 Жесты / hard (ориентир; каталог жестов — отдельно)

Зал (пример): bend, waist, sit_near, lap; hard-эскалация по tier + form.  
Кухня: не копировать зал 1:1; drop_coin (visibility u0/u1/nop); без harass-lap на табурете; hard play — hand_under / counter_sit (late) / rider_fall (потянул, оба упали, она сверху; early↑ / late спокойно) — **уточнять при кухне-pass**.

**Убрано:** kiss+шнуровка; cleaning floor/ladder/fall; face-to-crotch как «номер» на кухне.

### 3.5 Legacy-файлы (до миграции)

- `modules/events/hall/hall_lewd_behavior.qsps`  
- `modules/events/hall/hall_lewd_behavior_text.qsps`  
- `modules/events/kitchen/kitchen_lewd_sandra.qsps`  
- `modules/events/kitchen/kitchen_lewd_sandra_text.qsps`  

---

## 4. MISSING

### 4.1 Смысл

Её **нет** на месте. Уединение с клиентом — не витрина в центре зала.  
**Вход (v2):** только из **play** после выбора на виду (α).

### 4.2 Где и кто

| place | Кто |
|-------|-----|
| `under_table` | Аманда, Мелисса (A1: также harass coin/cock) |
| `storage` | Аманда, Мелисса |
| `stairs` | Аманда, Мелисса |
| `kitchen` | **только Сандра** |
| `second_floor` / `room_invite` | **пока нет** |

### 4.3 Гейты missing (из play)

```
stance == play (уже прошли)
AND pleasant client
AND FamilyLiberationGateOpen = 1
AND Act1MoralUnlocked = 1
AND FamilyCorruptionStage >= 3
AND personal mid/high (slut / stage — плейтест)
AND RAND
```

Числа stage/slut из старого § — **ориентир**, не отдельный missing-roll без play.

### 4.4 Лестница private acts (peek)

Одинаковая логика для сестёр и Сандры; у Сандры в **mid** + сиськи.

| Этап | Содержание |
|------|------------|
| **Early** | петтинг; оголила сиськи → дала полизать; показала киску → дала потрогать; **потрогала член** |
| **Mid** | **дрочка** ему и ей; затем **минет** и **куни** |
| **Mid + Сандра** | + **работа сиськами** |
| **Late** | минет → **яйца, глубокий заглот**; куни → **анилингус** |

### 4.5 Кнопки missing

| UI | Смысл |
|----|--------|
| Защитить | **вмешаться** |
| Наблюдать | **подсмотреть** |
| Отвернуться | **не вмешиваться** |

После resolve — **без policy (P0)**.

### 4.6 Файлы

- `modules/events/hall/hall_missing_girl.qsps`  
- `modules/events/hall/hall_missing_girl_text.qsps`  

---

## 5. Веса осмотра зала (после ужина, v2)

| Состояние | Harass roll | Play stance | Missing |
|-----------|-------------|-------------|---------|
| liberation, FamCorrupt &lt; 3 | ~100% | 0 | 0 |
| FamCorrupt ≥3, no coach | высокий | 0 (endure max) | 0 |
| coach + personal mid | высокий | rare | 0 / из play rare |
| coach + personal high | ниже/mid | выше (всё ещё rare) | mid из play |
| high + scandal | mid | mid | выше из play |

Отдельной колонки «lewd event %» **нет**.

---

## 6. Стык harass ↔ play ↔ missing

| Ситуация | Система |
|----------|---------|
| Клиент лезет, resist / endure | **harass** |
| Play (coach + pleasant) | **harass** + stance play |
| Ушла с ним / пропала | **missing** (только из play, α) |
| Монета + член под столом: flee/coin | **harass** |
| Под столом touch/hold | high play / **missing** |
| Policy после на виду | **да** |
| Policy после missing | **нет (P0)** |

---

## 7. Пороги — сводная (v2)

| Гейт | Значение |
|------|----------|
| 3 кнопки + policy 2–3 | `FamilyLiberationGateOpen` |
| **Play** возможен | `PlayCoached[girl]` + pleasant + FamCorrupt≥**3** + rare + personal веса |
| **Missing** | **только** из play + gейты + RAND |
| Policy after missing | **никогда (P0)** |
| Зал play | Аманда, Мелисса |
| Кухня play/missing | **только Сандра** |
| Форма | u0 / u1 / u1+nop |

Старые «soft-lewd slut≥28 / hard N=3» — legacy ориентиры для миграции жестов, не отдельный roll.

---

## 8. Диспетчер / look (целевое)

| Источник | Порядок (v2) |
|----------|----------------|
| `TavernHallActivityLook` | story → **harass** (stance внутри) → kitchen noise; **не** parallel lewd-roll |
| `TavernEventDispatcher` | harass CanStart; missing **только** как исход play, не отдельный auto с look |

Legacy: rare missing/lewd в look — **убрать** при миграции.

---

## 9. Бэклог миграции

### Сделано в коде (2026-07-22, волна 1)

| | |
|--|--|
| `modules/events/hall/hall_scene_v2_core.qsps` | PlayCoached, client pick/pleasant, stance v2, missing-from-play, StartFromPlay |
| Harass SetupScene | client + stance v2 |
| T3 | mid+ FamCorrupt; sub `on_crotch` / `on_face` |
| Missing auto | `HallMissingOnlyFromPlay=1` (look/dispatcher/CanStart) |
| Lewd auto | `HallLewdAutoDisabled=1` (debug Start жив) |
| P0 | missing resolve **без** policy menu |
| GameInit | флаги v2 + PlayCoached=0 |
| Debug panel | coach links |

### Сделано (волна 2 — coach + intro play)

| | |
|--|--|
| `hall_play_coach.qsps` / `_text.qsps` | Лизетта→А, Кларисса→М, Бекки→С |
| Меню | Lizette / Clarissa / Becky + useful talk |
| Intro | `HallHarassmentIntroPlayGesture` + form tag; T3 `on_face` |
| Debug | сцены coach + флаги |

### Сделано (волна 3)

| | |
|--|--|
| Кухня normalize | нет lap→wall; drop_coin пол; **без cock** |
| Kitchen intro | corner T2; drop floor + form u1/nop |
| Knowledge | `HallPlay_*` на play resolve; `HallMissing_*` + rumor from play |
| Legacy markers | hall_lewd / kitchen_lewd headers |

### Сделано (волна 4)

| | |
|--|--|
| `hall_harass_play_text.qsps` | resolve protect/watch/ignore при **play** (клиент + тон из lewd) |
| PrintHallReaction | play → PlayResolve (зал и кухня) |
| ResultWatch | play → чаще `watch_lewd` |
| `OffenseDaysMissingAfter` | ignore / peek / interrupt → mismatch / intercept |
| Missing ApplyConsequences | зовёт OffenseDaysMissingAfter |

### Сделано (волна 5 — доделка)

| | |
|--|--|
| Клиент-лейблы | drunk=пьяный горожанин; traveler=военный/моряк |
| Intro client tag | строка типа клиента в intro |
| Thoughts | play → hall_lewd / kitchen_lewd перед меню |
| room_invite / 2nd floor | **отложено Act2+** (канон без изменений) |

### Стык со старыми системами (v2)

| Система | Как стыкуется |
|---------|----------------|
| **GirlMemoryOfStefan** | `HallChoiceConsequencesApply` на каждый выбор; play → event `hall_lewd`; ignore+play → choice `encourage` |
| **HallChoiceMemory** | тот же Apply → `$LastHallChoice*` / `$LastGirlChoice*` для family/tavern talk |
| **HallFamilyState** | через Apply |
| **SaveLastHallEvent** | `HallHarassmentRegisterLastEvent` (лог панели) |
| **HallRumorRegister** | girl, event, severity; play/watch/ignore → `hall_lewd`; missing → `hall_missing` (**порядок ARGS исправлен**) |
| **Knowledge** | `HallHarassment_*`, `HallPlay_*`, `amanda_hall_lewd_witness`, `HallMissing_*` |
| **OffenseDays** | HarassmentAfter + MissingAfter |
| **Policy after** | на виду да; missing P0 нет |
| **HallRecentTalk** | frozen (thin memory A) — как было |

Play→missing: **два** снимка памяти (выбор на виду + выбор missing).

### Система — закрыто (можно тексты)

| | |
|--|--|
| Core play/missing/P0/coach/rumor/memory | done, probe PASS |
| SaveLastHallEvent на missing resolve | done |
| room_invite / 2nd floor | Act2+ |
| git push | локально у автора |

### Тексты — прогресс

| | |
|--|--|
| Hall intro T1–T3 | клиент woven; form/nop; ClientTag **до** prose |
| Kitchen intro T1–T3 | клиент woven + drop floor |
| Missing intro/peek/ignore/interrupt | клиент + place + FromPlay lead |
| Missing reactions peek_meet / interrupt | FromPlay-ветка (зал молчал / ворвался) |
| Play-хвосты / play-resolve | done |
| USER-OWNED after (`hall_harassment_text`) | не трогать без явного OK |

---

## 10. Чеклист решений (автор) — v2

| ID | Решение | Статус |
|----|---------|--------|
| Отдельный lewd-roll | **нет** (A) | утверждено |
| Play unlock | coach-лестница, не только slut | утверждено |
| Приятный клиент | только таблица type×girl | утверждено |
| Missing | только из play, путь **α** | утверждено |
| Policy after missing | **P0 — не давать** | **утверждено** |
| Кнопки play на виду | те же 3, без второго меню | утверждено |
| До coach | play off, max endure | утверждено |
| Форма | u0 / u1 / u1+nop | утверждено |
| Coach order | Аманда → Мелисса («мелкая») → Сандра (Бекки) | утверждено |
| Зал play | Аманда, Мелисса | утверждено |
| Кухня play/missing | только Сандра | утверждено |
| Cleaning | нет | утверждено |
| 2nd floor / room_invite | пока нет | утверждено |
| drunk_guest | пьяный горожанин; **всегда −−** у всех; never play/missing | утверждено |
| rich_merchant | купец / торговец | утверждено |
| craftsman | мастеровой / горожанин | утверждено |
| traveler | **военный / моряк** | утверждено |
| Веса клиентов | разные (early drunk↑, late merchant/traveler↑) | утверждено |
| T3 | только **mid+ FamCorrupt** | утверждено |
| Under-table cock | harass flee/coin — **да** | утверждено |
| Missing % из play | protect 0; watch/ignore ~15–25% | утверждено |
| Play: щипок | улыбка, попа, ниже наклон | утверждено |
| Play: колени | сидит, юбка, рука, ноги, missing | утверждено |
| Play: drop | спина, попа; nop+анус; Мелисса отдельно **нравится** | утверждено |
| Play: wall | между ног, подмахивает, стоны; nop мокрые пальцы | утверждено |
| crotch_pull | sub **`on_crotch`** (сверху на пах) \| **`on_face`** (сверху на лицо) | утверждено |
| on_face play | поерзала, язык, мокрые лица, «вкусные девочки», веселье зала | утверждено |
| Мелисса on_face | откинулась → язык **в попу**; нравится; отдельные реплики | утверждено |
| wall + play | → **сильный** шанс missing (storage/stairs) | утверждено |
| Клиенты/жесты/поток | §0.10 | утверждено |

---

## 11. Superseded (v1 notes)

Старые формулировки «отдельный LEWD при FamCorrupt+personal», «missing rare с look», «policy после любого resolve включая missing», hard face_fall как face-to-crotch на кухне — **заменены §0**.  
Держать §3.5 legacy-файлы до миграции кода.
