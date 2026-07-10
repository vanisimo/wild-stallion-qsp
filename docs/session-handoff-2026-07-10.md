# Session handoff — 2026-07-10

Сводка для продолжения на другой машине. Ветка: `main`.

## Сборка на новой машине

```powershell
powershell -File scripts/build.ps1 -Profile dev
# или: powershell -Command "& 'E:\TraKtir\scripts\build.ps1' -SkipCheck"
```

`game.qsp` в `.gitignore` — собрать после `git pull`.

---

## Сделано в этой сессии

### A. Sex cap + marathon gossip (этап A дизайна)
- Лимит оргазмов девушки за сцену (8/7/6 по tier).
- `SexMarathonGossipPending[girl]`, cooldown 7 дней для пула сплетен.

### B. Лимиты Lizette (этап B)
- Визиты в зал / комнату по неделе; гейт `week=7` для room talk.

### C. Amanda + Lizette pool (этап C)
- Новые id в `amanda_liza_talk_pick.qsps` / `amanda_liza_talk_text.qsps`.
- `marathon_exhausted` tier 7, `legare_deflower`, witness-фразы.
- **Overhear UI:** только «Подслушать» + «Вернуться»; убраны forbid/lift/scold и вся похвала.
- **Личные разговоры:** баны Lizette/Legare/guys в `girl_talk_personal.qsps`; перерисовка `GirlTalkMainMenu` без второго dropdown.

### D. Sandra + Becky Sunday pool (этап D)
- Новый файл `sunday_becky_sandra_talk_pick.qsps` (BuildPool, gates, effects).
- Тексты в `sunday_shop_visits_text.qsps`; цепочка gear → scandal → pool → fallback.
- **Канон в текстах:**
  - Сандра **ходит к мэру**, не наоборот.
  - Драупнир **коренастый**, молот по **наковальне** (не «маленький» в постели).
  - Бекки: **задняя комната**, матросы **сразу вдвоём / в два ствола**, **регулярные** гости.
  - Стефан **подглядывает** в щель (в текстах и в геймплее).

### Becky backroom peek (новая механика)
- Файл: `modules/events/shops/becky_shop_backroom_peek.qsps`
- **Открытая лавка:** 12% при входе → строка «из задней…» + «Заглянуть в заднюю».
- **Закрытая лавка:** 15% (10% ночью) → «Подсмотреть в заднюю» (не мешает воскресному подслушиванию Сандры).
- Условия: `sluttiness['becky']≥30` или `BeckyHomeSex=1`; 1 раз/день.
- Кнопка с рынка **убрана** — только через лавку.

#### Пул клиентов в задней (согласовано)

| id | Кто | Гейт |
|----|-----|------|
| `sailors_two` | Двое матросов | день корабля, пока нет `becky_two_men` |
| `neighbor_husband` | Муж соседки | всегда |
| `guard_grun` | Сержант Грюн | +вес при `IngaGuardProblem` |
| `mayor_clerk` | Клерк мэрии | всегда |
| `old_widower` | Старый вдовец-постоянный | всегда |
| `lucas` | Лукас | `IngaGuardProblem=1`, `IngaLucasInviteDone=0` (побои от Грюна, Инга не пустила) |
| `eddie_at_shop` | Эдди у прилавка | только `time=2`: в задней гость, спереди сын считает монеты |

**Убрано из пула:** купец, пьяный из трактира, налоговый инспектор.

#### Факты witness (для пулов сплетен)

- `becky_two_men` — матросы
- `becky_backroom_guard`, `becky_backroom_neighbor`, `becky_backroom_clerk`
- `becky_backroom_old_client`, `becky_backroom_lucas`, `becky_backroom_eddie_near`

### Прочее в diff (та же сессия / смежные правки)
- Sex scene texts/poses, intimacy kinks, amanda room/lizette, tavern hall, debug panels.
- `docs/design-girl-pair-gossip-pools.md` — дизайн этапов A–F.
- Asset-заглушки изображений (`images/locations/ASSET-*.txt`, evening jpg/png).

---

## НЕ доделано (следующие шаги)

### Этап E — Melissa + Clarissa pool
- По `docs/design-girl-pair-gossip-pools.md` §6.
- Расширить `SundayVisitClarissaMelissaText` паттерном `BuildPool` (как Sandra+Becky).
- Уже есть вставка `MelissaHomeSex` + bond≥12 — обернуть в полноценный пул.

### Этап F — Inga + Irma (воскресенье)
- Задел в дизайне §7; файлов кода нет.

### Пул Sandra+Becky — фразы на новые факты peek
- `becky_backroom_lucas`, `becky_backroom_clerk`, `becky_backroom_guard` и т.д. **не** добавлены в `sunday_becky_sandra_talk_pick.qsps`.
- Сейчас в пуле только `becky_two_men` с жёстким witness; остальные факты регистрируются, но Бекки о них **не болтает** Сандре.

### Playtest / баланс
- Шансы peek (12%/15%/10%) не калибровались в игре.
- Не проверено: конфликт `eddie_at_shop` только при открытой лавке в полдень vs peek с закрытой.

### Lizette room gate (из дизайна)
- Явный `week=7` в `AmandaLizaTalkCanTrigger` для `amandaroom` — помечено в дизайне, уточнить в коде.

### Изображения
- `ASSET-*.txt` и `tavern/second_floor/evening.*` — заглушки/черновики, не подключены в `ShowImage`.

---

## Идеи на потом (не в коде)

1. **Сплетни Бекки→Сандра** по каждому `becky_backroom_*` (одношоты, tier 1–2).
2. **Melissa+Clarissa:** брат, музыканты, ревность Легаре — таблица в дизайне v2.
3. **Amanda pool:** больше witness id (`amanda_neighbors_peek_*`, `amanda_hall_lewd_witness`) — регистрация при подгляде.
4. **Пятничный Sandra+Draupnir** (`SandraDraupnirFridayVisit`) + подглядывание у мастерской — параллель peek-системе Бекки.
5. **Клерк в задней** — связать с аркой мэра (`MayorClerkAdviceGiven`, налоги) в talk, не только в тексте peek.
6. **Лукас в задней** — реакция Инги, если `PlayerKnows['becky_backroom_lucas']` через слух/подслушивание.
7. **Повторяемый peek** — сейчас 1/день; можно разделить «видел сегодня» по типу клиента, не глобально.

---

## Debug-точки входа

- `SundayShopVisitsDebugMenu` — воскресные визиты, пул Sandra, матросы witness, задняя (Лукас / Эдди).
- `panel_debug_tools` / `debug_amanda_liza` — Amanda+Lizette.
- `debug_intimacy_arc` — Becky/Eddie/Sandra+Becky пресеты.

---

## Ключевые файлы сессии

| Область | Файлы |
|---------|--------|
| Дизайн | `docs/design-girl-pair-gossip-pools.md` |
| Amanda overhear / personal | `amanda_liza_overhear.qsps`, `girl_talk_personal.qsps` |
| Amanda pool | `amanda_liza_talk_pick.qsps`, `amanda_liza_talk_text.qsps` |
| Sandra+Becky | `sunday_becky_sandra_talk_pick.qsps`, `sunday_shop_visits*.qsps` |
| Becky peek | `becky_shop_backroom_peek.qsps`, `becky_shop.qsps` |
| Sex/marathon | `sex_scene_core.qsps`, `sex_register.qsps`, `next_day.qsps` |

---

## Статус этапов (design-girl-pair-gossip-pools)

| Этап | Статус |
|------|--------|
| A Sex cap + marathon | ✅ |
| B Lizette visit limits | ✅ |
| C Amanda pool + overhear UI | ✅ |
| D Sandra+Becky pool + canon | ✅ |
| E Melissa+Clarissa | ❌ следующий |
| F Inga+Irma | ❌ |
| Becky backroom peek | ✅ (без сплетен по новым фактам) |