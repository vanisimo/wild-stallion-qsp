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

**Inventory (static, 2026-08):** under `modules/events/**` **outside** `hall/` and `kitchen/` — **53 files, 174 `*clr`** not wired in this pass. By folder:

| Folder | files | *clr | Note |
|--------|------:|-----:|------|
| `tavern/` | 12 | 34 | ambient/work events outside hall_look |
| `dance/` | 9 | 33 | dance arc |
| `melissa/` | 7 | 22 | character modules |
| `family/` | 4 | 15 | council/home arcs |
| `sandra/` | 3 | 12 | non-kitchen sandra events |
| `inga/` | 3 | 11 | guard arc |
| `becky/` | 2 | 9 | home chain |
| `eddie/` | 1 | 9 | eddie arc |
| `engine/` | 1 | 7 | event engine |
| `legare/` | 1 | 6 | legare |
| `visits/` | 1 | 4 | visits |
| `church/` | 4 | 4 | church/spy |
| `amanda/` | 1 | 2 | amanda events |
| `port/` | 1 | 2 | port |
| `shops/` | 1 | 2 | shops |
| `georgette/` | 1 | 1 | georgette |
| `quests/` | 1 | 1 | quests |
| **total outside hall/kitchen** | **53** | **174** | wire in later VIS pass |

Also deferred:

| Area | Reason |
|------|--------|
| `modules/locations/**` entry screens | often location work images already |
| `modules/actions/**` sex/dialog | large; separate pass |
| Real `.webp` bulk generation | non-goal |

---

## 6. QA

1. Rebuild `game.qsp`  
2. `debug=1` → каждый hall/kitchen event: stub/real + `[VIS]` + `[VIS future]`  
3. `powershell -File tools/verify_hall_kitchen_visuals.ps1` → fail=0  
4. Spot-check: NobleAttack (SceneShowVisual), PlayCoach CanOffer=0 (stub), missing/kitchen ShowImage fallback (VisPrintCaption)  
