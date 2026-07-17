# Design: thin hall memory (variant A)

**Статус:** канон 2026-07  
**Связь:** `docs/state.md`, `GirlMemoryOfStefan`, `HallChoiceMemory`, `SaveLastHallEvent`

## Решение

Не три параллельные «памяти», а **две живые оси + лог**:

| Ось | Owner | Зачем |
|-----|--------|--------|
| **Долгий стиль хозяина** | `GirlMemoryOfStefan` → `GirlRemembers*` | DailyAftermath, italic after choice, personal scales |
| **Последний выбор (snapshot)** | `HallChoiceMemory` → `$LastHallChoice*` / `$LastGirlChoice*` | family/tavern talk hooks, choice family talk |
| **Лог сцены** | `SaveLastHallEvent` | панель таверны, тема «Что случилось в зале» |

## Frozen

| Модуль | Состояние |
|--------|-----------|
| `hall_recent_memory.qsps` | **no-op** (`HallRecentMemorySave` игнор) |
| `hall_recent_talk.qsps` | **CanShow = 0**; Start → fallback hall_event |
| Меню «Недавний случай в зале» | **убрано** |

Не удаляем файлы: старые `gs`/`gt` не должны падать.

## Не путать

- **Не** `if lewd: harass memory off` — memory пишет любой hall choice через `HallChoiceConsequencesApply`.
- **Не** плодить третий ledger под type/tier harassment.
- Счётчики `HallChoiceProtectByGirl` / dirty — вторичны (debug/legacy); для сюжета смотреть `GirlRemembers*`.

## Запись (один пайплайн)

```
hall/kitchen/lewd/missing resolve
  → HallChoiceConsequencesApply
       → HallChoiceMemorySave   (snapshot)
       → HallFamilyStateApply
       → GirlMemoryOfStefanRegister  (long-term + DailyAftermathPending)
  → SaveLastHallEvent (из event-specific RegisterLast)
```

## Разговоры игрока

| Тема | Источник | В личном меню |
|------|----------|----------------|
| После harass (итог + policy) | сама сцена harass | **не дублируем** |
| «Что случилось в зале» | `$LastHallEvent*` | **убрано** (дубль after) |
| «Моё решение в зале» | `HallChoiceFamilyTalk` / `$LastHallChoice*` | **убрано** из меню (код/тексты живы) |
| «Как она выполнила правило» | policy-response | если реально pending |
| «Реакция семьи» | family reaction | если CanDiscuss |
| Policy after на сцене | policy system | сразу после harass |

## Debug

- `GirlMemoryOfStefanDebugPanel`
- `HallChoiceMemoryDebugPanel` (snapshot)
- Panel: сброс `GirlRemembers*`
