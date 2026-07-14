# Session handoff — 2026-07-12

Сводка для продолжения. Ветка: `main`.

---

## Сборка

```powershell
powershell -File scripts/build.ps1 -Profile dev
```

Последняя проверка: **2516** локаций, OK.

---

## Сделано в коде (эта сессия)

### Живые тексты

- `hall_choice_family_talk_text.qsps` — intro + reaction (protect/calm/encourage/default)
- `girl_talk_family_text.qsps` — полный rewrite (context, hall_hook)
- `girl_talk_tavern_text.qsps` — intro, context, hall_hook, day_event, repair_hook, fallback
- `sandra_staff_girls_reaction_text.qsps` — relief texts
- `girl_talk_personal_text.qsps`, `girl_talk_sandra_text.qsps`
- `hall_family_reactions_text.qsps` — severity split
- `npc_talk_limits.qsps` — smalltalk amanda/melissa/sandra

**Эталон тона:** прямая речь, жесты, без литературного рассказчика; не «мама-мораль», не греческая трагедия.

### Подарки (старый реестр — частичный фикс)

- `port_capital_ship.qsps` — `recipe_codex` убран из покупки (квест/поиск позже)
- `menu_girl_actions.qsps` — `MenuGirlGiftValue` + реакции Мелиссы по канону §1–3

**Новая плоская система подарков — пока только дизайн, код не переписан.**

---

## ⚠️ Система подарков — изменена (сессия 2026-07-13, коммит `4e1a194`)

**Этот раздел ниже («7 полок») — УСТАРЕВШИЙ дизайн.**  
Актуальный канон: **`docs/economy.md` §Gifts** и код `modules/core/gifts/`.

### Что сделано вчера (кратко)

| Было (план 07-12) | Стало (в коде) |
|-------------------|----------------|
| 7 полок × 6 id, ротация лавка/корабль | **2 id:** `gift_cheap` / `gift_expensive` |
| Покупка по полкам у Бекки/Ирмы/корабля | Покупка **только у корабля** (порт), лимиты в неделю |
| Сумка по типам | Сумка: до **2** ordinary, **1** expensive |
| Карточки-легенды на каждый id | Короткие тексты `gift_simple_text.qsps` (вкус по NPC) |
| Старые shelf-модули в `modules` | Перенесены в **`archive/old/gifts/`** (вне сборки) |
| Редкие мечты в полках | **Не** в shop; eavesdrop + `DreamItemKnown` (`economy.md` §4a) |

Файлы: `gift_registry.qsps`, `gift_shop_menus.qsps`, `gift_simple_text.qsps`, `panel_gift_bag.qsps`, `debug_gifts.qsps`.

---

## [ARCHIVED] Старый дизайн: 7 полок (не реализовывать)

### Принципы (архив)

| Правило | Было |
|---------|------|
| Чужой тип | не берёт |
| Простые | тратятся при вручении |
| Дорогие | не тратятся, редкая ротация |
| Сумка | 1 простой на полку (макс. 7) |
| Редкие мечты | только talk |
| Act 1 | все 7 полок сразу |

### 7 полок (архив — не код)

| Полка | Кто берёт | Где |
|-------|-----------|-----|
| Косметика | Аманда | корабль |
| Книги | Мелисса | лавка |
| Специи | Сандра | корабль |
| Семена | Бекки | лавка |
| Шитьё | Инга | лавка |
| Ароматика | Ирма | корабль |
| Афродизиаки | Кларисса | корабль |

Тексты карточек (специи, книги и т.д.) — справочно в `archive/old/gifts/*_text.qsps` и переписке 07-12.  
**Не** возвращать в `qsp-project` без явной просьбы.

### Старый «следующий шаг» (закрыт / перенесён)

1. ~~Ротация полок~~ → упрощение cheap/expensive.
2. ~~Убрать 22 id~~ → archive.
3. Квест мечт (`recipe_codex`, огурцы…) → `economy.md` §4a, eavesdrop.
4. Дорогие как отдельный id — **уже есть** `gift_expensive` (корабль).

---


## Коммит этой сессии (диалоги + частичный фикс подарков + handoff)

См. git log; полная перепись подарков — **следующая сессия**.