# ASSET inventory — hall / kitchen / missing visuals

**Канон:** `AGENTS.md` — нет пустых экранов; stub + `[VIS]` подпись; `#SceneShowVisual`.  
**Stub:** `images/common/hall_scene_stub.png` · `images/common/hall_harass_stub.png`  
**Real art flags:** `SceneArtUseReal=1` · `HallMissingArtUseReal` · `SandraKitchenArtUseReal` · `HallLewdArtUseReal` · `KitchenCustomerArtUseReal` · `KitchenLewdArtUseReal`

Не генерировать bulk art — только wiring + подписи + списки path.

**Verify:** `powershell -File tools/verify_hall_kitchen_visuals.ps1` (из корня репо).

---

## Caption convention

| Field | Rule |
|-------|------|
| `[VIS] …` | **Русским** (или short bilingual): что **должно** быть на кадре |
| `[VIS future] path.ext` | при `debug=1` или `debug_images=1` — ключ ассета для художника |
| Path | без расширения в `SceneShowVisual` ARGS[0]; ext в ARGS[3] (webp default) |

Пример:
```
gs 'SceneShowVisual', 'images/events/sandra/kitchen_hook/notice_door_enter', 'кухня: клиент у двери, из зала', 'large', 'webp'
```

---

## 1. Статус систем (код 2026-08)

| Система | Helper | Stub+[VIS] | Shipped art |
|---------|--------|------------|-------------|
| **Kitchen hook** | `SandraKitchenShowImage` | да | нет (ASSET-kitchen_hook.md) |
| **Missing** | `HallMissingGirlShowImage` | да + рус. caption | нет |
| **Missing bargain** | `HallMissingBargainShowImage` | да | нет |
| **Missing noble** | `SceneShowVisual` s1–s3 | да | нет |
| **Harass intro/after** | `HallHarassmentShow*` | да | A/M matrix + reaction |
| **Harass policy updated** | `SceneShowVisual` | да | нет |
| **Lewd hall** | `HallLewdShowImage` | да | partial base A |
| **Kitchen lewd** | `KitchenLewdShowImage` | да | нет |
| **Kitchen customer** | `KitchenCustomerShowImage` | да | folders empty |
| **Kitchen harass door** | `SceneShowVisual` notice | да | нет |
| **Noble attack** | `NobleAttackShowImage` | да | poor_young_noble.png |
| **Play coach** | `SceneShowVisual` | да | нет |
| **Tavern hall look** | `TavernHallEventShowVisual` | да | нет |
| **Family / policy talk** | `SceneShowVisual` | да | нет |
| **Debug panels** | `SceneShowVisual` | да | нет |

---

## 2. Harass — shipped (amanda / melissa)

```
images/events/{girl}/hall_harass/
  t{1|2}_type{1..4}_{u0|u1}.webp
  waitress_{1|2}_base.webp
  reaction_watch.webp | reaction_protect_hard.webp | reaction_ignore.webp
```

**Future oneshot:** `…/t{tier}_type{n}[_sub][_cock_*]_{u0|u1}[_nop].webp`  
Сандра/kitchen: stub + future key.

---

## 3. Missing path keys

| Outcome | Path (no ext) |
|---------|----------------|
| intro | `…/{g}/hall_missing/{place}_uniform{0\|1}_intro` |
| bargain | `…/bargain_{hall\|kitchen}_uniform{0\|1}` |
| peek | `…/{place}/{act}_u{0\|1}[_{finish}]` |
| after / interrupt | `…/{place}_uniform{0\|1}_{after\|interrupt}` |
| noble sN | `…/storage/noble_s{N}` |

---

## 4. Tavern hall look keys

`images/events/tavern/hall_look/{key}.webp`  
keys: closed · already_looked · look_intro · waitress_attention · cleaning_attention · calm · tips · dirty_table · slow_service · quarrel · quarrel_calm · quarrel_hard · quarrel_ignore

---

## 5. Deferred (out of this pass)

| Area | Reason |
|------|--------|
| `modules/locations/**` full entry screens | often already have location work images; inventory later |
| `modules/actions/**` sex/dialog every screen | large; not hall pipeline |
| church / port / dance event packs | separate arcs |
| Real `.webp` generation | non-goal |

---

## 6. QA

1. Rebuild `game.qsp`  
2. `debug=1` → каждый hall/kitchen event: stub/real + `[VIS]` + `[VIS future]`  
3. `powershell -File tools/verify_hall_kitchen_visuals.ps1` → fail=0  
