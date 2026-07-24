# Design: Hall / Kitchen Harassment (v1)

**Статус:** логика T1–T3 (types 1–5 + wall/drop/cock) + художественные intro G3 v1 — в коде.  
**Код:** `modules/events/hall/hall_harassment.qsps`, `modules/events/kitchen/kitchen_harassment.qsps`  
**Тексты:** `hall_harassment_intro_text.qsps` (intro), `hall_harassment_text.qsps` (after/policy), kitchen text  
**Связано:** `docs/design-hall-scene-unified.md` (lewd/missing + пороги), `docs/economy.md` §0c, offense days, state.md  

Единые кнопки/policy/лестница зала — в **design-hall-scene-unified.md**.

**Канон v2 (2026-07-22, утверждено):** сквозное приставание; play = stance (не отдельный lewd-roll); missing только из play (α); **policy после missing не показывать (P0)**. Подробности — `docs/design-hall-scene-unified.md` §0.

---

## 1. Поток сцены (игрок)

```
Осмотр зала / spark queue
  → #HallHarassment (или #KitchenHarassment для Сандры)
  → HallHarassmentSetupScene
  → stub image (small) + служебный intro
  → dropdown «мне»: Защитить / [Наблюдать / Отвернуться]
  → HallHarassmentApplyChoice → resolved
  → экран «в стороне»: итог + меню policy (сдержанно / сама / расковано)
```

| Шаг | Что видит игрок |
|-----|-----------------|
| Intro | oneshot-картинка (сейчас одна заглушка) + текст сцены |
| Выбор | **Защитить** всегда; **Наблюдать** / **Отвернуться** только если `FamilyLiberationGateOpen = 1` |
| After | реакция зала + разговор о правилах работы (policy) |

**Не в hall harass** (отдельные события): подворотня, missing girl, group, стрип-шоу, glory — не раздувать типы приставания.

---

## 2. Кто и где

| Зона | Девушки | Job key | Entry |
|------|---------|---------|--------|
| Зал | Аманда, Мелисса (waitress на смене в `TavernMain`) | `waitress` | `HallHarassmentTry`, spark hall |
| Кухня / шум | Сандра | `kitchen` | `KitchenHarassmentTry` ~22%, `TryFromHall` ~14% |

Общие переменные сцены: `$HallHarass*`, `HallHarassType`, `HarassTier`, `$HarassGirlStance`, …

Кухня после setup вызывает тот же `HallHarassmentSetupScene`.

---

## 3. Оси мира (не смешивать)

| Ось | Переменная | Смысл |
|-----|------------|--------|
| Семейный уклад | `FamilyCorruptionStage` 0…5 | «насколько зал/дом уже разъехался» |
| Личная распущенность | `sluttiness[girl]` 0…100 | готова ли **эта** девушка |
| Форма | `GirlUniformLevel` 0/1 | u0 обычная / u1 откровенная |
| Без трусиков | `GirlNoPantiesWork[girl]` | отдельный флаг (гейты offer: stage≥3 + slut + u1) |
| Policy | `GirlWorkPolicy` 1…3 | **не** открывает tier; влияет на after / тон позже |

**Прямой формулы stage ↔ sluttiness нет.** В harass они встречаются только в **AND-гейтах** (AllowedTier, stance).

Форма:

- **u0** — льняное платье до середины бедра, шнуровка, рукава по локоть  
- **u1** — более лёгкая ткань, короче подол, короткие рукава  
- **no panties** — поверх u1, отдельный offer  

Путь смены: Irma offer/orders → `uniform_purchased` → `GirlUniformTalk` → optional no-panties talk.

---

## 4. AllowedTier / HarassTier / Type

### 4.1 `#HallHarassmentCalculateAllowedTier`

| AllowedTier | Условие |
|-------------|---------|
| **1** | всегда (база) |
| **2** | `FamilyCorruptionStage >= 2` **и** `sluttiness >= 20` |
| **3** | `stage >= 3` **и** `sluttiness >= 40` **и** `GirlUniformLevel = 1` (**E2**) |

Дополнительно:

- если `GirlNoPantiesWork = 1` и AllowedTier &lt; 3 → `AllowedTier += 1`
- **clamp E2:** если `GirlUniformLevel <> 1` → AllowedTier **не выше 2** (Tier 3 без u1 невозможен)

**Policy на AllowedTier не влияет** (осознанное решение).

### 4.2 `#HallHarassmentPickTier` (D1)

```
HarassTier = RAND(1, HallHarassAllowedTier)   // равный шанс
```

### 4.3 `#HallHarassmentPickType` (A2 + план)

| HarassTier | Пул type |
|------------|----------|
| 1, 2 | `RAND(1, 4)` |
| 3 | weighted 1–5: ~22% each types 1–3, ~19% type 4 wall, ~15% type 5 drop; type 5 → `drop_cutlery` \| `drop_coin`; cock только `drop_coin` + гейты |

---

## 5. Каталог типов (дизайн сцен)

Одна **картинка-поза** на type; **text_roll 1–3** на позу.  
**Только клиент-driven.**  
**Не в harass:** сама наклонилась «для шоу», face-sit как номер, «трётся об руку», cleaning, член на виду в общем зале.

Полная карта слоёв: `docs/design-hall-scene-unified.md`.

### Tier 1 — намёки, лёгкие касания

| Type | Жест | Картинка (идея) |
|------|------|-----------------|
| 1 | Хватает за руку | клиент держит запястье |
| 2 | Прихватил за талию | рука на талии |
| 3 | Взгляд / «оценка» | Аманда — попа; Мелисса — декольте; кухня Сандра — roll |
| 4 | Щипок за бок | рука у бока |

### Tier 2 — нарушение границ

| Type | Жест | Картинка (идея) |
|------|------|-----------------|
| 1 | Рука на попе | ладонь на юбке сзади |
| 2 | Тянет / сажает на колени | на коленях |
| 3 | Лицом в декольте (**он** прижал) | обхват к груди |
| 4 | Сзади + трётся пахом | обхват сзади |

### Tier 3 — жёстко (клиент)

**T3 только при u1** (E2), кроме там где u0 ещё читается (длинный подол).  
Panty / nop — где видна юбка/пах.

| Type | Жест | MVP | Panty |
|------|------|-----|-------|
| 1 | Задирает юбку | да (stub) | да |
| 2 | Сажает на колени жёстко | да (stub) | да |
| 3 | Тянет → падает к нему **на пах** (не на лицо) | да (stub) | да |
| 4 | **Прижал к стойке/стене**, рука под юбкой | **да** (`$HallHarassSubScene=wall`) | да |
| 5 | **Drop** (subroll) | **да** | да |

#### Type 5 subroll (вместо «сама / face»)

| Sub | Сцена |
|-----|--------|
| `drop_cutlery` | клиент роняет вилку/ложку → она поднимает → рука под юбку |
| `drop_coin` | роняет монету под стол → она лезет → лапает / попа |

**Член только здесь, только под столом** (`drop_coin` + гейты):

```
она уже под столом за монетой
  → он достаёт член (не на виду зала)
  → реакция harassment only:
       flee  — вылетела
       coin  — спокойно забрала монету, ушла
  → touch / hold — НЕ harass → lewd или missing high
```

Гейты under-table cock (**в коде** `#HallHarassmentPickUnderTableCock`):

- `$HallHarassSubScene = drop_coin`
- `FamilyLiberationGateOpen = 1`
- `FamilyCorruptionStage >= 3`
- `HallHarassEverOccurred = 1` (не на самом первом harass кампании; флаг ставится в ApplyChoice)
- **не** (slut &lt; 35 **и** policy = 1) → иначе только `groping` без члена

Реакция при cock: `provoke`/slut≥50 → `coin`; `resist`/slut&lt;40 → `flee`; mixed → 50/50.

**Не возвращаем в harass:** «сама показала», падение **на лицо** (face → **lewd** `face_fall`), cleaning.

---

## 6. Stance (`$HarassGirlStance`)

**Не открывает tier.** Тон intro/реакций.

| Stance | Условие (F1) | Смысл в **harass** |
|--------|--------------|---------------------|
| `resist` | default | злость, страх, отшат |
| `mixed` | slut≥35 **и** FamCorrupt≥2 | стыд + терпит; не сразу отдёрнула |
| `provoke` | slut≥50 **и** FamCorrupt≥3 | **лёгкий** флейвор: взгляд, пауза — **не** «трётся / ведёт» |

**После слома (liberation + late):**  
- в harass — **A**: другие реакции (терпит иначе, пауза, coin под столом);  
- **B** «трётся об руку / сама играет» — только **lewd**.

### Girl flavor (I1 — intro)

| Девушка | Окраска |
|---------|---------|
| **Аманда** | краснеет, взвизгивает, вскрикивает |
| **Мелисса** | отстранённо, шлёпает по рукам, смотрит зло |
| **Сандра** | отталкивает, зло говорит, полотенцем (кухня) |

Late stance сдвигает тон, персона сохраняется.

---

## 7. Реакции **игрока** (dropdown)

| Ключ | UI | Когда доступен |
|------|-----|----------------|
| `protect_hard` | Защитить | всегда |
| `watch` | Наблюдать | `FamilyLiberationGateOpen = 1` |
| `ignore` | Отвернуться | `FamilyLiberationGateOpen = 1` |

Обработка: `#HallHarassmentApplyChoice` → ResultProtectHard / Watch / Ignore → consequences + extra systems.

### Подрезультаты (`$HallHarassTalkReaction`) — тон aftermath

| Реакция игрока | Возможные talk-метки | Aftermath / hall reaction (ключи текста) |
|----------------|----------------------|------------------------------------------|
| protect_hard | `protect_success`, `protect_dislike`, `protect_fail` | thanks / annoyed / fail |
| watch | `watch_ok`, `watch_bad`, `watch_lewd` | ok / angry / lewd hall |
| ignore | — (cold vs ok по friends/fear) | ignore_cold / ignore_ok |

### Связь с offense days

`OffenseDaysHarassmentAfter` (amanda/melissa) **v2.1**:

| Условие | Reason |
|---------|--------|
| liberation=0 (early Act1) | no_protect **off** |
| play / provoke | no_protect **off** |
| band **0** mid | no_protect **off** |
| band **1** + ignore | `no_protect_low` K=3 |
| band **1** + watch_bad | `no_protect_low` K=3 |
| band **1** + watch_lewd | **нет** |
| band 2 + protect_dislike | `protect_high` |
| protect_success | intercept → `intercept` |

Сандра `daughter_no_protect` **v2.1**: learn **15–40%**; cooldown **3 дня**; **K=3** (не сразу days); не play; не watch_lewd; дочь band 1 only.

См. `modules/core/family/offense_days.qsps`.

### После сцены: policy

Меню (если gate): сдержанно (1) / сама (2) / расковано (3) → `GirlWorkPolicyTalkAfterHarassApply`.  
До liberation gate policy &gt; 1 блокируется.

---

## 8. Картинки

### Сейчас (заглушка)

| | |
|--|--|
| Файл | `images/common/hall_harass_stub.png` (маленький, 160×90) |
| Вызов | `ShowImage`, type `common`, action `hall_harass_stub`, size **small** |
| Intro и reaction | обе на stub, чтобы не листать large |

### План oneshot (когда появятся ассеты)

```
images/events/{girl}/hall_harass/t{tier}_type{n}_{u0|u1}[_nop].webp
```

Примеры:

- `…/t1_type1_u0.webp`
- `…/t3_type1_u1_nop.webp`

Правила:

- **u1-поза** только если `GirlUniformLevel = 1`; иначе всегда **u0** в ключе  
- `_nop` только если `GirlNoPantiesWork = 1`  
- T3 без u1 **не** генерируется (AllowedTier)  
- reaction later: `hall_harass/reaction_{protect_hard|watch|ignore}` (сейчас stub)

Переменные путей после setup:

- `$HallHarassStubImagePath`
- `$HallHarassFutureImagePath` (план, для debug)

---

## 9. Тексты

| Фаза | Что |
|------|-----|
| **Сейчас (G3 v1)** | `#HallHarassmentPrintArtisticIntro` → hall/kitchen × T1–T3 × type; stance-хвост; T3 wall/drop/cock; service-блок только при `debug=1` |
| **Потом** | text_roll 2–3 варианта; panty-ветки; полировка USER tone |

Локации intro: `hall_harassment_intro_text.qsps`  
Debug: `gt 'HallHarassmentDebugMenu'` / `HallHarassmentDebugStart` (girl, tier, type [, sub, cock, react])  

Старые ключи `waitress_intro_1..4` — legacy.

---

## 10. Переменные (снимок сцены)

| Переменная | Смысл |
|------------|--------|
| `$HallHarassGirl` | ключ девушки |
| `$HallHarassJob` | waitress / kitchen |
| `$HallHarassConsequenceArea` | hall / kitchen |
| `HallHarassAllowedTier` | потолок 1…3 |
| `HarassTier` | выпавший 1…3 |
| `HallHarassType` | type в тире |
| `$HallHarassSubScene` | `wall` / `drop_cutlery` / `drop_coin` / '' |
| `HallHarassUnderTableCock` | 0/1 — член под столом |
| `$HallHarassUnderReact` | `groping` / `flee` / `coin` |
| `HallHarassEverOccurred` | 1 после первого resolve (гейт cock) |
| `$HarassGirlStance` | resist / mixed / provoke |
| `$HallHarassUniformKey` | u0 / u1 |
| `$HallHarassPantyKey` | panties / nop |
| `$HallHarassReaction` | protect_hard / watch / ignore |
| `$HallHarassTalkReaction` | подтип aftermath |
| `HallHarassmentResolved` | 0 intro / 1 after |
| `HallHarassPolicyChosen` / `HallHarassPolicyValue` | after policy |

---

## 11. MVP контента (когда выйдем из заглушек)

1. T1–T3 intro тексты — **G3 v1 готово** (hall + kitchen)  
2. Oneshot-арт по ключам path  
3. text_roll / panty-ветки / after-flavor по type  
4. After/policy тексты — отдельно (уже есть generic)  

Порядок: **логика ✓ → intro prose v1 ✓ → арт / polish.**

---

## 12. Файлы

| Роль | Путь |
|------|------|
| Логика зал | `modules/events/hall/hall_harassment.qsps` |
| Логика кухня | `modules/events/kitchen/kitchen_harassment.qsps` |
| Intro | `modules/events/hall/hall_harassment_intro_text.qsps` |
| After/прочее | `modules/events/hall/hall_harassment_text.qsps` |
| Policy after | `modules/actions/tavern/girl_work_policy_*.qsps` |
| Offense after | `modules/core/family/offense_days.qsps` |
| Stub image | `images/common/hall_harass_stub.png` |
| Униформа | `girl_uniform_talk*`, `girl_no_panties_work*`, `irma_uniform_*` |

---

## 13. Чеклист решений (зафиксировано с автором)

| ID | Решение |
|----|---------|
| A2 | T3 types 1–5 + drop/wall/cock subrolls **done** (stub intro) |
| B1 | stance resist / mixed / provoke |
| C1 | type4: accidental / mixed / provoke (later) |
| D1 | equal RAND tier |
| E2 | Tier 3 only with u1 |
| F1 | large slut/stage bands only |
| G3 | long artistic texts when written |
| H | no full content yet; one stub image |
| I1 | girl flavor only in intro |
| — | text_roll 1–3 per pose |
| — | policy does not raise AllowedTier |
| — | service text now; paths in debug |
