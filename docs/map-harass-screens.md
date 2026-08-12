# Карта экранов harass (чтобы не теряться)

**Нужен rebuild `game.qsp`**, иначе в игре старый текст.

---

## Два экрана

| | Экран 1 | Экран 2 |
|--|---------|---------|
| Заголовок | `НЕПРИЯТНЫЙ СЛУЧАЙ` | `ПОСЛЕ: ЗАЛ` / `ПОСЛЕ: КУХНЯ` |
| Картинка | intro (лапают) | watch/protect = reaction_*; **ignore = стойка** |
| Текст | intro — **только захват** | блоки A→B→C→D ниже |
| Меню | Защитить / Наблюдать* / Отвернуться* | «Обсудить правило…» + act Главный зал |

\* после семейного ужина

---

## Экран 2 — блоки (сверху вниз)

```
[A] картинка
[B] ── Что произошло ──     ← hall_harassment_after_text.qsps
      watch  = видно сцену ($HallHarassSceneBeat)
      ignore = звуки из ТОЙ ЖЕ сцены
      protect = клиент ушёл + она
[C] ── Имя ──               ← talk_watch/ignore/protect band 0–3
      реплика к Стефану (коррупция)
[D] ── На будущее ──        ← girl_work_policy_talk_text (смягчённо)
      меню: сдержанно / сама / расковано
```

---

## Какие файлы править

| Файл | Что |
|------|-----|
| `hall_harassment_intro_text.qsps` | **Экран 1** — схватили (USER-OWNED) |
| `hall_harassment_after_text.qsps` | **Экран 2** B+C — сцена, звуки, реплики |
| `girl_work_policy_talk_text.qsps` | **Экран 2** D — мост policy |
| `hall_harassment.qsps` | логика, меню, картинки |
| ~~не смотреть~~ `hall_harassment_text.qsps` | legacy / talk-recall; live after **не** отсюда |

---

## Один roll сцены

`$HallHarassSceneBeat`: `hand_bare` | `grab_tits` | `grab_ass` | `wall` | `drop_bend` | `play_tip` | …  
`HallHarassSceneSlap` 0/1  

Watch и ignore берут **один** beat.

---

## Если «ничего не поменялось»

1. Build → `game.qsp` (Sublime qsp-build-and-run)  
2. Новая сцена harass (не старый сейв mid-event)  
3. Debug: строка `[DEBUG AFTER] choice=… beat=… slap=… band=…`  
4. Заголовок должен быть **`ПОСЛЕ: ЗАЛ`**, не старый `ПОСЛЕ СЛУЧАЯ` + «безучастие»
