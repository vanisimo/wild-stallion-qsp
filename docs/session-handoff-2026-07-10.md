# Session handoff — 2026-07-10

Сводка для продолжения на другой машине. Ветка: `main`.

## Сборка на новой машине

```powershell
powershell -File scripts/build.ps1 -Profile dev
```

`game.qsp` в `.gitignore` — собрать после `git pull`.

---

## Сделано в этой сессии

### A–D (ранее)
- Sex cap + marathon gossip, Lizette limits, Amanda pool + overhear UI, Sandra+Becky Sunday pool.

### E — Melissa + Clarissa pool ✅
- `sunday_clarissa_melissa_talk_pick.qsps`, тексты, визит, кнопка в `wine_shop.qsps`.

### F — Inga + Irma (воскресенье) ✅
- `sunday_irma_inga_talk_pick.qsps`, визит у закрытой `IrmaShop`.

### Becky backroom peek ✅
- Файл: `modules/events/shops/becky_shop_backroom_peek.qsps`
- **Открытая лавка:** 12% при входе → «Заглянуть в заднюю».
- **Закрытая лавка:** 15% (10% ночью) → «Подсмотреть в заднюю».
- Условия: `sluttiness['becky']≥30` или `BeckyHomeSex=1`.
- **Повтор:** 1 раз/день **на тип клиента** (`BeckyShopBackroomPeekClientSeenDay[id]`).
- **Эдди:** только open + `time=2` (полдень), не в closed peek.
- Картинка: `becky/shop/backroom_peek` (placeholder до арта).
- Debug: `BeckyShopBackroomPeekDebugPanel` (sim 100×, force 100%, статистика).

#### Пул клиентов

| id | Гейт |
|----|------|
| `sailors_two` | день корабля, нет `becky_two_men` |
| `neighbor_husband`, `guard_grun`, `mayor_clerk`, `old_widower` | всегда |
| `lucas` | `IngaGuardProblem`, до `IngaLucasInviteDone` |
| `eddie_at_shop` | open-лавка, `time=2`, не воскресенье |

### Sandra+Becky — фразы peek ✅
- Все `becky_backroom_*` в `sunday_becky_sandra_talk_pick.qsps` + тексты.
- Слух Лукаса регистрирует `PlayerKnows` (rumor).

### Прочие хуки сессии ✅
- Amanda witness facts (`amanda_neighbors_peek`, `amanda_hall_lewd_witness`).
- Sandra+Draupnir Friday peek (`sandra_draupnir_friday_peek`).
- Клерк мэрии ↔ арка мэра + talk Бекки.
- **Инга + Лукас в задней:** one-shot `IngaBeckyLucasGossipTalk`, тексты по peek/слуху, хвост в Lucas arc.
- Playtest peek: debug-панель + фикс Эдди/offer.

### Изображения (частично) ✅
- `GetLocationTimeSuffix`: `time=4` → `evening` (2-й этаж и др.).
- Placeholder: `becky/shop/backroom_peek.png`, `church/window/ajar.png`.
- Брифы: `ASSET-*.txt` — остальные без PNG.

### Lizette room gate ✅
- Явные гейты `week=7` + `sunday_visits` в `AmandaLizaTalkCanTrigger` (`amandaroom`), `AmandaLizaRoomDoorCanShow`, `AmandaLizetteInAmandaRoomNow`, `AmandaLizetteTryEvent` (`room_visit`).
- Дизайн-док обновлён (`design-girl-pair-gossip-pools.md`).

---

## НЕ доделано / на потом

### Изображения
- Финальный арт вместо placeholder для backroom_peek, church/window/ajar, прочие `ASSET-*.txt`.

### Идеи (не в коде)
- Melissa+Clarissa v2 (брат, музыканты, Легаре).
- Больше Amanda witness id.
- Повторяемый peek по части дня (сейчас — по типу клиента/день).

---

## Debug-точки входа

- `SundayShopVisitsDebugMenu` — воскресные визиты, peek debug panel.
- `debug_intimacy_arc` — Инга/Lucas gossip, Becky/Eddie.
- `debug_mayor_arc` — клерк, налоги.

---

## Ключевые файлы

| Область | Файлы |
|---------|--------|
| Peek | `becky_shop_backroom_peek.qsps`, `becky_shop.qsps` |
| Sandra+Becky | `sunday_becky_sandra_talk_pick.qsps`, `sunday_shop_visits*.qsps` |
| Melissa+Clarissa | `sunday_clarissa_melissa_talk_pick.qsps` |
| Inga+Irma | `sunday_irma_inga_talk_pick.qsps` |
| Инга+Лукас talk | `girl_talk_inga*.qsps`, `inga_lucas_arc_text.qsps` |
| Мэрия/Бекки | `mayor_office*.qsps`, `talk_with_becky.qsps` |

---

## Статус этапов (design-girl-pair-gossip-pools)

| Этап | Статус |
|------|--------|
| A Sex cap + marathon | ✅ |
| B Lizette visit limits | ✅ |
| C Amanda pool + overhear UI | ✅ |
| D Sandra+Becky pool + canon | ✅ |
| E Melissa+Clarissa | ✅ |
| F Inga+Irma | ✅ |
| Becky backroom peek + сплетни | ✅ |
| Инга реакция на Lucas peek | ✅ |