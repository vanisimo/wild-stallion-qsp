# Hall Missing — Сандра: порядок, лесенка, схема

**Дата:** 2026-08-11  
**Статус:** канон wiring (код) + карта prose  
**Код:** `hall_missing_bargain.qsps` (phase + ApplyPromise)  
**Prose:** `hall_missing_agent_sandra_text.qsps` (USER-OWNED)  
**Уговор (1 экран):** `hall_missing_bargain_text` / `docs/review_hall_missing_bargain_unified_v2.md`  
**Связь:** `docs/design-hall-missing-bargain-catalog.md`

---

## 0. Рамка (владелец)

| # | Решение |
|---|---------|
| 1 | **Один** уговор перед missing: «уединение / ласка за монету» — **не** меню услуг |
| 2 | Расширение («**уговор на большее**») — **внутри** Scene missing |
| 3 | Сандра: **только кухня** (печь / стол / стена / ларь / ящик / бочка) |
| 4 | Нобиль: **off** |
| 5 | Initiative low/high **нет** — тон = progress / `FlagMouthMature` |
| 6 | Hard mouth first-show: **6 шагов**, **без** этапа «DT + кашель» |
| 7 | **Метки типажа клиента** (prose + free-bias) — см. §3a |

---

## 3a. Метки типажа клиента (канон 2026-08-11)

Код: `#HallMissingApplyClientFlavorTags` в `hall_missing_girl.qsps`  
Вызов: после `PickClient` и в `EnsurePrintContext`.

| `$HallMissingClient` | Член (`$HallMissingClientCock`) | Prefer act | Prefer finish | Cum heavy | Prose-якорь |
|----------------------|---------------------------------|------------|---------------|-----------|-------------|
| **traveler / sailor** (моряк) | **`big`** — большой | **`hand`** — работа **рукой** | `hand` | 0 | `hand_sandra`: акцент на толщине/длине, handjob |
| **rich_merchant** (купец) | **`thick`** — **толстый** | **`mouth`** — **отсос** | **`cum_mouth`** — **в рот** | 0 | `mouth_mid` / swallow: толстый ствол, finish в рот |
| **craftsman / local** (мастеровой) | `average` | **`facial`** | **`cum_face`** | **1** — **обильно** | `facial_sandra`: много семени на лицо |
| **drunk_guest** | — | — | — | 0 | уговор срывается, missing нет |

**Переменные:**
- `$HallMissingClientCock` = `big` | `thick` | `average` | `''`
- `$HallMissingClientPreferAct` = `hand` | `mouth` | `facial` | `''`
- `$HallMissingClientPreferFinish` = `hand` | `cum_mouth` | `cum_face` | `''`
- `HallMissingClientCumHeavy` = 0/1 (мастеровой: обильный finish)

**Как использовать в prose:**
```
if $HallMissingClientCock = 'big': … большой …
if $HallMissingClientCock = 'thick': … толстый …
if HallMissingClientCumHeavy = 1: … обильно / много струй …
if $HallMissingClientPreferAct = 'hand': ветка hand …
```

**Free hard bias (Сандра):**  
моряк → чаще `hand_quick` / titjob; купец → `mouth_hard` (+ finish в рот); мастеровой → `facial` (+ heavy).  
First-show hard ladder **не** ломается метками — только free и текст.

---

## 1. Два слоя

```
[Кухня] Гость заходит
    → УГОВОР (1 экран): client × Explicit × rumor × (offense=отказ)
    → Intro (занавеска) → peek / ignore / interrupt
    → Scene = $HallMissingPrivateAct (+ $HallMissingFinish)
         внутри: «уговор на большее» (если не pure hold)
    → Meet (Стефан у щели)
    → PhaseAdvance
```

---

## 2. Фазы (общая машина)

| `$HallMissingPhase[sandra]` | Смысл | N first |
|-----------------------------|--------|---------|
| `soft_intro` | A1→A2→A3 **hold only** | 3 |
| `soft_play` | random soft ± break | N=3 |
| `hard` | mouth ladder sub 0..5 | 6 peeks |
| `free` | random soft S3 + hard terminals | ∞ |

После hard ladder done → `free`, `FlagMouthMature = 1`.  
Mature также при hard sub counter ≥2 (после проглота / show path progress).

---

## 3. Soft-лесенка (темы → acts)

| Тема | Hold (intro) | Break (play) | Post / free (S3) |
|------|--------------|--------------|------------------|
| **A1 грудь** | `look_tits` | `tits_lick` | `titjob` |
| **A2 попа** | `hug_waist` | `petting` → `pussy_touch` | `cuni`, `anilingus` |
| **A3 рука** | `cock_touch_cloth` | `hand` | `mouth` (минет) |

**Break** = +1 ступень внутри темы, не прыжок в hard terminal.

---

## 4. Hard mouth first-show (×6, **без cough**)

Код: `HallMissingHardSubMax = 6`, promise `mouth_hard`.

| Sub | `$HallMissingPrivateAct` | `$HallMissingFinish` | Scene key | Содержание | «На большее» |
|-----|--------------------------|----------------------|-----------|------------|--------------|
| **0** | `mouth` | `cum_mouth` | `mouth_mid_sandra` | минет → **в рот** | base = рот; «кончай в рот» |
| **1** | `mouth` | `swallow` | `mouth_swallow_sandra` | **проглот** | «не выплёвывай / глотни» |
| **2** | `mouth` | `show_mouth` | `mouth_show_sandra` | **покажи** во рту | «открой рот» |
| **3** | `mouth` | `cum_face` | `facial_sandra` | **на лицо** | «не в рот — на лицо» |
| **4** | `deepthroat` | `cum_mouth` | `deepthroat_sandra` | DT + **в рот** | «глубже… и в рот» |
| **5** | `deepthroat` | `cum_throat` | `deepthroat_sandra` | DT + **в горло** | «до конца / в горло» |

**Убрано (2026-08-11):** sub «DT + `cough` / кашель first» — не в first-show, не отдельный finish.

После sub 5 (6-й peek) → `HardLadderDone`, phase `free`.

### Free / random terminals (после лесенки)

Типично: `mouth_hard` / `facial` / `deepthroat` / `titjob` + soft S3.  
`deepthroat_sandra` читает `$HallMissingFinish` (`cum_mouth` | `cum_throat` | free-варианты).

---

## 5. Переходы Scene → Meet → дальше

Каждый peek:

```
HallMissingPrintPeekScene
  → #HallMissingScene_<key>_sandra
  → (act UI: дальше / meet …)
  → #HallMissingMeet_<key>_sandra
  → HallMissingPhaseAdvance  ! +1 intro/play/hard sub
```

| Scene | Следующий first-show (hard) | Soft next (логика темы) |
|-------|----------------------------|-------------------------|
| `look_tits` | — | break → `tits_lick` / free → `titjob` |
| `tits_lick` | — | free → `titjob` |
| `titjob` | — | terminal soft |
| `hug_waist` | — | break → `petting` |
| `petting` | — | deeper → `pussy_touch` |
| `pussy_touch` | — | free → `cuni` / `anilingus` |
| `cuni` / `anilingus` | — | terminal soft |
| `cock_touch_cloth` | — | break → `hand` |
| `hand` | hard entry mouth | free → mouth* |
| `mouth_mid` | → swallow (sub1) | free mouth terminal |
| `mouth_swallow` | → show (sub2) | mature tone on |
| `mouth_show` | → facial (sub3) | |
| `facial` | → DT cum_mouth (sub4) | |
| `deepthroat` (cum_mouth) | → DT cum_throat (sub5) | |
| `deepthroat` (cum_throat) | → **free** | |

---

## 6. Карта prose-статуса (файл agent)

| Scene | Статус | Приоритет дописки |
|-------|--------|-------------------|
| Intro / Ignore / Interrupt | OK | — |
| look_tits, hug_waist, cock_touch_cloth | OK hold | — |
| tits_lick, petting, pussy_touch, hand | OK; добавить дожим | P1 |
| titjob | OK (+ client split) | P2 craftsman |
| cuni, anilingus | тонко / short | P0 soft free |
| mouth_mid | thin — **P0 hard** | base + в рот |
| mouth_swallow | OK | P1 дожим «глотни» |
| mouth_show | stub | **P0** |
| facial | stub | **P0** |
| deepthroat | stub + ветки finish | **P0** |
| mouth_wipe / taste / hold_spit | sister leftovers | P3 |
| mouth_spit | prose OK, hard path не first | P2 |
| noble | off | не писать |

---

## 7. Шаблон «уговор на большее» в Scene

1. Старт = обещанное (осмотр / юбка / рука / **рот**).  
2. Клиент 1–2 реплики дожима.  
3. Сандра early: «ладно, тихо»; mature: коротко, грязно.  
4. Действие + finish.  
5. Meet 1–2 фразы.

Hard mouth: уговор **до** missing = минет; facial / DT — **только** внутри Scene.

---

## 8. Wiring checklist (код проверен 2026-08-11)

| Место | Ожидание | Статус |
|-------|----------|--------|
| `HallMissingHardGetSlot` sandra | SubMax **6**, slot mouth | OK |
| `ApplyPromise` sandra mouth_hard | 0..5 map без `cough` | OK |
| `PhaseAdvance` | sub≥2 → MouthMature; sub≥6 → free | OK |
| `ResolveSceneKey` | finish→ scene keys | OK |
| `cough` finish | **не** выдаётся Сандре | OK (снят) |

---

## 9. Порядок письма prose (волны)

**A — hard first-show:** `mouth_mid` → `mouth_show` → `facial` → `deepthroat` (×2 finish) → polish `mouth_swallow`  
**B — soft free:** `cuni`, `anilingus`, дожимы soft break  
**C — leftovers:** wipe/taste/hold_spit, thigh  

В `hall_missing_agent_sandra_text.qsps` у каждой Scene — `!` комментарий: **что в сцене** + **куда переходит**.
