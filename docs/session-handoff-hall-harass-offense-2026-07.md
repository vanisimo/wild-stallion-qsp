# Handoff: Hall Harassment + Memory A + OffenseDays (2026-07)

**Ветка:** `main`  
**Проект:** Wild Stallion QSP / «Дикий Жеребец»  
**Для:** продолжение с другой машины после `git pull`  
**Связанные доки:**  
`docs/design-hall-harassment.md`,  
`docs/design-hall-memory-thin.md`,  
`docs/design-hall-scene-unified.md`,  
`modules/core/family/offense_days.qsps`

---

## 0. Что сделать сразу на новой машине

```powershell
cd E:\traktir   # или свой путь
git pull origin main
```

Пересобрать `game.qsp` (QSP 5.90 / `qsp-build-and-run`).  
Файл debug: `modules/debug/debug_hall_harassment.qsps` должен попасть в сборку (папка `modules/debug` подключена).

Вход в тест:

```
gt 'HallHarassmentGateDebugMenu'
```

или предмет **Дебаг** → «Harassment: после ужина + гейты T1–T3».

---

## 1. О чём договорились (канон сессии)

### 1.1 Harassment — каталог и логика

| Решение | Суть |
|---------|------|
| Tier 1–2 | types 1–4 |
| Tier 3 | types 1–5; **4 = wall**, **5 = drop** |
| Type 5 sub | `drop_cutlery` \| `drop_coin` |
| Член | **только** under-table: `drop_coin` + гейты (не в общем зале) |
| Реакция cock | harass only: `flee` \| `coin` (touch/hold → lewd/missing, не harass) |
| Гейты cock | liberation + stage≥3 + `HallHarassEverOccurred` + не (slut&lt;35 **и** policy1) |
| T3 pool | weighted: ~22%×3 types1–3, ~19% wall, ~15% drop |
| Intro | художественный G3 v1: `hall_harassment_intro_text.qsps` |
| Service intro | только при `debug=1` |
| Kitchen | тот же setup; intro flavor кухни для Сандры |
| Картинки | пока stub `hall_harass_stub.png` |

**Не в harass:** сама наклонилась для шоу, face-sit, cleaning-шоу, член на виду.

### 1.2 Thin memory (вариант A)

| Ось | Owner | Зачем |
|-----|--------|--------|
| Долгий стиль хозяина | `GirlMemoryOfStefan` → `GirlRemembers*` | DailyAftermath, italic |
| Snapshot выбора | `HallChoiceMemory` → `$LastHallChoice*` | family/tavern talk hooks |
| Лог сцены | `SaveLastHallEvent` | панель, «что случилось» legacy |

| Frozen | Как |
|--------|-----|
| `HallRecentMemorySave` | no-op |
| `HallRecentTalk` | CanShow=0, меню убрано |
| «Что случилось в зале» | убрано из личного (дубль after+policy) |
| «Моё решение в зале» | убрано из меню (код/тексты живы) |

**Не удалять** frozen-файлы — старые `gs` не должны падать.

### 1.3 Личный разговор

| Проблема | Решение |
|----------|---------|
| Пустой серый экран | `Menu.Show` **после** intro-текста |
| «Запретить парней» с Act1 | гейт: unlock `amanda_boys` **или** запрет уже включён |
| Дубли зала | hall_event / hall_choice не в личном меню |
| Policy | **только** сразу после harass на after-screen |

### 1.4 OffenseDays (обида)

| Правило | Суть |
|---------|------|
| Накопление | **K=3** mismatch → `GirlOffenseDays=4` |
| no_protect | ignore **или** watch_bad/watch_lewd при **band ≠ 2** |
| protect_high | band=2 + protect_dislike |
| Soft 1/3–2/3 | короткая строка на after-screen |
| Полная обида | реплика «обиделась / не подходи» + (если был секс) отказ от близости |

**Sex-строки (только если был интим):**

- **Аманда:** «На потрахушки можешь не рассчитывать…»
- **Мелисса:** «…к моей пещерке… отлучён от сладкого, нерыцарь»
- **Сандра:** «Ночью ко мне не приходи»

Гейт интима: `*HomeSex` **или** `IntimStage≥3` **или** `sexacts>0`.

### 1.5 Критические баги, которые уже чинили

1. **`killvar '$OffenseGirl'`** в хелперах → счётчик писал в ключ `''` → `protectK` всегда 0.  
   Фикс: отдельные имена (`$OffenseRegGirl`, `$OffenseHarassGirl`, …).

2. **`$GirlOffenseReason[girl]`** (строковый массив QSP).  
   Без `$` → error 12 «Несоответствие типов» на `OffenseDaysStart`.  
   Все reason — только `$GirlOffenseReason[...]`.

---

## 2. Ключевые файлы

| Роль | Путь |
|------|------|
| Логика harass | `modules/events/hall/hall_harassment.qsps` |
| Intro prose | `modules/events/hall/hall_harassment_intro_text.qsps` |
| After/policy texts | `modules/events/hall/hall_harassment_text.qsps` |
| Кухня harass | `modules/events/kitchen/kitchen_harassment.qsps` |
| Offense engine | `modules/core/family/offense_days.qsps` |
| Offense texts + scene reaction | `modules/core/family/offense_days_text.qsps` |
| Debug гейты | `modules/debug/debug_hall_harassment.qsps` |
| Thin memory doc | `docs/design-hall-memory-thin.md` |
| Harassment design | `docs/design-hall-harassment.md` |
| Personal talk | `modules/actions/dialogs/girl_talk_personal.qsps` |
| Girl talk menu order | `modules/actions/dialogs/girl_talk.qsps` |

---

## 3. Debug-пресеты (шпаргалка)

`gt 'HallHarassmentGateDebugMenu'`

| Пресет | Ожидание |
|--------|----------|
| **ДО ужина** | только «Защитить», policy только 1 |
| **ПОСЛЕ ужина** | watch/ignore + policy 2–3 |
| **После + T2** | stage2 slut25 |
| **После + T3** | stage3 slut45 u1 ever=1 |
| **Cock-ready** | under-table cock возможен |
| **offense_low** | band low, ignore копит K |
| Force wall / drop / cock | type без rand |
| Natural | tier/type по реальным гейтам |
| protectK +1 / ×3 | быстрый тест обиды |

---

## 4. Этапы тестирования (приоритет)

Делать **по порядку**. Не переходить к следующему этапу, пока текущий красный.

### P0 — Сборка и debug (блокеры)

| # | Шаг | OK |
|---|-----|----|
| P0.1 | `git pull`, build без ошибок локаций | ☐ |
| P0.2 | `gt 'HallHarassmentGateDebugMenu'` открывается, статус сверху читается | ☐ |
| P0.3 | Force Аманда T1 type1 — intro + меню, **нет error 12** | ☐ |

### P1 — OffenseDays (сейчас самый важный)

| # | Шаг | Ожидание | OK |
|---|-----|----------|----|
| P1.1 | Пресет **offense_low** → Force T1 → **Отвернуться** | soft «(1/3)», debug `protectK=1 react=ignore` | ☐ |
| P1.2 | Сброс слота, ещё 2× ignore | (2/3) затем (3/3) | ☐ |
| P1.3 | На 3-м after-screen | «обиделась / не подходи» + days=4 | ☐ |
| P1.4 | Разговор с Амандой | экран **ОБИДА**, intro + menu | ☐ |
| P1.5 | (опц.) `AmandaHomeSex=1` + ×3 ignore | + строка про потрахушки | ☐ |
| P1.6 | Debug: protectK ×3 без сцены | days=4 без error | ☐ |

**Красный если:** `protectK=0` после ignore, error 12, нет soft-строки.

### P2 — Гейты кнопок и policy after

| # | Шаг | Ожидание | OK |
|---|-----|----------|----|
| P2.1 | **ДО ужина** + harass | только Защитить | ☐ |
| P2.2 | **ПОСЛЕ ужина** | Защитить / Наблюдать / Отвернуться | ☐ |
| P2.3 | After-screen policy | 1 всегда; 2–3 только liberation | ☐ |
| P2.4 | Policy apply | реакция на правило, без crash | ☐ |

### P3 — Catalog T1–T3 intro

| # | Шаг | Ожидание | OK |
|---|-----|----------|----|
| P3.1 | T1 types 1–4 (force) | разные stub-жесты + girl flavor | ☐ |
| P3.2 | T2 types 1–4 | жёстче, intro wall of text OK | ☐ |
| P3.3 | T3 type1–3 | юбка / колени / пах (не face) | ☐ |
| P3.4 | T3 wall | wall press | ☐ |
| P3.5 | drop_cutlery / drop_coin groping | sub в service/debug | ☐ |
| P3.6 | coin+cock flee / coin | гейты cock-ready | ☐ |
| P3.7 | Мелисса / кухня Сандра | intro kitchen flavor | ☐ |

### P4 — Thin memory / личный разговор

| # | Шаг | Ожидание | OK |
|---|-----|----------|----|
| P4.1 | После harass личный | **нет** «Что случилось» / «Моё решение» | ☐ |
| P4.2 | Личный разговор open | intro виден, не пустой серый экран | ☐ |
| P4.3 | Act1 early | **нет** «Запретить парней» | ☐ |
| P4.4 | Нет пункта «Недавний случай в зале» | frozen | ☐ |

### P5 — Band high / edge

| # | Шаг | Ожидание | OK |
|---|-----|----------|----|
| P5.1 | T3-пресет slut45 pol3, band часто 2 | ignore **не** копит no_protect | ☐ |
| P5.2 | watch_ok (не bad/lewd) | не копит | ☐ |
| P5.3 | protect_success | intercept count (не сразу days) | ☐ |

### P6 — Регрессия (после P1–P3)

| # | Шаг | OK |
|---|-----|----|
| P6.1 | Lewd / missing debug start не сломан | ☐ |
| P6.2 | GirlTalk обычные темы | ☐ |
| P6.3 | Daily aftermath при GirlRemembers* | ☐ |
| P6.4 | Kitchen harass Сандра after + policy | ☐ |

---

## 5. Известные ограничения (не баги)

- Полная обида с **одного** ignore — **не** задумано (K=3).  
- T3 без u1 не выпадает (AllowedTier).  
- Oneshot-арт harass ещё stub.  
- text_roll 2–3 варианта intro — не везде.  
- HallChoiceFamilyTalk prose жив, но **не** в UI.  
- USER-OWNED тексты (policy, family talk и т.д.) не трогать без «можно править тексты».

---

## 6. Следующие шаги после зелёного P1–P3

1. Полировка intro (text_roll, panty-хвосты).  
2. Oneshot paths по `$HallHarassFutureImagePath`.  
3. Offense на lewd/missing choices (если ещё нет).  
4. Не размораживать HallRecent без явной задачи.

---

## 7. Быстрые команды

```text
gt 'HallHarassmentGateDebugMenu'
gt 'HallHarassmentDebugStart', 'amanda', 1, 1
gt 'HallHarassmentDebugStart', 'amanda', 3, 4
gt 'HallHarassmentDebugStart', 'amanda', 3, 5, 'drop_coin', 1, 'flee'
gs 'HallHarassmentDebugPreset', 'offense_low'
gs 'OffenseDaysRegisterMismatchProtect', 'amanda', 'no_protect_low'
gs 'OffenseDaysDebugReset'
```

---

*Handoff для продолжения playtest harass/offense/memory A.*
