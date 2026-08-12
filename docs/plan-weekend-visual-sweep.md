# План на выходные: visual на всех экранах

**Статус:** отложено (не делать до напоминания)  
**Когда:** суббота вечер / выходные  
**Канон:** `AGENTS.md` — нет пустых экранов; stub + `[VIS]` подпись; `#SceneShowVisual`

## Уже сделано

- `#SceneShowVisual` — stub + caption + future path  
- Kitchen hook Сандры — visual на каждом экране  
- Missing agent (print dispatch) — visual + подпись  
- Правило в `AGENTS.md`

## Сделать на выходных (массовый проход)

1. **Inventory** — экраны с `*clr` / `gt` без `ShowImage` / `SceneShowVisual` / location image:
   - `modules/locations/**`
   - `modules/events/**` (entry + resolve)
   - `modules/actions/**` (диалоги, сундуки, окна, street sex…)
2. **Stub + caption** на каждый найденный экран:
   ```
   gs 'SceneShowVisual', 'images/…/future_key', 'подпись: что на кадре'
   ```
3. **ASSET-списки** по папкам (`ASSET-*.md`) — path + смысл, без выдуманного арта.
4. **Не** генерировать bulk art; только wiring + подписи.
5. Спорные кадры — спросить владельца.

## Не трогать

- USER-OWNED prose (только logic + image call рядом)  
- `qsp-project.json` без явной просьбы  

## Напоминание

Durable scheduler: напомнить в **субботу вечером** при подключении / срабатывании задачи.
