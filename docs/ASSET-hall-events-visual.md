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

## 5. Game-wide wiring (2026-08)

**Status:** structural pass **done** — every connected `*clr` location body has stub/real path via `SceneShowVisual` / `VisPrintCaption` / domain `*ShowImage` / location image helpers.

**Inventory:** ~301 `*clr` under `modules/{events,locations,actions,core,menu,npc,debug}`  
**Wired this pass:** ~215 overlays that previously had no visual helper (events outside hall/kitchen, actions/sex, shops overlays, core/debug panels).  
**Already had painters:** hall/kitchen helpers, `ShowLocationImage` / `ShowLocationTimeImage` / `TavernMainShowLocationImage` / engine ambient events, shop main screens.

**Verify:**

```
powershell -File tools/verify_hall_kitchen_visuals.ps1   # fail=0 (hall/kitchen gate)
powershell -File tools/verify_gamewide_visuals.ps1       # fail=0 (all connected *clr)
```

Future path keys for newly wired overlays follow:

`images/{module_path_without_qsps}/{location_snake}`  
example: `images/events/dance/friday_dance/friday_dance_mayor_speech`

---

## 5b. SFW art batch (2026-08, moderation-aware)

**Shipped:** **24** high-traffic SFW plates as `.webp` (+ `.png` twin) at SceneShowVisual keys.  
**List:** `tools/art_batch_sfw_keys.txt`  
**Verify:** `powershell -File tools/verify_art_batch_files.ps1` → fail=0  
**Style masters:** `images/common/style_masters/` (plaza, tavern, shop, street, office, home)

| Family | Examples |
|--------|----------|
| Plaza / Friday dances | `friday_dance_*`, Legare notice/dance start |
| Tavern | bar work, supply status, hall look, kitchen door notice, uniform talk, Legare supply talk |
| Town | mayor office, Becky porch, dinner, port alley, Draupnir shop, Irma uniform offer |
| Family | daily aftermath, offense days talk |

**Show real art in player:** `#SceneShowVisual` uses future path only when **`SceneArtUseReal = 1`** (else stub + `[VIS]`). Domain helpers (harass/missing/kitchen) already flip this flag when their own shipped art exists. For QA of this batch: set `SceneArtUseReal = 1` in save/debug (or temporarily in `GameInit` for a playtest).

**Deferred (moderation / explicit):** group_sex, sex_scene, intimacy_kinks hard, after_sex, hard missing/lewd, church sex, dark-alley sex launch, etc. — stay on **stub** + caption; do not invent fake “safe sex” plates. Full inventory buckets: session scratch / re-run classifier from `SceneShowVisual` paths.

Still **non-goal:** bulk explicit packs; full 200+ key art fill.

---

## 6. QA

1. Rebuild `game.qsp`  
2. `debug=1` → event overlays: stub/real + `[VIS]` + `[VIS future]`  
3. `powershell -File tools/verify_hall_kitchen_visuals.ps1` → fail=0  
4. `powershell -File tools/verify_gamewide_visuals.ps1` → fail=0  
5. `powershell -File tools/verify_art_batch_files.ps1` → fail=0  
6. Spot-check: FridayDanceMayorSpeech, plaza observe, mayor office, bar work, kitchen door (SFW batch); NobleAttack / missing still domain helpers  
