# Design: soft → high → Explicit, лестницы, гейты, диалоги после

**Статус:** снимок кода + канон обсуждений (2026-08)  
**Системы:** hall/kitchen **harassment** + hall **missing** (bargain + phase ladder)  
**Код (истина runtime):**  
- `modules/events/hall/hall_missing_bargain.qsps` — phase, Explicit, initiative, promise→act  
- `modules/events/hall/hall_missing_bargain_text.qsps` — реплики уговора  
- `modules/events/hall/hall_missing_bargain_hooks.qsps` — offense / rumor  
- `modules/events/hall/hall_missing_girl.qsps` — flow, dispatch сцен  
- `modules/events/hall/hall_missing_agent_*_text.qsps` — **USER-OWNED** prose сцен (soft/high/Explicit внутри)  
- `modules/events/hall/hall_harassment.qsps` — stance/play, after band, policy  
- `modules/events/hall/hall_harassment_after_text.qsps` — after talk  

**Связано:**  
`design-hall-harassment.md` · `design-hall-scene-unified.md` · `design-hall-missing-bargain-catalog.md` · `design-hall-missing-sandra-ladder.md` · `design-hall-missing-bargain-offense.md` · `design-hall-missing-layers.md` · `design-hall-missing-finger-count.md` · `prose-hall-missing-pack-map.md` · `ASSET-hall-events-visual.md`

---

## 0. Три «языка» — не путать

В проекте **три разных оси**, которые все называют soft/high/explicit:

| Ось | Где | Значения | Смысл |
|-----|-----|----------|--------|
| **A. Phase ladder** | missing progress | `soft_intro` → `soft_play` → `hard` → `free` | **какая дорожка** сейчас (что обещают / какой слот hard) |
| **B. Bargain Explicit** | уговор | `HallMissingBargainExplicit` 0\|1 | **прямой язык** в уговоре (не эвфемизмы) |
| **C. Scene tone** | prose сцены | soft / `$HallMissingInitiative=high` / Explicit | **как ведёт себя тело/тон** в agent text |

**Harass** использует **другую** тройку: stance `resist | endure(mixed) | play(provoke)` + after-band 0…3 + policy 1…3.  
Missing **не** открывается «типом harass T1–T3»; мост — **play + coach + liberation** (см. §6).

---

## 1. Axis B — Explicit (уговор)

### 1.1 Когда включается (`#HallMissingBargainIsExplicit`)

| Девушка | Explicit = 1 если |
|---------|-------------------|
| **Аманда / Мелисса** | `HallMissingFlagFaceDone[girl] = 1` — после **первого hard-лица** (слот `face` добит) или при закрытии hard ladder |
| **Сандра** | `HallMissingFlagMouthMature['sandra'] = 1` — после **зрелого рта** (sub ≥ 2 на mouth-лестнице или ladder done) |

### 1.2 Что меняет Explicit = 1

| Область | Explicit = 0 | Explicit = 1 |
|---------|--------------|--------------|
| Уговор prose | эвфемизмы: «только гляну», «бутончик», «штурвал» | **прямой** язык; soft-слоты тоже откровенные |
| Soft promises (look/hug/hand) | hold / mid | часто **break** (`HallMissingPromiseBreak = 1`) — «сразу делом» |
| free-фаза style roll | soft 60% / hard 40% | soft 45% / hard **55%** |
| initiative (часто) | low (если stage низкий) | **high** |
| face finish | `cum_face_soft` на early sub | `cum_face_high` |

**S3 (обсуждение catalog):** после FlagFaceDone soft **не убиваем**; soft-слоты живут, но тон = Explicit; meta «ерунда или делом» в prose / break.

### 1.3 Как говорят в уговоре (канон ответов)

| Explicit | Тон клиента | Тон девушки (если «да») |
|----------|-------------|-------------------------|
| **0 soft** | осторожно, «только посмотрю / обниму / рукой» | смущение, торг, «только это», «быстрее» |
| **0 hard (mid ladder)** | уже hard promise (рот/лицо/cuni), но без S3-флага | стыд + согласие по цене/страху |
| **1** | без экивоков: куда кончить, горло, «как в прошлый раз» | **единый откровенно-томный** ответ (catalog §32: без ложной ветки «low»); сёстры — кураж/ирония; Сандра — зрелый pragmatic |

Отказ при **обиде** (`GirlOffenseDays > 0`, не noble):  
`#HallMissingBargainTryOffenseAnswer` → только **ответ отказа** по `$HallMissingPromise`, без входа в missing.  
См. `design-hall-missing-bargain-offense.md`.

---

## 2. Axis C — soft / high / Explicit **внутри сцены** (prose)

В `hall_missing_agent_*_text.qsps` типичный шаблон:

```
if HallMissingBargainExplicit = 1:
    … Explicit prose …
elseif $HallMissingInitiative = 'high':
    … high prose …
else
    … soft / base …
end
```

Плюс ветки по `$HallMissingClient` (traveler / craftsman / rich_merchant) и finish (`$HallMissingFinish`, `$HallMissingHandFinish`).

### 2.1 Откуда `$HallMissingInitiative` (`#HallMissingBargainPickPromise`)

| Условие | Initiative |
|---------|------------|
| phase = `soft_intro` | **low** (всегда) |
| `HallMissingBargainExplicit = 1` | **high** |
| `GirlHallLewdStage[girl] ≥ 3` **или** `HallMissingGirlStage ≥ 4` | **high** |
| иначе | **low** |

**Сандра:** в catalog — **нет** split low/high initiative как у сестёр; тон = progress (phase/step). В prose всё равно часто смотрят Explicit + client.

### 2.2 Что должно быть в soft / high / Explicit (канон pack)

Ниже — **целевой** смысл кадров (как обсуждали + pack map).  
Факт наличия локаций — §7.

#### Soft (hold / early)

| Act | soft | high | Explicit |
|-----|------|------|----------|
| **look_tits / look_line** | смотрит вырез, хвалит, не лезет глубоко | трогает / сжимает | лижет / «как в прошлый раз» / break |
| **hug_waist** | обнимашки, запах, лёгкий поцелуй | рука на попе / hard hug | petting / «делом» / org path |
| **hand / touch_cock** | cloth → осторожно | bare / ритм | finish mouth/face/panties |
| **touch_thigh / H0 smell** | нюх, восхищение, «молодость» | целует, мокро | пальцы + оргазм / cuni bridge |
| **cuni** | снаружи, осторожно | язык внутрь, она жмёт | + пальцы/anil page3 (сёстры late) |
| **mouth** | **wipe/taste = МОСТ soft\|high only** (S-AM-06; Explicit clamp→high) | spit / hold_spit = **first-show only** (07/08) | 09 swallow; **11 show = full, free-random после лесенки** (не first-show). Free: 09 или 11, без wipe/taste/spit |
| **facial** | визит 1: на грудь (тон soft/high) | визит 2: низ лица+рот (тон soft/high) | визит 3: на лицо → FlagFaceDone / Explicit. Free: только Explicit |
| **deepthroat** | try **на пол** / partial **на грудь** / full **на лицо** (одно начало) | — (слоёв нет, уже Explicit) | cum_mouth / cum_throat в free |

#### После сцены — `HallMissingMeet_*` (встреча со Стефаном)

| Тон сцены | Как **должна** говорить после (meet / recall) |
|-----------|-----------------------------------------------|
| **soft** | «он только смотрел / обнял», стыд, «ты вовремя / не смотри так», просьба не раздувать |
| **high** | смешанно: злость + возбуждение, «я сама… почти», торг «не говори семье», ирония (Мелисса) |
| **Explicit** | циничнее / томнее: «уже не первый раз», «заплатил за …», меньше притворства; при protect-стефане — стыд что «застали за…» |

**P0:** после missing **не** показывать policy-экран (в отличие от harass).

---

## 3. Axis A — Phase ladder (missing progress)

### 3.1 Состояния

```
soft_intro  →  soft_play  →  hard  →  free
```

| Phase | Смысл | Сколько «тиков» advance |
|-------|--------|-------------------------|
| **soft_intro** | 3 **hold-only** intro (A1→A2→A3) | SoftIntroStep 0..2 → Done |
| **soft_play** | N=**3** random soft ± break | SoftPlayCount ≥ SoftPlayNeed (default 3) |
| **hard** | first-show hard ladder | HardSub / HardStep |
| **free** | mix soft S3 + hard terminals + noble random | ladder advance **не** жёсткий |

**Вход** не обязан soft: `#HallMissingPhaseEnsure` **восстанавливает** phase из флагов (save/load).

Advance: `#HallMissingPhaseAdvance` на peek/ignore (noble promise **не** двигает soft/hard counters).

### 3.2 Soft intro (фиксированный порядок)

| Step | Promise (сёстры) | Promise Мелисса | PrivateAct |
|------|------------------|-----------------|------------|
| 0 | `look_tits` | `look_line` | look_tits |
| 1 | `hug_waist` | hug_waist | hug_waist |
| 2 | `touch_cock` | touch_cock | hand |

ForceHold = 1 (без break в intro, пока не Explicit).

После intro done (сёстры): **NobleUnlock tier 1** (s1).

### 3.3 Soft play

Random 33% look / hug / cock (Melissa look → look_line).  
После N=3 → phase **hard**, HardStep=0, HardSub=0.

### 3.4 Hard ladder — **Аманда / Мелисса**

HardStepMax = **5** (steps 0..4):

| HardStep | Slot | SubMax | Promise | Acts / finish (sub →) |
|----------|------|--------|---------|------------------------|
| 0 | **h0a** | 4 | piggy_look / **bud_smell** (M) | look → thigh → hug+break → **cuni** |
| 1 | **mouth** | 5 | mouth_hard | wipe → taste → spit → hold_spit → **swallow** |
| 2 | **h0b** | 2 | piggy_cuni / bud_cuni | cuni; sub>0 → anil flag + Explicit |
| 3 | **face** | **3** | facial | грудь → низ лица → **на лицо + FlagFaceDone** |
| 4 | **throat** | 5 | deepthroat | try → partial → full → cum_mouth → cum_throat |

После закрытия **mouth**: NobleUnlock **2**.  
После **throat** / ladder done: NobleUnlock **3**, FlagFaceDone=1, phase **free**.

**Mouth show:** finish `show_mouth` **не** выдаётся сёстрам (show = beat внутри swallow high; late/debug E).

### 3.5 Hard ladder — **Сандра** (кухня)

HardStepMax = **1** (один slot `mouth`, SubMax = **6**):

| Sub | Finish / act | Зрелость |
|-----|--------------|----------|
| 0 | cum_mouth (mid) | |
| 1 | swallow | |
| 2 | show_mouth | **MouthMature** (≥2) |
| 3 | cum_face | |
| 4 | deepthroat + cum_mouth | |
| 5 | deepthroat + cum_throat | |
| done | free; MouthMature=1 | **без DT+cough** |

Сандра: soft intro/play **те же** look/hug/cock (kitchen framing в prose); **noble нет**.

### 3.6 Free phase

- Soft style: random soft promises (S3 ton если Explicit)  
- Hard style: terminals mouth / facial / DT / cuni / (Sandra titjob)  
- Sandra free hard: bias по `$HallMissingClientPreferAct` (hand/mouth/facial tags)  
- Noble: 12% если `NobleInRandom` (после A6), screens=3  

---

## 4. Bargain style (soft vs hard promise band)

`#HallMissingBargainPickStyle`:

| Phase | Style |
|-------|--------|
| soft_intro / soft_play | **soft** band 1 |
| hard | **hard** band 3 |
| free + Explicit | 55% hard / 45% soft |
| free + not Explicit | 40% hard / 60% soft |

---

## 5. Диалоги **после** — карта

### 5.1 Сразу после missing-сцены

| Канал | Когда | soft | high | Explicit |
|-------|-------|------|------|----------|
| **Meet** `HallMissingMeet_*` | peek interrupt / meet Stefan | стыд, минимизация | смесь, торг тишины | цинизм / «уже было» |
| **Girl memory** | write after event | thin memory id | + lewd witness flags | + missing knowledge |
| **Daily aftermath** | утро | мысли «вчера в зале/подсобке» | тяжелее | скандал/acceptance |
| **Policy UI** | — | **не** после missing (P0) | — | — |
| **Rumor hint** (в следующем уговоре) | SoftPlayDone / FaceDone / HardStep≥1 / phase hard\|free | редко | чаще | да |
| **Offense answer** | GirlOffenseDays>0 | отказ по promise | отказ жёстче | отказ + «не трогай» |

### 5.2 После **harassment** (для связки)

| Канал | soft-мир (early) | mid | play / Explicit-era |
|-------|------------------|-----|---------------------|
| After talk band | злость protect/watch | «смотрел чтобы не обидели» | «сама / деньги / хороший дядька» (`HallHarassAfterBand` 0…3) |
| Policy | да, на after-экране | policy 1–3 | policy; >1 blocked until liberation |
| Talk reaction ids | protect_thanks / watch_hurt / ignore… | profit_low/high | play → hall_lewd memory hooks |
| Missing roll | **нет** (до play+гейтов) | — | watch/ignore + play → chance missing (v2 α) |

**Stance гейты (harass):**  
- play **только** `PlayCoached` + приятный клиент (CalculateStanceV2)  
- до coach: resist \| endure  
- liberation=0: no_protect off (только protect)  

---

## 6. Гейты «когда девушки как говорят» — сводная таблица

### 6.1 Missing: когда **можно** говорить/играть на уровне

| Уровень | Гейты (код / канон) | Как говорит |
|---------|---------------------|-------------|
| **Вообще missing** | liberation + Act1Moral + FamCorrupt≥3 (bargain start); **OnlyFromPlay**; coach | вход в уговор |
| **soft_intro** | phase / SoftIntroDone=0 | low initiative; hold |
| **soft_play** | SoftIntroDone | soft random; low/high by stage |
| **hard first-show** | SoftPlayDone | hard promises; mid language |
| **Explicit bargain** | FlagFaceDone (sisters) / MouthMature (Sandra) | прямой язык **всегда** (soft+hard) |
| **high initiative** | Explicit **или** GirlHallLewdStage≥3 **или** MissingGirlStage≥4; **не** в soft_intro | bolder prose |
| **Noble dig** | sisters; pending after A3/A4/A6 | отдельный multi-screen; offense dig |
| **Отказ offense** | GirlOffenseDays>0, not noble | только ответ, no scene |

### 6.2 Harass: когда как говорит

| Уровень | Гейты | Речь |
|---------|-------|------|
| T1–T3 intro | AllowedTier (stage∧slut∧u1) | intro text T×type |
| resist | default / low slut | «отстань», злость |
| endure | mid | терпит, стыд |
| play | PlayCoached + pleasant | подыгрывает → мост missing |
| after band 0–3 | FamilyCorruptionStage | личная злость на ГГ, не «зал осуждает» |
| policy talk | after harass | 1–3; >1 needs liberation |

---

## 7. Что **есть сейчас** в коде (инвентарь)

### 7.1 Wired и работает

| Компонент | Статус |
|-----------|--------|
| Phase machine soft_intro/play/hard/free | **да** `hall_missing_bargain.qsps` |
| Explicit flag Face/MouthMature | **да** |
| Initiative low/high pick | **да** |
| Soft intro A1–A3 order | **да** |
| Soft play N=3 | **да** |
| Sisters hard h0a→mouth→h0b→face→throat | **да** |
| Sandra mouth×6 no cough | **да** |
| Noble unlock 1/2/3 + pending | **да** (сёстры) |
| Promise → PrivateAct + finish | **да** ApplyPromiseToAct |
| Offense answer + rumor hooks | **да** hooks |
| Agent prose A/M/S soft/high/Explicit branches | **да** (~56–58 scene/meet locs each) |
| Pack weave v3 (hug high, hand, cuni, mouth A–E) | **частично вшит** (см. pack-map) |
| Harass stance + play→missing α | **да** harassment.qsps |
| Policy after harass / **not** after missing | **да** P0 |
| Visual stub+[VIS] harass/missing | **да** |
| Real webp hard missing | **нет** (defer moderation) |

### 7.2 Prose / act inventory (agent text)

Каждая девушка: **~56–58** `#HallMissingScene_*` / `#HallMissingMeet_*`  
В т.ч.: look_tits (+2/3 pages), hug (+2/3), hand (+2), thigh, cuni (+2/3), mouth wipe/taste/spit/hold_spit/swallow, facial/DT, anil, meet tails.

### 7.3 Известные дыры / backlog

| Тема | Статус |
|------|--------|
| under_table | **не** вшит |
| sister_kiss | Act2+, не missing v1 |
| mouth_show first-show sisters | **не** (E late/debug) |
| hand_melissa high polish | pack-map P1 backlog |
| hug high client flavor | P2 |
| anil / titjob full branches | partial |
| Harass intro refuse (resist→no missing) | backlog |
| Единый «диалог после Explicit» template для всех acts | **нет** — per-scene USER-OWNED |
| Soft/high/Explicit **гармонизация** всех meet-текстов | ongoing, owner prose |

### 7.4 Что **не** soft/high/Explicit

- **Harass types T1–T5** — поза/tier, не initiative  
- **GirlWorkPolicy 1–3** — правило работы, не тон missing  
- **FamilyCorruptionStage** — уклад; влияет band/tier, не прямая подпись soft/high  

---

## 8. Лестница одной картинкой (runtime)

```
[Harass] resist|endure|play ──play+coach+liber+stage──┐
                                                       ▼
[BargainStart] ── PhaseEnsure ── IsExplicit ── PickStyle ── PickPromise
                                                       │
        soft_intro: look → hug → cock (hold)            │
        soft_play:  random soft ×3                      │
        hard:       h0a → mouth → h0b → face* → throat  │  (*FlagFace → Explicit)
        sandra:     mouth sub 0..5 (mature@2)           │
        free:       soft S3 + terminals + noble%        │
                                                       ▼
        ApplyPromiseToAct → PrivateAct + Finish
                                                       ▼
        Scene soft|high|Explicit prose (agent text)
                                                       ▼
        Meet / memory / aftermath   |   NO policy (P0)
        PhaseAdvance on resolve
```

---

## 9. Краткие «долженствующие» диалоги после (чеклист для prose)

Использовать при дописке meet / talk-recall:

### Soft
- «Он почти ничего…» / «только смотрел»  
- Стыд перед Стефаном, просьба не рассказывать  
- Protect: благодарность + «в следующий раз раньше»  

### High  
- «Я… сама не сразу оттолкнула»  
- Злость + возбуждение; «не смотри так, будто…»  
- Мелисса: ирония; Аманда: смущение; Сандра: «не лезь в кухню с нравоучениями»  

### Explicit  
- Меньше оправданий: «заплатил», «как вчера»  
- Если застукали: злость «стучись» / кураж «уже поздно»  
- При offense: жёсткий отказ **в уговоре**, не meet  

---

## 10. Файлы для правок

| Задача | Файл |
|--------|------|
| Phase / Explicit / promise | `hall_missing_bargain.qsps` |
| Реплики уговора soft/hard Explicit | `hall_missing_bargain_text.qsps` |
| Сцены soft/high/Explicit | `hall_missing_agent_*_text.qsps` (**USER-OWNED**) |
| Meet tails | те же agent + `HallMissingMeetStefanTail` |
| Harass after talk | `hall_harassment_after_text.qsps` |
| Policy after harass | `girl_policy_*` |
| Pack status | `prose-hall-missing-pack-map.md` |

---

*Документ = канон-снимок для агентов и владельца. При расхождении prose vs code — править prose только с явного «можно тексты»; логику phase/Explicit — в bargain.qsps.*
