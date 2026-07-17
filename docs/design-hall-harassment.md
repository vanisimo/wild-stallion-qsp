# Design: Hall / Kitchen Harassment (v1)

**Статус:** логика tier/stance/E2 — в коде; intro пока служебный + stub; каталог T3-4/5 — дизайн.  
**Код:** `modules/events/hall/hall_harassment.qsps`, `modules/events/kitchen/kitchen_harassment.qsps`  
**Тексты:** `hall_harassment_text.qsps`, kitchen text  
**Связано:** `docs/design-hall-scene-unified.md` (lewd/missing + пороги), `docs/economy.md` §0c, offense days, state.md  

Единые кнопки/policy/лестница зала — в **design-hall-scene-unified.md**.

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
| 3 | **сейчас** `RAND(1, 3)`; **позже** + type 4–5 (drop/стена); under-table cock — subroll type 5 coin |

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
| 1 | Задирает юбку | да | да |
| 2 | Сажает на колени жёстко | да | да |
| 3 | Тянет → падает к нему **на пах** (не на лицо) | да | да |
| 4 | **Прижал к стойке/стене**, рука под юбкой | план | да |
| 5 | **Drop** (subroll) | план | да |

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

Гейты under-table cock (черновик): liberation + FamCorrupt ≥2–3 + не первый harass; low slut+refuse → только лапанье **без** члена.

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
