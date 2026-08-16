# План: visual на всех экранах

**Статус:** **game-wide structural pass done** (2026-08)  
**Канон:** `AGENTS.md` · helper `#SceneShowVisual`  
**Инвентарь:** `docs/ASSET-hall-events-visual.md`  
**Verify:**  
- `tools/verify_hall_kitchen_visuals.ps1` (hall/kitchen gate)  
- `tools/verify_gamewide_visuals.ps1` (все connected `*clr`)

## Сделано

### Hall/kitchen pipeline
- Kitchen hook, missing peek/bargain/meet/noble  
- Harass intro/after/policy + kitchen door notice  
- Lewd hall + kitchen lewd + kitchen customer  
- Noble attack, play coach  
- Tavern hall look events  
- Family reaction / choice talk / policy response talk  
- Debug: girl memory panel, hall_scene_v2 probe  

### Game-wide (outside hall/kitchen)
- `modules/events/**` dance, tavern/legare, melissa, family, sandra, inga, becky, eddie, engine, church, port, …  
- `modules/actions/**` sex / group_sex / policy & uniform talk / bar work  
- `modules/locations/**` shop overlays, mayor office, hall activity no-event  
- `modules/core/**` supply, offense days, event state debug, girls_desc  
- `modules/debug/**` debug panels  
- Stub + Russian `[VIS]` caption; `debug=1` → `[VIS future] path`

## Дальше (optional)

1. Real `.webp` under future keys (no logic change)  
2. Per-arc ASSET lists with final captions for artists  
3. Runtime playthrough spot-check in QSP 5.90  

## Не трогать

- USER-OWNED prose (только image call)  
- `qsp-project.json` без просьбы  
