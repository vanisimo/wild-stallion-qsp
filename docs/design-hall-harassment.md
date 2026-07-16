# Design: Hall / Kitchen Harassment (v1)

**Статус:** логика выбора сцены — в коде; художественные intro — **ещё нет** (служебный текст + stub-картинка).  
**Код:** `modules/events/hall/hall_harassment.qsps`, `modules/events/kitchen/kitchen_harassment.qsps`  
**Тексты (legacy aftermath / policy hooks):** `hall_harassment_text.qsps`, kitchen text  
**Связано:** `docs/policy-flow.md`, `docs/design-interaction-schemes.md` §4, `docs/state.md` (family/uniform), offense days  

Коммит опорной логики: `feat(harass): tier/stance gates, service intro stub…` (ветка `main`).

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

### 4.3 `#HallHarassmentPickType` (A2)

| HarassTier | Пул type |
|------------|----------|
| 1, 2 | `RAND(1, 4)` |
| 3 | `RAND(1, 3)` — types **4–5 позже** |

---

## 5. Каталог типов (дизайн сцен)

Одна **картинка-поза** на type; **text_roll 1–3** на позу (дешевле, чем 3 арта).  
Girl flavor в **художественном** intro (I1 — только intro, не after-меню).

### Tier 1 — намёки, лёгкие касания, игривость

| Type | Жест | Картинка (идея) |
|------|------|-----------------|
| 1 | Хватает за руку | клиент держит за руку/запястье |
| 2 | Прихватил за талию | рука на талии, рядом у стола |
| 3 | Взгляд / «оценка» | **Аманда** — попа; **Мелисса** — декольте; **Сандра** — и то и то (roll) |
| 4 | Щипок за бок | рука у бока |

### Tier 2 — нарушение границ

| Type | Жест | Картинка (идея) |
|------|------|-----------------|
| 1 | Рука на попе | ладонь на юбке сзади |
| 2 | Сажает на колени | на/полуна коленях у клиента |
| 3 | Лицом в декольте | обхват к груди |
| 4 | Сзади + трётся пахом | обхват сзади |

### Tier 3 — агрессия / почти публичный секс-жест

**Только при u1** (E2). Ветки **panties / nop** где видна юбка/пах.

| Type | Жест | MVP | Panty branch |
|------|------|-----|--------------|
| 1 | Задирает юбку | **да** | да |
| 2 | Сажает на колени (жёстче T2) | **да** | да |
| 3 | Тянет за руку → падает сверху на пах | **да** | да |
| 4 | Наклон «показ» (случайно / mixed / сама дразнит) | **позже** (C1) | да |
| 5 | Наклон за предметом → падение лицом | **позже**, rare | да |

Type 4 stance-ветки (когда контент):

| Код | Смысл |
|-----|--------|
| 4r resist | наклонилась по работе, клиент пользуется |
| 4m mixed | чуть дольше, чем нужно |
| 4p provoke | специально для «своего» / денежного |

---

## 6. Stance девушки (`$HarassGirlStance`)

**Не открывает tier.** Меняет тон текста intro (и позже — провокационные жесты).

| Stance | Условие (F1 large bands) | Смысл |
|--------|--------------------------|--------|
| `resist` | default | не хочет, границы, злость/страх |
| `mixed` | `sluttiness >= 35` **и** `stage >= 2` | стыдно + терпит / неоднозначно |
| `provoke` | `sluttiness >= 50` **и** `stage >= 3` | улыбка, наклон «для своих», намёки «готов на большее» |

На высоких band’ах девушки **не всегда жертвы**: могут провоцировать, тереть рукой, дразнить понравившихся/денежных клиентов — **в тексте**, без отдельного AllowedTier.

### Girl flavor (I1 — художественный intro)

| Девушка | Окраска |
|---------|---------|
| **Аманда** | краснеет, взвизгивает, вскрикивает |
| **Мелисса** | отстранённо, шлёпает по рукам, смотрит зло |
| **Сандра** | отталкивает, зло говорит, отмахивается полотенцем |

При high stance flavor **сдвигается** (игровее / контроль / прагматика), но персона сохраняется.

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

`OffenseDaysHarassmentAfter` (amanda/melissa):

| Условие | Reason |
|---------|--------|
| band low + ignore / watch_bad / watch_lewd | `no_protect_low` (накопление K) |
| band high + protect_hard + protect_dislike | `protect_high` |
| protect_success | intercept count → `intercept` |
| + Сандра узнала про дочерей | `daughter_no_protect` |

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
| **Сейчас** | `#HallHarassmentPrintServiceIntro` — кто, tier, type, stance, uniform, panty, stage, slut; пути только при `debug = 1` |
| **Потом (G3)** | длинные художественные intro: type × girl × stance × text_roll; panty-ветки на T3 |

Предлагаемые id (когда писать):

```
waitress_intro_t{tier}_type{n}
waitress_intro_t{tier}_type{n}_{resist|mixed|provoke}
waitress_intro_t{tier}_type{n}_nop
kitchen_intro_…  (зеркало)
```

Старые ключи `waitress_intro_1..4` без tier — legacy; не опираться для новых сцен.

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
| `$HarassGirlStance` | resist / mixed / provoke |
| `$HallHarassUniformKey` | u0 / u1 |
| `$HallHarassPantyKey` | panties / nop |
| `$HallHarassReaction` | protect_hard / watch / ignore |
| `$HallHarassTalkReaction` | подтип aftermath |
| `HallHarassmentResolved` | 0 intro / 1 after |
| `HallHarassPolicyChosen` / `HallHarassPolicyValue` | after policy |

---

## 11. MVP контента (когда выйдем из заглушек)

1. T1 types 1–4 — тексты + oneshot (хотя бы u0)  
2. T2 types 1–4 — u0 + u1  
3. T3 types 1–3 — u1 + panty/nop + stance  
4. T3 type 4 (C1) и type 5 rare — phase 2  
5. Girl flavor I1 в intro; after — отдельно  

Порядок утверждён: **сначала логика/служебка (готово) → художество и арт по слоям.**

---

## 12. Файлы

| Роль | Путь |
|------|------|
| Логика зал | `modules/events/hall/hall_harassment.qsps` |
| Логика кухня | `modules/events/kitchen/kitchen_harassment.qsps` |
| Тексты зал | `modules/events/hall/hall_harassment_text.qsps` |
| Policy after | `modules/actions/tavern/girl_work_policy_*.qsps` |
| Offense after | `modules/core/family/offense_days.qsps` |
| Stub image | `images/common/hall_harass_stub.png` |
| Униформа | `girl_uniform_talk*`, `girl_no_panties_work*`, `irma_uniform_*` |

---

## 13. Чеклист решений (зафиксировано с автором)

| ID | Решение |
|----|---------|
| A2 | T3 types 1–3 now; 4–5 later |
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
