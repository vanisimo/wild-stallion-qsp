# Design: ambient-реплики клиентов (сервис + грязная слава)

**Статус:** backlog (осмотр / T3 harass); **часть в уговоре missing — v1** (rumor + offense refuse).  
**Связь:** `docs/design-hall-missing-bargain-offense.md` (уговор/обида/нобиль — **править prose там**), hall activity, harassment, `tavern_event_state_core`, `hall_rumors`.

---

## 0. Зачем

`tavern_reputation` и счётчики скандала/слухов уже живут в коде, но **зал почти не говорит**:

- rep падает/растёт → в основном `rep_mult` и ярлык в UI;
- `TavernScandal` / `TavernLewdFame` / `Tavern*Rumor` крутят score сцен;
- `HallRumorRegister` пишется из harass/missing, тексты есть, **print/NPC-мосты почти не consumer’ятся**.

Нужен тонкий **голос гостей**, не новая «книга слухов» и не отдельный мини-гейм.

---

## 1. Что **не** путать

| Система | Роль | Ambient? |
|---------|------|----------|
| `tavern_reputation` | обслуживание, запасы, overload → доход (`rep_mult`) | **не** гейт dirty-реплик |
| `TavernScandal` / `TavernLewdFame` | грязная слава | dirty-пул |
| `TavernGirlsEasyRumor` / `Backroom` / `Kitchen` | ambient-флаги «про что шепчут» | dirty-пул (+ score сцен) |
| `HallRumorRegister` / `HallRumorPrintLast` | след **конкретной** сцены | не заменять ambient; optional echo позже |
| Knowledge `HallMissing_*` | игрок видел / подозревает | girl talk, не client ambient |
| Pair-gossip (Amanda–Lizette и т.п.) | личные сплетки NPC | **отдельный** дизайн |

**Правило:** dirty-клиент **не** смотрит на `tavern_reputation`.  
Сервис-ворчание смотрит на **причины** (power/stock/overload), не обязательно на число rep.

---

## 2. Два пула

### Пул 1 — сервис (жалоба на проблемы)

**Где:** осмотр зала **без события** (и зеркало — кухня).

**Хуки:**

- `#TavernHallLookBuildNoEventMessage`
- `#TavernHallActivityNoEventScreen`
- `#KitchenLookBuildNoEventMessage` (опционально, тот же принцип)

**Драйверы (примеры):**

| Условие | Тон реплики |
|---------|-------------|
| `tavern_waitress_power` низкий | ждут заказ, стучат кружками |
| `tavern_cleaning_power` низкий | липкий стол / пол |
| низкие запасы food/beer/wine | «опять пусто», «разбавлено» |
| overload / 2 jobs | «одна на всех» |
| `tavern_kitchen_power` низкий (из зала) | долго еда, ор с кухни |

**Формат:** 1 короткая реплика гостя (+ опционально 1 строка наблюдения Стефана).  
**Не** каждый осмотр: есть ≥1 проблема → roll (например 50–70%).  
Нет проблем → текущий нейтральный текст (или редкий позитив позже).

Уже есть **отдельные** micro-event’ы `DirtyTable` / `SlowService` — ambient **не** дублирует их 1:1, а даёт фоновый гул между сценами.

### Пул 2 — грязная слава (вшитый, не отдельная сцена)

**Где:** существующие intro/client lines, **не** новый act.

| Место | Как |
|-------|-----|
| **Harassment intro (hard / T3)** | 1 фраза-намёк на разврат **не на все** T3, **ротация** — «слыхал, у вас…», «покажешь» |
| **Missing / bargain open** | намёки «в угол / пропадаете» — **только после существенных private**, см. **§2.1** (не soft A1–A3) |
| **Hall lewd intro** | тот же dirty-prefix-хелпер, что harass (если подключат) |
| **Kitchen customer** | сервис + dirty, если kitchen rumor / существенный progress |

**Драйверы dirty (не rep):**

- harass: T3 + ротация (+ optional scandal/lewd/easy)
- missing-слух: **существенный** progress missing, **не** сырой `PrivateCount` с soft
- `TavernScandal` / `TavernLewdFame` / `Tavern*Rumor` — усилители, не замена гейта

**Формат:** 1 sentence motive, не стена текста, не новый T-tier сцен.

---

### 2.1 Missing: когда клиент может ссылаться на «слух про пропажи»

**Канон (2026-07-31):** слухи про «водят / пропадают / в угол как…» **не** с первого private и **не** с soft A1–A3.

| Что **не** включает missing-слух | Почему |
|----------------------------------|--------|
| Soft **A1–A3** (look сиськи / hug / hand «штурвал» и аналоги M1–M3 / Sandra soft) | «Попялился / потрогал» — ещё не городская молва про трактир |
| Первый private / один soft-complete | Прецедента мало; «как все» звучит фальшиво |
| Просто `HallMissingGirlPrivateCount >= 1` | Считает и soft-пяление |

| Что **может** включить (существенное) | Идея |
|---------------------------------------|------|
| Несколько **существенных** missing-исходов | Не «1 раз», а **несколько** (ориентир **≥2–3**), где act **глубже soft A1–A3** |
| Soft-play насыщение / выход в hard | `HallMissingSoftPlayDone` / phase `hard` / шаг **A4+** (рот и дальше) — уже не «только сиськи» |
| Hard-line progress | рот / лицо / горло (A4–A6), cuni/titjob **после** soft-линейки, kitchen hard у Сандры |
| Опциональный флаг | `HallMissingRumorReady[girl]` или global, когда набрали N существенных |

**Тон по этапам (когда гейт уже открыт):**

| Этап | Клиент в open / motive |
|------|-------------------------|
| До гейта (soft A1–A3, мало substantial) | Обычный уговор **без** «слыхал / как все / пропадаете» |
| После N substantial | «В угол…», «говорят, пропадаете», «как вчера» — **намёк**, не обвинение |
| После A5 / `FlagFaceDone` (S3) | Тот же мотив, **язык прямее** (explicit bargain) — A5 **не** unlock слуха, а **жёсткость речи** |

**Черновик счётчика (уточнить при коде):**

```
substantial missing для rumor:
  - phase уже hard / SoftPlayDone = 1
  - ИЛИ private act ∈ {mouth, deepthroat, cuni, titjob, anilingus, hand_finish hard…}
     НЕ ∈ {look_tits, hug, cock_look soft A1–A3 hold-only}
  - N_substantial[girl] += 1 при peek/ignore complete такого act
  - rumor lines if N_substantial[girl] >= 2  (или 3 — playtest)
```

`TavernBackroomRumor = 1` при ignore/peek storage — **можно оставить** как score/ambient зала, но **client line «пропадаете»** в missing open всё равно ждать N substantial (не один заход в подсобку с A1).

**Не делать:** одна фраза «девки распутные» на каждый missing после unlock — **ротация** 2–4 вариантов.

### 2.2 Обида на ГГ → отказ клиентам (не ambient, но стык)

**Канон:** `docs/design-character-intimacy-arc.md` § «Обида → отказ клиентам».

Пока `GirlOffenseDays[girl] > 0`:

- **нет** play / missing / bargain;
- harass → короткая сцена **отказа гостю** + укол в хозяина (*«дворянство не заработала»*, *«пусть хозяин сиськи покажет»*…);
- **не** копить substantial для missing-слуха;
- dirty ambient «пропадаете» **не** растёт с этой девушкой.

Опционально later: обратный шёпот «у хозяина девки нос задрали» — низкий приоритет, не v1 ambient.

---

## 3. Техника (когда дойдём до кода)

Один хелпер, два режима:

```
gs 'HallClientAmbientPick', 'service' | 'dirty' [, $girl]
→ $HallClientAmbientLine   ! '' если нечего
```

| Режим | Читает |
|-------|--------|
| `service` | power / stock / overload |
| `dirty` | scandal / lewd / easy / backroom / kitchen (+ optional girl stage) |

**Лимиты:** 1 ambient-line на канал на часть дня  
(`HallAmbientServiceDayKey`, `HallAmbientDirtyDayKey` = `day_time`),  
чтобы 3 осмотра не превратились в хор.

**Встройка:**

| Место | Вызов |
|-------|--------|
| look no-event | `service` → в `$TavernHallLookMessage` / экран |
| harass intro | `dirty` → 1 `*pl` если не пусто |
| missing bargain open / first client line | `dirty` + weight backroom |
| kitchen look | `service` (+ soft dirty if kitchen rumor) |

USER-OWNED prose: **не** bulk-rewrite. Предпочтительно prefix/suffix через `$HallClientAmbientLine` / `$HallClientMotiveLine`.

---

## 4. Куда ещё (после missing) — приоритет

### Высокий
1. Service ambient в look (зал).
2. Dirty-prefix в harass intro.
3. Dirty/backroom в bargain open (не «распутные» на каждый missing).
4. Общий хелпер + lewd intro.

### Средний
5. Kitchen look / kitchen customer.
6. Tips / waitress attention events — 1 ворчание или мягкий dirty.
7. Bar / стойка — 1 реплика без сцены.
8. Girl talk «про трактир» — **девушка цитирует** клиентов (если `HallRumorGirlNoticed` / easy_rumor).
9. Ирма form offer — 1 reason-line при rumor-флагах (score уже есть).

### Низкий / Act later
10. Пятничные танцы, церковь (`ChurchTavernRumorReady`), noble, daily summary «о вас говорят».
11. Дожать consumer’ы `HallRumorPrintLast` / `*RumorReady` (Irma/Church/Legare) — **отдельный** слой, не ambient look.

### Не делать
- UI «книга слухов».
- Dirty-гейт от `tavern_reputation`.
- Отдельная кнопка «послушать клиентов».
- Спам на каждый missing/harass/осмотр.
- Смешивать с pair-gossip pools.

---

## 5. Missing **сейчас** — что добавлять?

**Решение (2026-07-31): не вшивать dirty-ambient в missing, пока не закрыт текущий пакет missing/bargain.**

| Вариант | Вердикт |
|---------|---------|
| «По одной фразе что девки распутные» на каждый missing | **Нет** |
| Слух после **1-го** private / soft A1–A3 | **Нет** — см. §2.1 |
| Слух после **нескольких substantial** (harder than soft A1–A3) | **Да, backlog** |
| A5 / FlagFaceDone = unlock слуха | **Нет** — A5 только **прямой язык** (S3) |
| Только `HallRumorRegister` как сейчас | **Оставить** на missing v-now |

**Код (уговор missing) — см. полный док:**  
`docs/design-hall-missing-bargain-offense.md`  
(`TryOffenseAnswer`, `OffenseAnswerText` по реальным `$p`, noble dig, rumor hint.)

**Ещё backlog:** service ambient в осмотре; dirty-prefix на **T3 harass** (ротация, не каждый).

Эскалация (когда дойдём) — см. §2.1:

| Состояние | Client open |
|-----------|-------------|
| soft A1–A3, N substantial ниже порога | уговор **без** «слыхал / пропадаете» |
| N substantial ≥ 2–3 | «в угол…», «говорят, пропадаете» (ротация) |
| FlagFaceDone / S3 | то же + **explicit** тон |
| high lewd + T3 harass (зал) | отдельные намёки на harass, не путать с missing-гейт |

---

## 6. Порядок реализации (когда вернёмся)

| Шаг | Что | Статус |
|-----|-----|--------|
| A | Закрыть missing / bargain / agent prose | **сейчас** |
| B | `HallClientAmbientPick` service + look no-event | backlog |
| C | dirty-prefix harass intro | backlog |
| D | dirty/backroom в bargain open (условный) | backlog |
| E | kitchen / bar / girl talk / Irma reason | backlog |
| F | HallRumor consumer’ы (print, *RumorReady NPC) | backlog, optional |

---

## 7. Открытые мелочи (не решать до кода)

- Точные пороги power/stock для service pool.
- Нужен ли позитивный ambient при хорошем staff (низкий приоритет).
- Связь severity `HallRumorRegister` с показом echo после return из missing (½ строки vs полный `HallRumorPrintLast`).
- Имена debug в панели (`IrmaRumorReady` vs `IrmaUniformRumorReady`) — почистить при consumer’ах.

---

*Зафиксировано по обсуждению: ambient ≠ tavern_reputation; два пула; dirty вшивать в harass/missing; missing сейчас не трогаем ради «одной фразы».*
