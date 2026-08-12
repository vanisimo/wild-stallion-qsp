# ASSET: Sandra kitchen_hook + hall_missing visuals

**Канон (AGENTS.md):** во всей игре нет экранов без картинки.  
Сейчас: stub `images/common/hall_scene_stub.png` + подпись `[VIS] …`.  
Helper: `#SceneShowVisual` — path future + caption.  
Когда файлы появятся: `SceneArtUseReal = 1` или `SandraKitchenArtUseReal = 1` / `HallMissingArtUseReal = 1`.

## kitchen_hook (notice из зала)

| key | path (webp) | смысл |
|-----|-------------|--------|
| **notice_door_enter** | `images/events/sandra/kitchen_hook/notice_door_enter.webp` | зал: мужик заходит за кухонную занавеску/дверь |
| bargain_harass | `.../bargain_harass.webp` | уговор harass у печи |
| bargain_play | `.../bargain_play.webp` | уговор play |
| bargain_refuse | `.../bargain_refuse.webp` | пьяный / отказ |
| watch_harass | `.../watch_harass.webp` | подсмотр harass |
| watch_play | `.../watch_play.webp` | подсмотр play |
| escalate | `.../escalate.webp` | мост play→missing |
| protect | `.../protect.webp` | Стефан ворвался |
| offscreen | `.../offscreen.webp` | зал, слушает звуки (дверь/занавеска) |

Missing peek/meet: через `HallMissingGirlShowImage` → `hall_missing/kitchen/...`

## hall_missing (все девушки)

`images/events/<girl>/hall_missing/<place>_uniform0|1_<outcome>.webp`  
или scene: `.../<place>/<act>_u0[_finish].webp`

outcomes: intro, peek/scene, after, interrupt, bargain_kitchen / bargain_hall

## Включить real art

```
SandraKitchenArtUseReal = 1
HallMissingArtUseReal = 1
```
