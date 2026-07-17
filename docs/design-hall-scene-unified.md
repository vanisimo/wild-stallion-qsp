# Design: единый паттерн сцен зала (harassment / lewd / missing)

**Статус:** канон согласован (2026-07); кнопки/policy в коде v1; гейты lewd/missing и каталоги — **дизайн + частично код** (score/gate правки lewd; missing места/acts — довести).  
**Связь:** `docs/economy.md` §0c, `docs/design-hall-harassment.md`, `docs/state.md`

---

## 0. Лестница появления

```
до семейного ужина
  → только HARASSMENT
  → кнопки: только «Защитить»
  → policy after: только «сдержанно»

FamilyLiberationGateOpen = 1  (ужин)
  → кнопки watch/ignore + policy 2–3
  → LEWD / MISSING ещё НЕ сразу

грязный или mix путь
  + FamilyCorruptionStage ↑
  + личная (sluttiness / GirlNpcPath / agreement) ↑
  → LEWD (она играет, на виду)

ещё позже (выше stage + personal)
  → MISSING (пропала / уединение)
```

**Harass после unlock lewd не выключается** — реже + другие реакции.  
**Не:** `if lewd_unlocked: harassment = OFF`.

---

## 1. Три слоя UI (не путать)

| Слой | Что | Когда |
|------|-----|--------|
| **Сцена** | harassment / lewd / missing | осмотр зала / rare / dispatcher |
| **Кнопки сцены** | реакция Стефана | menu в событии |
| **Policy** | правило на будущее | **после** resolve |

### Кнопки (канон §0c)

| UI | Код | Тон (мысли) |
|----|-----|-------------|
| **Защитить** | `protect_hard` | harass: оборона; lewd: **запретить** шоу; missing: **вмешаться** |
| **Наблюдать** | `watch` | harass: не спускать глаз; lewd: **смотреть**; missing: **подсмотреть** |
| **Отвернуться** | `ignore` | harass: не заметил; lewd: **отвернуться**; missing: **не вмешиваться** |

- До ужина: только **Защитить**.  
- Отдельной кнопки «profit» **нет**.

Legacy aliases в коде: lewd `stop`→protect, `encourage`→ignore; missing `interrupt`→protect, `peek`→watch.

### Policy после сцены

| UI | Value |
|----|-------|
| Вести себя сдержанно | 1 |
| Решать самой | 2 |
| Вести себя расковано | 3 |

Меню: `#HallHarassmentBuildPolicyMenu` / `#HallHarassmentPolicyChoose`  
(`$HallScenePolicySource` = `lewd` \| `missing` \| harass-цикл).

До ужина policy >1 режется. OffenseDays: AfterHarassApply (policy K=3).

### Поток UI

```
intro (без полного refuse-policy текста)
  → thoughts §0c
  → Защитить / [Наблюдать / Отвернуться]
  → resolve
  → after_harass_intro + policy 1/2/3
  → реакция на правило + Вернуться
```

---

## 2. HARASSMENT (кратко; детали — design-hall-harassment.md)

| | |
|--|--|
| **Смысл** | Клиент **лезет**, она **против / терпит** (+ late: лёгкий флейвор, не «трётся») |
| **Файлы** | `hall_harassment.qsps`, `kitchen_harassment.qsps` |
| **Гейт** | рабочий зал/кухня |
| **Кто** | зал: Аманда, Мелисса; кухня harass: Сандра |

**Не в harass:** сама наклонилась «для шоу», face-play как номер, «трётся об руку», cleaning-сцены, член на виду в общем зале.

**Член:** только ветка **монета под столом** → flee \| coin; **touch** → не harass (lewd/missing high).

---

## 3. LEWD — «играет на виду»

### 3.1 Смысл

Она **ведёт** (или осознанно подыгрывает): задержалась, наклонилась дольше, села ближе.  
Не «жертва harassment»; не «исчезла» (missing).

### 3.2 Где и кто

| Место | Кто | Таблица |
|-------|-----|--------|
| **Зал** | **только Аманда, Мелисса** | hall-lewd |
| **Кухня** | **только Сандра** | kitchen-lewd (отдельные сцены) |
| **Уборка / cleaning** | **нет** | `floor` / `ladder` / `fall` **запрещены**, не использовать |

Сандра **не** в hall-lewd. Сёстры **не** в kitchen-lewd.

### 3.3 Когда открывается (числа)

**Не сразу после ужина.** Нужны dirty/mix + семейная + личная коррупция.

```
первое soft-lewd:
  FamilyLiberationGateOpen = 1
  AND Act1MoralUnlocked = 1
  AND FamilyCorruptionStage >= 3
  AND (
        sluttiness[girl] >= 28
     OR GirlNpcPath[girl] >= 22
     OR (GirlWorkPolicy[girl] = 3 AND GirlPolicyAgreement[girl] >= 2)
  )
```

**Refuse policy 3** (agreement ≤1 + low slut) → **не** кандидат lewd.

**Сандра kitchen-lewd:** те же оси, чуть жёстче (ориентир slut ≥32 или pol3+agr≥2) + только кухня.

### 3.4 Soft vs hard

| | Soft | Hard |
|--|------|------|
| Тон | ещё почти «на грани», но **она** уже не чистая жертва | явно играет |
| Картинки | **те же** позы | те же |
| Текст | soft-roll | hard-roll |

**Hard** (lap, face_fall): только после **N = 3** soft-lewd **или** `HallLewdStage >= 3` (что раньше).  
Счётчик: `GirlHallLewdSoftCount[girl]` или прогресс stage от soft-событий.

### 3.5 Каталог сцен (зал, Аманда/Мелисса)

| id | Сцена | Unlock |
|----|--------|--------|
| `bend` | дольше наклоняется | soft |
| `waist` | рука на бедре, не сразу убирает | soft |
| `sit_near` | край лавки | soft |
| `lap` | на коленях | hard (B2) |
| `face_fall` | **падение на лицо** | hard (B2) |

**Убрано:** `kiss` + шнуровка лифа.  
**Убрано:** cleaning floor/ladder/fall.

Кухня-Сандра: отдельные id (не копировать hall 1:1); без cleaning-позы.

### 3.6 Кнопки (тон)

| UI | Смысл |
|----|--------|
| Защитить | **запретить** (оборвать шоу) |
| Наблюдать | **смотреть** |
| Отвернуться | **отвернуться** (не мешаю → чаевые/scandal) |

### 3.7 Файлы

- `modules/events/hall/hall_lewd_behavior.qsps`  
- `modules/events/hall/hall_lewd_behavior_text.qsps`  
- (future) kitchen-lewd table for Sandra  

---

## 4. MISSING — исчезновение

### 4.1 Смысл

Её **нет** на обычном месте. Уединение / «дело», не витрина lewd в центре зала.

### 4.2 Где и кто

| place | Кто |
|-------|-----|
| `under_table` | Аманда, Мелисса (**A1:** также harass coin/cock) |
| `storage` | Аманда, Мелисса |
| `stairs` | Аманда, Мелисса |
| `kitchen` | **только Сандра** (сёстры **нет**) |
| `second_floor` | **пока нет** |
| `room_invite` | **пока нет** |

### 4.3 Когда открывается (числа)

```
первое missing:
  FamilyLiberationGateOpen = 1
  AND Act1MoralUnlocked = 1
  AND FamilyCorruptionStage >= 3
  AND HallMissingStage >= 3   (или общий lewd-progress ≥3)
  AND sluttiness[girl] >= 35  (сёстры)

Сандра kitchen missing:
  те же семейные гейты
  AND (sluttiness >= 38 OR (policy=3 AND agreement >= 2))
  AND place = kitchen only
```

**Late acts:** stage ≥4 + выше personal / fam corruption.

### 4.4 Лестница private acts (peek)

Одинаковая логика для сестёр и Сандры; у Сандры в **mid** + сиськи.

| Этап | Содержание |
|------|------------|
| **Early** | петтинг; оголила сиськи → дала полизать; показала киску → дала потрогать; **потрогала член** |
| **Mid** | **дрочка** ему и ей; затем **минет** и **куни** |
| **Mid + Сандра** | + **работа сиськами** |
| **Late** | минет → **яйца, глубокий заглот**; куни → **анилингус** (задрал юбку, лижет попу) |

### 4.5 Кнопки (тон)

| UI | Смысл |
|----|--------|
| Защитить | **вмешаться** (ворваться) |
| Наблюдать | **подсмотреть** |
| Отвернуться | **не вмешиваться** |

### 4.6 Файлы

- `modules/events/hall/hall_missing_girl.qsps`  
- `modules/events/hall/hall_missing_girl_text.qsps`  

---

## 5. Веса осмотра зала (после ужина, ориентир)

| Состояние | Harass | Lewd | Missing |
|-----------|--------|------|---------|
| только liberation, FamCorrupt &lt; 3 | ~100% | 0 | 0 |
| FamCorrupt ≥3, personal mid | высокий | появляется | 0 / редко |
| personal high + agreement | ниже | высокий | mid |
| stage missing/lewd high + scandal | ниже | mid | выше |

---

## 6. Стык harass ↔ lewd ↔ missing

| Ситуация | Система |
|----------|---------|
| Клиент лезет, она против/терпит | **harass** |
| Лёгкий late-флейвор (не отдёрнула сразу) | **harass** reaction |
| **Трётся** / сама ведёт | **lewd** |
| Монета + член под столом: flee/coin | **harass** |
| Под столом: touch / hold | **lewd** или **missing** high |
| Ушла из зала / кухня Сандры с клиентом | **missing** |

---

## 7. Пороги — сводная таблица (канон чисел)

| Гейт | Значение |
|------|----------|
| Первое **soft-lewd** | FamCorrupt **≥3** + liberation + (slut≥**28** ∨ path≥**22** ∨ pol3+agr≥**2**) |
| **Hard-lewd** (lap, face_fall) | **N=3** soft **или** HallLewdStage≥**3** |
| Первое **missing** | FamCorrupt **≥3** + liberation + stage≥**3** + slut≥**35** (сёстры) |
| **Late** missing acts | stage≥**4** + выше personal |
| Сандра lewd/missing | **только кухня**; slut≥**32/38** или agr≥2; без зала / 2nd floor |

---

## 8. Диспетчер / look

| Источник | Порядок |
|----------|---------|
| `TavernHallActivityLook` | story → harassment → rare (missing/lewd) → kitchen noise |
| `TavernEventDispatcher` | missing / lewd **только через CanStart** |

---

## 9. Что ещё (бэклог)

1. Общий `#HallSceneBuildChoiceMenu` / after-policy helper.  
2. Довести CanStart/score missing+lewd **точно** к таблице §7.  
3. Убрать cleaning-сцены из lewd-пулов в коде/текстах.  
4. Kitchen-lewd table для Сандры.  
5. OffenseDays на lewd/missing choices.  
6. USER-OWNED prose pass.  
7. room_invite / 2nd floor — Act2+ (D2).

---

## 10. Чеклист решений (автор)

| ID | Решение |
|----|---------|
| Lewd не сразу после ужина | dirty/mix + FamCorrupt + personal |
| Зал lewd | только Аманда, Мелисса |
| Кухня lewd/missing | только Сандра |
| Cleaning | нет |
| kiss+шнуровка | нет; hard = lap + face_fall |
| Soft/hard | одни картинки, разный текст |
| Hard unlock | N=3 soft или stage≥3 |
| Under_table | A1 harass + missing |
| Missing acts | early→mid→late как §4.4; Сандра + сиськи в mid |
| 2nd floor / room_invite | пока нет |
| Harass + lewd | оба живы; подыгрыш-флейвор в harass, «трётся» в lewd |
