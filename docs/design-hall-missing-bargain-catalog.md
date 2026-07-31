# Каталог уговоров hall missing — обсуждение (продолжение)

**Дата:** 2026-07-30 (обновлено: **v0.8** soft lock + Soft-игра N)  
**Статус:** **утверждено:** якорь early soft = после hard-**лица**; Soft-игра **N=3**; вход soft не обязателен  
**Prose / wiring:** не трогаем

**Связанные файлы:**
- `modules/events/hall/hall_missing_bargain.qsps` — механика
- `modules/events/hall/hall_missing_bargain_text.qsps` — тексты уговора (USER-OWNED)
- `modules/events/hall/hall_missing_girl.qsps` / `hall_missing_girl_text.qsps`
- `modules/events/hall/hall_missing_agent_amanda|melissa|sandra_text.qsps`
- `docs/design-npc-voices.md` §1–3
- `docs/design-hall-scene-unified.md` §0.3a, 0.6

---

## Утверждённые решения владельца (рамка)

| # | Решение |
|---|---------|
| **1** | Структура **A**: `hall_missing_bargain_text` **girl-first** (`PrintAmanda` / `PrintMelissa` / `PrintSandra`) |
| **2** | **Все уговоры пересматриваем** (не «починить id», а заново набор) |
| **3** | Soft **break** = **+1 ступень** (`petting` / `tits_lick` / `pussy_touch` / `hand`…), **не** прыжок в `cuni` |
| **4** | Аманда: **compliance hold-сцены** нужны (позже prose) — вариант **4a** |
| **5** | **Noble** = редкий **client** + **свой promise** (вариант **5b**), не общий soft-пул |
| **6** | Сейчас: **таблицы на всех** → утверждение → потом wiring; **prose не трогаем** |
| **7** | **Missing = лесенка** (первый показ по порядку, потом random в открытом пуле) — см. §Лесенка |
| **8** | **Аманда A1–A3** — детальный канон; **A4–A6** hard mouth-лестницы; **A7 = noble** |
| **9** | Hard «копилка…» = **H0**; split **H0.a до A4** / **H0.b после A4.5** |
| **10** | A4 last sub **проглотила** = last first; post-ladder random = **терминалы** |
| **11** | A7 noble: **один** уговор soft\|high; prose multi-screen **есть** |
| **12** | **Seq β:** полный sub-круг слота, **потом** следующий слот |
| **13** | Post-ladder random: **только последние** сцены (A4.5, A5.3 LITE, A6.5, H0 last cuni) |
| **14** | **H0 cuni** = первая hard-линейка **до** A4, **рвём посередине**, хвост **после A4.5** |
| **15** | A5 = **LITE**; A7 wiring **ок** (N3) |
| **16** | Вход missing **не** обязан soft; soft = дорожка по фазе |
| **17** | Soft-игра насыщение **N=3** (после Soft-знакомства) → hard-лесенка |
| **18** | **Якорь** early soft OFF = после first hard-**лица** (A5 LITE done / first face) |
| **19** | Variant **A**: phase counters, без HallMissingSlut; H-pure на hard first |

---

## Лесенка missing — **канон v0.2 (владелец)**

Идея: first = **пройти лестницу целиком**; после — random **финальных** сцен, не всех промежуточных sub.

### Фазы (Аманда)

| Фаза | Условие | Что крутим |
|------|---------|------------|
| **S1 Hold-seq** | soft first | **A1 → A2 → A3**, **только hold** (без break) |
| **S2 Soft-rand** | S1 done; hard **ещё не** all-done | random A1–A3, **возможен break**; soft-high **S3 ещё нет** |
| **H-seq β** | hard-гейт (после S1 minimum — TBD) | H0.a → A4 → H0.b → A5 → A6; **low/high = тон**, не отмена seq |
| **S3 Soft-high-seq** | **только после hard-all-done** | A1h→A2h→A3h (или variants) — тексты **уровня last hard**, свои, не reuse terminal |
| **S4 General** | S3 done | random: soft early/break + soft-high + hard terminals + A7 |
| **A7 noble** | после S1+ / soft-circle | N3 |

### Жёсткий порядок hard first (β + H0 split) — **утверждено**

```
soft-circle + hard gate
    → H0.a  (копилка, first half cuni-track, full sub)
    → A4    (A4.1 … A4.5 swallow, full β)
    → H0.b  (cuni second half … H0.last)
    → A5    (LITE A5.1 … A5.3)
    → A6    (A6.1 … A6.5 throat cum)
    → H-term-rand: { A4.5, A5.3, A6.5, H0.last }
A7 noble: after soft-circle, N3 (not inside H-seq)
```

### Разрез H0.a / H0.b (предложение — подтвердить)

| sub | Half | Содержание |
|-----|------|------------|
| H0.a.1 | a | смотрят, хвалят (копилка / раковина / мамина) |
| H0.a.2 | a | трогают, пошло |
| H0.a.3 | a | просто **cuni** |
| H0.a.4 | a | cuni + **пальцы** ← конец first half |
| | | *— A4.1…A4.5 —* |
| H0.b.1 | b | + **anilingus** |
| H0.b.2 | b | + **пальцы в попе** = **H0.last** (term-rand) |

### Флаги (черновик)

```
HallMissingSoftCircleDone['amanda']
HallMissingHardGate['amanda']
HallMissingForceStep['amanda']   ! e.g. H0a.3 / A4.2 / H0b.1 / A5.1 / A6.4
HallMissingHardAllDone['amanda'] ! → term-rand
HallMissingSubSeen['amanda']['A4'][1..5]  ! etc.
```

---

## Аманда — канон v0.2 (уговор + missing)

### Обзор слотов

| id | Тип | Тема | First | Post |
|----|-----|------|-------|------|
| **A1–A3** | soft | грудь / обнять / хуй | S-seq | S-rand |
| **H0.a** | hard cuni | копилка early | **до** A4 | — |
| **A4** | hard mouth | → **A4.5 swallow** | full β | term **A4.5** |
| **H0.b** | hard cuni | → **H0.last** | **после** A4.5 | term **H0.last** |
| **A5** | hard facial | **LITE** → **A5.3** | full β | term **A5.3** |
| **A6** | hard DT | → **A6.5** | full β | term **A6.5** |
| **A7** | noble | 1 уговор soft\|high | soft-circle+ | N3 |

---

### A1 — посмотреть на грудь

**Уговор (клиент):** просит **показать** грудь.

| | Soft (low) | Hard / high-тон |
|--|------------|-----------------|
| **Аманда** | смущение: «они маленькие, что там смотреть» | «любишь, когда маленькие?» |
| **Клиент** | уговаривает: не маленькие — **аккуратненькие**, как у **первой любви** | подтверждает: да, как у его любви |

**Missing**

| Режим | Содержание |
|-------|------------|
| **Hold (договор)** | клиент **смотрит**; может просить большего словами |
| **High (разрешено)** | позволяет **потрогать**: мнёт грудь, крутит соски |
| **Break (нарушение)** | мнёт **и лижет** (`tits_lick`) |
| **Early escalate cuni** | **НЕТ** — cuni только H0 / post-hard soft (см. ниже) |

**Act map (ранний soft / S-rand до hard-all)**

| outcome | act / scene key |
|---------|-----------------|
| hold | `look_tits` |
| high hold+ | tits touch / соски |
| break | `tits_lick` |

---

### A2 — обнять, поцеловать, вдохнуть запах

**Уговор (клиент):** красивая; ему в радость **просто обнимашек**.

| | Soft | Hard |
|--|------|------|
| **Аманда** | смущение: «правда просто обниму — и тебе будет легче?» | «идём, обниму, дам **подержаться за попу**» |

**Missing**

| Режим | Содержание |
|-------|------------|
| **Hold soft** | простые **обнимашки** (+ лёгкий поцелуй/запах по тексту) |
| **Hold hard** | рука **на попе** |
| **Break** | **petting** |
| **Hard-tone + high (ещё до hard-all)** | рука на попе / petting / пальцы+оргазм — **в рамках soft-лестницы A2**, не cuni |
| **Post-hard soft escalate** | см. §Post-hard soft (мета «обниматься или делом?») |

**Act map (ранний soft)**

| outcome | act |
|---------|-----|
| hold soft | `hug_waist` |
| hold hard-tone | `hug_ass` |
| break | `petting` |
| high early | `pussy_touch` (+ orgasm) — **опционально**, не cuni |

---

### A3 — потрогать хуй

**Уговор (клиент):** комплименты; **тесно в штанах**; только такие **славные ручки** снимут дискомфорт.

| | Soft | Hard |
|--|------|------|
| **Аманда** | красная, стыдно: «не знаю… не умею» (+ клиент ещё уговаривает) | «знаю я тебя: наедине сразу **член в руки** вывалишь и спросишь, красивый ли» → клиент **отрицает** (отмазка) |

**Missing**

| Режим | Содержание |
|-------|------------|
| **Hold / договор** | выполнение: сквозь ткань / в руки по уговору |
| **High** | **голый** член, подрачивание, мнёт яйца, **без** окончания *или* см. ниже |
| **Break** | full **handjob** |
| **Finish soft** | окончание **на пол** |
| **Finish high** | окончание **на руки** + **облизывание** |

**Act map**

| outcome | act |
|---------|-----|
| hold soft | `cock_touch_cloth` |
| hold/high | `cock_touch` / hand no cum |
| break / finish | `hand` (+ cum floor / hands+lick variants) |

---

### Soft phases v0.4 — лесенка soft (владелец передумал «low = вечный контраст»)

**Отказ:** low post-hard = всегда только честные обнимашки как вечный контраст.  
**Вместо:** soft = **своя лесенка фаз**, как hard β, потом общий random.

#### Фазы soft + hard (v0.5 — S3 **после** hard)

**Почему S3 не раньше hard:**  
тексты S3 («обниматься или делом?», смелый post) **по тону = last hard**.  
Если S3 до H0/A4–A6 — **ломают** first-time hard (спойлер интенсивности).  
Если S3 «смягчить» под early — **не** совпадут с hard-линейкой.  
→ **S3 only after hard-all-done.**

```
S1  A1→A2→A3 hold only
        ↓
S2  random soft + break     (пока hard не завершён; S3 закрыт)
        ↓
H   H0.a → A4 → H0.b → A5 → A6   (β full; low/high = тон реплик)
        ↓
S3  soft-high first seq     (свои тексты уровня last hard, НЕ gt terminal)
        ↓
S4  general random
```

#### S1 — первые 3 без нарушений

| # | Slot | Уговор | Missing **только hold** |
|---|------|--------|-------------------------|
| 1 | A1 | посмотреть | клиент **только смотрит** (не мнёт, не лижет) |
| 2 | A2 | обнять | **только** обнимашки / лёгкий поцелуй-запах (не попа hard, не petting break) |
| 3 | A3 | потрогать | **сквозь ткань** / робко, **без** full handjob / cum |

Игрок (и текст) видит: «договорились — сдержали».

#### S2 — random + break, до high-флагов

| Slot | Hold (ещё) | Break (возможно) |
|------|------------|------------------|
| A1 | смотрит | мнёт / **лижет** |
| A2 | hug / рука на талии | petting; (ещё не full high-meta) |
| A3 | cloth / short touch | handjob; cum floor? |

**High-флаги (что открывает S3)** — TBD:  
`GirlHallLewdStage` / `sluttiness` / `PrivateCount` / `HallMissingSoftBreakCount>=N` / initiative rolls.

#### S3 — «вся лестница, high» — **два толкования, выбрать**

| | **S3-A: слоты high-seq** | **S3-B: intensity-seq на слот** |
|--|--------------------------|--------------------------------|
| Что first | A1 **high-text** → A2 high → A3 high (3 missing) | Для A1: break-max → high-post; потом A2… |
| Смысл | «показать high-версию каждого soft-уговора» | «добить интенсивность внутри темы» |
| Объём | 3 сцены | 3×(1–2) длиннее |
| Мета | «обниматься или делом?» на каждом | то же |

**Рекомендация к обсуждению: S3-A** (проще, 3 first high), high-текст **свой** (не H0).

Содержание high-текстов (черновик, свои prose):

| Slot | High missing (свой, не terminal hard) |
|------|----------------------------------------|
| A1h | сама ведёт look→touch→lick; смелее |
| A2h | мета «обниматься или делом?» → petting / пальцы / **свой** cuni-text optional |
| A3h | сразу голый hand, cum hands+лиз; без A4.5 |

#### S4 — общий random

После S3 (+ когда hard-all done — hard terminals в pool):

| Пул | вес (черновик) |
|-----|----------------|
| Soft any open (hold/break/high variants) | ~25% |
| Hard terminals | ~65% |
| A7 | ~10% |

**Не** вечный «только low soft». Low/hold исходы могут выпасть roll’ом, но не как отдельная «фаза контраста».

#### Soft S3 ≠ прыжок в hard-сцену

S3 = soft-слот + **новый** lewd-текст «после hard».  
**Не** `gt` H0.last / A4.5 / A6.5 (reuse). Разнообразие.

#### Робкая (low) на hard — **ломает линейку?** (обсуждение v0.5)

Владелец: *по текстам возможен переход на hard ещё робкой Аманды; S3 только после hard.*

**Линейка first-show** = порядок **слотов/sub**, не «только high-персона».

| Слой | Low на hard | Ломает seq? |
|------|-------------|-------------|
| **Порядок** H0.a→A4→…→A6 | low проходит **те же** first sub | **Нет** — β цела |
| **Тон** | «ой… только пол шишечки…» / платок / стыд (уже в deepthroat/facial prose) | **Нет** — initiative ветка |
| **S3 до hard** | если low/high S3 early | **Да** — спойлер last-hard тона → **запрет**, S3 after hard |
| **S3 = hard scene** | soft-high = copy terminal | **Да** по разнообразию → **свои** тексты |
| **Hard только high** | low никогда не видит H0/A4 | **Не ломает**, но **режет** контент; ты сказал тексты **допускают** low hard |

**Вывод:**  
робкая на hard **не ломает** лесенку, если:
1. hard-гейт = **stats/phase** (S1/S2 done + slut/stage), **не** «только high initiative»;  
2. low/high = **какой абзац** внутри sub, не «пропуск A4.3»;  
3. S3 **строго после** hard-all;  
4. S2 soft break **не** выдаёт A4.5/DT-level prose.

**Риск (мягкий, не seq-break):**  
игроку low-DT может казаться жёстче «характера» — но у вас канон: *стесняется постыдного, не «не делает»*; клиент дожимает. Тексты low hard это уже держат.

**S3 и low после hard:**  
после hard-all даже «робкая» в S3 может flip high **в этой** сцене (мета «делом») **или** S3 требует high-флаг отдельно — TBD.  
Но **открытие** S3 = hard-all, не «сначала high потом hard».

#### Флаги (черновик)

```
HallMissingSoftPhase['amanda'] = 1..4   ! S1..S4
HallMissingSoftHoldSeq['amanda'] = 0..3 ! 0=need A1 hold, 3=S1 done
HallMissingSoftHighSeq['amanda'] = 0..3 ! S3 progress
HallMissingSoftHighGate['amanda'] = 0/1
PromiseBreak forced 0 in S1
```

#### Глоссарий v0.7 (не путать буквы)

| Говорим | Было в чате | Смысл |
|---------|-------------|--------|
| soft **грудь / обнять / рука** | A1 A2 A3 | темы **мягкого** уговора |
| hard **копилка / рот / лицо / горло** | H0 A4 A5 A6 | темы **жёсткой** лесенки |
| **нобиль** | A7 | дворянин |
| **Soft-знакомство** | S1 | 3 first hold без break |
| **Soft-игра** | S2 | random soft + break |
| **Hard-лесенка** | H-seq | first hard по порядку |
| **Soft-после-hard** | S3 | soft-темы, смелые тексты после hard |
| **Общий random** | S4 | всё открытое |
| **soft / hard** | bargain style | мало vs прямо в уговоре |
| **low / high** | initiative | робкая vs смелая **в тексте** |
| **фаза** | S1… | прогресс лесенки девушки |
| **вход missing** | event start | одно событие; ≠ «всегда soft» |

---

#### Вход ≠ soft обязателен (v0.7)

Владелец: *не требую входа на soft; вход может быть и на high.*

Каждый missing смотрит **текущую фазу** девушки:

| Фаза сейчас | Что выдаём |
|-------------|------------|
| Soft-знакомство не done | следующий hold (грудь→обнять→рука) |
| Soft-игра | random soft ± break |
| Hard-лесенка не done | следующий hard-шаг |
| Soft-после-hard / random | high-track |

Если в игру / stats уже «далеко» — можно **сразу** hard или high, **минуя** soft (или soft уже закрыт).  
Soft — **дорожка**, не обязательный тамбур.

---

#### Если всё же идём по soft — до каких пор soft живёт?

```
SOFT EARLY открыт
  │  Soft-знакомство: 3× без break
  │  Soft-игра: random + break, пока «насытили»
  ▼
( soft early ещё может быть, пока не якорь закрытия )
  ▼
ЯКОРЬ: после first hard-**лица**  (утверждено)
  ▼
SOFT EARLY мёртв
  │  нет «только посмотреть / честный hug»
  ▼
HIGH track: Soft-после-hard + hard last + горло/… + нобиль
```

| | |
|--|--|
| Soft early | знакомство (3 hold) → игра (**3** random) → hard до **лица** |
| После лица | early soft **OFF**; Soft-после-hard = другие тексты |
| Вход не soft | soft-дорожку можно не проходить |

**Variant A:** phase counters, без отдельной «шлюховатости».  
**H-pure:** пока Hard-лесенка first — только hard-шаг (soft random не мешает).

**Якорь early soft OFF — утверждено v0.8:** после first hard-**лица**  
( Soft-знакомство + Soft-игра + hard до лица включительно; early soft в pool больше нет ).

После якоря: Soft-после-hard (смелые тексты) + продолжение hard (горло…) + last/нобиль — **не** early hold/break.

---

#### Soft-игра «насытили» → hard — утверждено v0.8

| | |
|--|--|
| Правило | Soft-знакомство done + **ровно 3** missing Soft-игры (random soft ± break) |
| Flag | `HallMissingSoftPlayCount['girl'] >= 3` → soft-sat → Hard-лесенка |
| Hard | от **этого flag** (+ старые gейты FamCorrupt/play), не от initiative high |

**Минимум missing на full soft early (если шли soft с нуля):**  
3 (знакомство) + 3 (игра) = **6**, затем hard (копилка→…→лицо→ якорь → …).

**S3:** всегда 3 first после hard-all, **независимо** от low/high *во время* hard.  
S3-тексты = «уже после hard» (смелые); low-проза S3 **не** нужна или редкий rollback.

**Low gate «дальше не пройдёт»:**  
не «low не видит hard», а **phase**: без S2-flag **нет** H и **нет** S3.  
Tone low/high **внутри** phase — отдельно.

---

#### Сейчас в коде: когда High? Успеет ли игрок увидеть low?

**Initiative high** (`HallMissingBargainPickPromise`):

```
high if ANY:
  GirlHallLewdStage >= 3
  OR sluttiness >= 30
  OR GirlNpcPath >= 26
  OR HallMissingGirlStage >= 4
```

**Вход в missing** (сёстры): `sluttiness >= 35` **или** `GirlNpcPath >= 28` **или** policy3+agr≥2  
(+ FamCorrupt≥3, Liberation, stage≥3, play path…)

**Аманда старт:** `sluttiness['amanda'] = 0` (`amanda.qsps`).

| Проблема | Суть |
|----------|------|
| **Порог high (30) < вход missing (35)** | как только missing **легален** по slut — initiative **уже high** почти всегда |
| NpcPath≥26 | high; missing path +2 per peek → **быстро** 26 |
| Stage≥4 score | scandal/fame/slut/policy — mid-late Act1 **часто** stage 4 → high |
| PrivateCount≥1 | после **1** peek → bargain band mid, 40% hard style |
| Missing rare | play→15–25% missing — **мало** событий, но **тон** high с первого |

**Ответ на «свалится ли сразу в high»:**  
**По тону реплик — да, риск очень высокий** с текущими числами: first missing при slut≥35 ⇒ high.  
**По фазам S1/S2/H** — ещё **нет** в коде (лесенки phase нет); сейчас random promise soft/hard.

**Успеет увидеть low soft hold?**  
При **текущем** initiative: **почти нет**, если missing открыт через slut≥35.  
Окно low: только path NpcPath 28+ при slut&lt;30 (редко) или debug.

**Harass** даёт slut +1 кусками — до missing 35 игрок видит **зал** low/mid, но **missing** already high-tone.

---

#### Что делать, чтобы не «свалилась»

1. **Phase-first (лесенка):** S1–S2–H–S3 = счётчики first-show, **не** initiative.  
2. **Initiative в missing пересчитать:**  
   - S1–S2: force **low** (или high только после K breaks / SoftHighSeen)  
   - H-seq: low/high по **отдельной** шкале или roll, не slut≥30  
   - S3+: force high-prose / allow high  
3. **Поднять** missing-high порог (slut≥45 / LewdStage≥3 only) **или**  
4. **Опустить** не надо entry 35 без phase — иначе first three holds с high-репликами «я сама» диссонанс.

**Рекомендация:**  
- Soft-игра sat = **N=3** (v0.8)  
- hard после soft-sat  
- early soft OFF после first hard-**лица**  
- Soft-после-hard / high pool после якоря  
- `$HallMissingInitiative` в Soft-знакомство = force low; не slut≥30  

Игрок на soft-дорожке: 3 hold + 3 soft-игры, затем hard до лица, потом early soft закрыт.

---

### H0 — hard уговор «укромный уголок / копилка» (один promise, голоса клиента)

**Один** hard-уговор: «покажешь укромный уголок / поможешь с проблемой / тихая гавань…».

| Client type | Метафора / голос |
|-------------|------------------|
| generic / young | такая молодая и красивая… хочу **посмотреть** |
| **merchant** | очень красивая **копилка**, хочу посмотреть |
| **traveler / sailor** | **раковина**; «тихая гавань, где русалка поможет уставшему моряку» |
| **craftsman / local** | сильно ли **отличается от маминой** |

Ответы Аманды: **soft vs high** (смущение / азарт).

**Missing**

| Режим | Содержание |
|-------|------------|
| Hold soft | **смотрят**, **хвалят** |
| Hold hard | **трогают**, **пошлые** комментарии |
| Break soft | **просто cuni** |
| Break hard ladder | cuni → +пальцы внутри → +anilingus → +пальцы в попе |

**Открыто:** на каком этапе hard-ladder включать каждую ступень (PrivateCount / slut / stage / first H0 seen).

---

### A4 — отсос (sub-лестница) — канон владельца

**Уговор hard (общий mouth):** губками / «помоги ротиком» — один promise `mouth` / `mouth_spit`→эволюционирует в sub.

**Правило sub-лестницы (как сказал владелец):**
1. **Первый круг** внутри A4: показывать sub **по порядку** A4.1 → … → A4.5  
2. **A4.5 проглотила** = **последний** first-show  
3. После того как **весь** A4-круг пройден → при выпадении слота A4 **random** среди A4.1–A4.5 (включая swallow)

| sub | Содержание | Близкий prose key (уже есть / partial) |
|-----|------------|----------------------------------------|
| **A4.1** | отсос, закрыла **рукой** (вытерла) | mid_spit / hand wipe flavor |
| **A4.2** | отсос, рукой + **попробовала** (вкус) | late_tongue partial |
| **A4.3** | окончание **в рот**, **выплюнула** | `mouth_amanda_mid_spit` / late_show_spit |
| **A4.4** | в рот, **подержала**, выплюнула | late_show / tongue hold spit |
| **A4.5** | **проглотила** ← last first, потом в random | `mouth_amanda_late_tongue_swallow` |

**Флаги (черновик):** `HallMissingSubSeen['amanda']['A4'][1..5]`, `HallMissingSubCircleDone['amanda']['A4']`.

---

### A5 — facial **LITE** — утверждено

**Уже есть prose-база:** `#HallMissingUserScene_mouth_amanda_late_facial`.

| sub | Содержание | Post |
|-----|------------|------|
| **A5.1** | жмурится, вытирает платком | first only |
| **A5.2** | терпит, не вытирает сразу | first only |
| **A5.3** | подставляет / слизывает / взгляд в щель (high-show) | **term-rand** |

Full β: A5.1→A5.2→A5.3, затем в term-rand только **A5.3**.

---

### A6 — глубокое горло (sub-лестница) — канон владельца

| sub | Содержание |
|-----|------------|
| **A6.1** | попытка **глубже** → **кашель, слёзы** (не до конца) |
| **A6.2** | проходит **чуть-чуть** глубже; всё ещё кашель/слёзы |
| **A6.3** | **залез до конца** |
| **A6.4** | до конца + окончание **в рот** |
| **A6.5** | до конца + окончание **в горло** (stomach) |

Правило то же: **seq first** .1→.5, затем **random** всех A6 sub.

**Prose:** `#HallMissingUserScene_deepthroat_amanda` уже **поздний** (часто сразу deep + cum throat) + soft/high + client.  
Wiring later: **разбить** на sub-параграфы / `$HallMissingMouthSub` ветки **или** отдельные keys `deepthroat_amanda_try` … `deepthroat_amanda_throat_cum` — **prose later**, сейчас только map.

| sub | act / key (черновик) |
|-----|----------------------|
| A6.1 | `deepthroat_try` |
| A6.2 | `deepthroat_partial` |
| A6.3 | `deepthroat_full` (no cum / hold) |
| A6.4 | `deepthroat` + cum_mouth |
| A6.5 | `deepthroat` + cum_throat (= current climax beat) |

---

### A7 — нобиль (один уговор soft|high)

**Не** в цепочке A4→A5→A6.  
**После** soft-circle A1–A3; участвует в **общем random** (и/или только если `$HallMissingClient = 'noble'` / rare force noble client).

#### Уже есть в файлах

| Location | Содержание |
|----------|------------|
| `#HallMissingUserScene_noble_amanda` | уговор в зале: алтарь / укромный уголок; soft\|high ответ; **без оплаты**; act → s1 |
| `_s1` | поцелуй + hand (high сама достаёт) |
| `_s2` | на колени, рот (high deep / soft старательно) |
| `_s3` | finish random/forced: **mouth** / **face** / **anilingus+cum hair** |
| `#HallMissingUserMeet_noble_amanda` | aftertalk: «женился бы» / злость Стефана / finish flavor |

То есть **уговор + 3 экрана peek + meet** уже написаны. Задача — **встроить в лесенку/dispatch**, не переписывать с нуля.

#### Как сделать (варианты wiring — обсудить)

| | **N1 Force client** | **N2 Slot in pool** | **N3 Hybrid (рекомендация)** |
|--|---------------------|---------------------|------------------------------|
| **Pick** | rare roll client=`noble` → promise A7 only | после soft-circle A7 в random slots; client → noble | soft-circle done → A7 может выпасть в ALL-rand **или** client noble → always A7 |
| **Bargain screen** | можно **скип** отдельный bargain: noble scene **сама** = уговор+уход | тонкий bargain 1 экран = реюз intro noble | **скип** `HallMissingBargain*` → `gt` noble_amanda (уговор внутри) |
| **Peek UI** | missing-меню interrupt/peek/ignore **или** сразу «смотреть в щель» как сейчас | унифицировать с A1–A6 peek | first: оставить **3 act** noble; later unify |
| **Finish** | keep rand 1/3 mouth/face/anilingus | soft→ mouth\|face only; high→ +anilingus | soft: mouth/face; high: all 3; **не** anilingus на первом A7 |
| **Повтор** | после first A7 — random finish; scene same | sub? не нужно | one slot, finish ladder optional |

**Soft vs high (уже в prose):**
- soft: румянец, «правда к алтарю?», робкий hand/mouth, платок после  
- high: сияет, сама в подсобку, deep, подмигивает Стефану, «сестра дворянина»

**Стык с A4–A6:** noble **не** требует A4 first; только soft-circle. Опционально: A7 weight выше после hard-circle (Familiar).

**Оплата:** канон noble — **0 серебра** (конфликт сословный) — не ломать.

---

### Свод hard (Аманда) v0.2 — утверждено

```
S-seq A1→A2→A3 → S-rand
hard gate → H0.a → A4(1…5) → H0.b → A5(1…3 LITE) → A6(1…5)
         → term-rand {A4.5, A5.3, A6.5, H0.last}
A7 noble after soft-circle (N3)
```

---

## Как устроено сейчас (кратко)

```
play на виду
  → HallMissingBargainStart
       style: soft | hard
       promise: id (уже частично по девушке в PickPromise)
  → HallMissingGirlStartFromPlay
       ApplyPromiseToAct → $HallMissingPrivateAct + PromiseBreak
  → peek → $HallMissingSceneKey → hall_missing_agent_<girl>_text
```

**Проблемы текущего текста/map:**
1. Клиентские реплики общие, promise — личные; чужие promise склеены (`show_stockings`≈`smell`, `whisper_poem`≈ rest).
2. Reply-ключи ≠ id promise (`smell`, `rest`, `petting` vs roll ids).
3. Soft break часто → `cuni` (против решения 3a).
4. PromiseBreakTail устарел (look_tits / smell / touch_cock).
5. Noble торчит в soft-bargain, в PickPromise не крутится; текст noble про Аманду.
6. Compliance Аманды (hold) — dispatch есть, prose почти нет.

---

## Общие правила (предложение канона каталога)

### Слои

```
play на виду
  → BARGAIN (soft | hard)     ← «что обещали»
  → MISSING peek               ← hold act ИЛИ break act
  → meet / thought
```

### Soft vs hard

| | Soft | Hard |
|--|------|------|
| **Слова клиента** | «только…», мало, в тень | рот / рука до конца / cuni / titjob — прямо |
| **Hold act** | compliance (слово держали) | обычно **то же**, что обещали (договор = mid-сцена) |
| **Break** | ~55–70% → **+1** по лестнице | опционально silver_extra / «взял больше» (~30–50%), **не** новый act-класс |
| **Band** | early / early→mid | mid / late |

### Лестница act (soft break не перепрыгивает)

| Ступень | Act | Смысл |
|--------:|-----|--------|
| 0 | `look_tits`, `hug_waist`, `cock_touch_cloth`, `touch_thigh`, `show_hint`… | hold soft |
| 1 | `tits_lick`, `petting`, `hand`, `pussy_touch` | soft **break** |
| 2 | `mouth`, `cuni`, `titjob` | **hard** promise / mid band |
| 3 | `mouth_balls`, `deepthroat`, `anilingus`… | late band (часто **без** отдельного soft-уговора; late roll или hard+stage) |

Hard `cuni` / `mouth_*` — ступень 2, **не** soft-break.

### Клиенты и noble (5b)

| Client | Play/missing | В уговоре |
|--------|--------------|-----------|
| drunk | **нет** | — |
| merchant / craftsman / traveler | да (по pleasant) | обычный soft/hard pool |
| **noble** | редко | **отдельный** promise-пул, не в общем soft 1/3 |

Noble: отдельный gate (client already noble **или** rare roll при stage+), свои 1–2 promise на девушку.

### Структура текста (A, позже, без prose сейчас)

```
#HallMissingBargainPrintText
  → intro (общий «слышу уговор»)
  → gs PrintAmanda | PrintMelissa | PrintSandra
       soft → по $HallMissingPromise (клиент + ответ)
       hard → по $HallMissingPromise
```

Один **promise id** = одна строка каталога = клиент + девушка + hold + break + scene keys.

---

## Что из текущего набора выбрасываем / не тащим

| Старое | Проблема | Решение в новом каталоге |
|--------|----------|---------------------------|
| `smell` как reply-ключ | нет в roll, путаница | убрать id |
| `whisper_poem` → cuni | семантика и break | **переделать** (Мелисса soft) |
| `show_stockings` + client smell | склеены чужие смыслы | заново |
| soft → break `cuni` | против 3a | break max ступень 1 |
| noble внутри soft generic | дыра + «Аманда» в клиенте | **5b** отдельный пул |
| `kitchen_backroom_rest` ≈ rest generic | пустой контракт | заменить на **кухонный** soft |
| Много `*_spit/*_price/*_quick` | id разные, act один | схлопнуть hard id **или** flavor-id → один act |

---

## Черновой каталог v0 (для обсуждения)

Ниже — **предложение**, не код. % — ориентир.  
**Сцена status:** что есть в agent/dispatch **сейчас** (prose не пишем).

**Легенда status:** есть · dispatch · нет · USER · hold / break

---

# Аманда

**Тон soft:** смущение + любопытство, «только…», блеск комплиментов, передок ломает.  
**Тон hard:** стыд + азарт, «губками», «пока Стефан…».  
**Место:** зал → storage / stairs / under_table.

### Soft (обычный client)

| # | promise id | Уговор (смысл) | hold act | break % | break act | scene hold | scene break | status hold | status break |
|---|------------|----------------|----------|---------|-----------|------------|-------------|-------------|--------------|
| A1 | `look_tits` | «только гляну на грудь / шнуровку» | `look_tits` | 70 | `tits_lick` | `look_tits_amanda` | `tits_lick_amanda` | dispatch/нет prose | dispatch |
| A2 | `hug_kiss` *(бывш. hug_waist)* | «обнять / один поцелуй в шею-щёку» | `hug_waist` | 65 | `petting` | `hug_waist_amanda` | `petting_amanda` | dispatch/нет | USER есть |
| A3 | `touch_cock` | «ладошкой сквозь сукно» | `cock_touch_cloth` | 70 | `hand` | `cock_touch_cloth_amanda` | `hand_amanda` | нет/dispatch | USER есть |

**Вопрос A-soft:** три слота ок? Или вместо `hug_kiss` — «похвали / погладь по щеке» (слабее тело, сильнее передок словами)?

### Hard (обычный)

| # | promise id | Уговор | hold=act | break? | scene | status |
|---|------------|--------|----------|--------|-------|--------|
| A4 | `mouth_spit` | губы, **не** глотать / выплюнуть | `mouth` | silver_extra / mid→late flavor | mid spit / late spit | USER mid/late |
| A5 | `mouth_swallow` | губы + **проглот** | `mouth` | late band flavor | late swallow / tongue | USER |
| A6 | `hand_finish` | рукой до конца | `hand` | без прыжка в другой класс | `hand_amanda` | USER |

**Вопрос A-hard:** cuni у Аманды в hard pool?
- Сейчас в roll hard cuni у Аманды нет (cuni есть в mid band random).
- **Предложение:** hard Аманды = **рот + рука**; cuni только late random / initiative — **или** редкий A7 `cuni_ask`.

### Noble (client = noble, редко)

| # | promise id | Уговор | hold | break | notes |
|---|------------|--------|------|-------|-------|
| AN1 | `noble_flatter` soft | «укромный угол, полюбоваться / алтарь-лесть» | `hug_waist` / `look_tits` | `petting` | fantasy статуса |
| AN2 | `noble_mouth` hard | «по-благородному» → губы | `mouth` | late flavor | multi-step noble scene — задел |

**Вопрос noble-A:** один soft + один hard или только soft noble + hard из общего?

---

# Мелисса

**Тон soft:** «предсказуемо», цена → бумага/стихи, границы словами, не «злая шлюха».  
**Тон hard:** торг с усмешкой, «ритм», cuni = она **оценивает** его старание.  
**Место:** зал → storage.

### Soft — полный пересмотр (текущие id не святы)

**Было:** `show_stockings` / `touch_thigh` / `whisper_poem` (break→cuni).  
**Предлагаю v0 три контракта:**

| # | promise id | Уговор (смысл) | hold act | break % | break act | scene hold | scene break | status |
|---|------------|----------------|----------|---------|-----------|------------|-------------|--------|
| M1 | `look_line` *(или look_tits)* | «посмотри на линию / вырез — руки **при себе**» | `look_tits` | 60 | `tits_lick` | `look_tits_melissa` | `tits_lick_melissa` | hold+break есть |
| M2 | `touch_thigh` | «ладонь **снаружи**, минута» | `touch_thigh` | 65 | `pussy_touch` | `touch_thigh_melissa` | `pussy_touch_melissa` | hold нет; break есть |
| M3 | `poem_corner` | «в тишине — **стих / комплимент по уму**, не лапать» | `hug_waist` *или* `tease` | 55 | `petting` | `hug_waist_melissa` / новый | `petting_melissa` | hug есть; petting USER |

**Альтернатива M3b:** `coin_paper` — «серебро на бумагу, постою в закутке» hold=`hug_waist`, break=`petting`.

**Выкинуть из soft:** break в `cuni`; smell-generic; `whisper_poem` если hold неясен.

**Вопрос M-soft:**
1. Нужны ли **чулки** (`show_stockings`) отдельным id?
2. M3 = **стихи** или **чистый торг** «на издание»?
3. Soft **без** рта и **без** руки до конца — ок?

### Hard

| # | promise id | Уговор | act | notes | status |
|---|------------|--------|-----|-------|--------|
| M4 | `mouth_price` | губы «как плата за бумагу» | `mouth` | mid spit / late throat | USER mouth |
| M5 | `hand_strict` | рука, она **задаёт** темп/границы | `hand` | | USER hand |
| M6 | `cuni_grade` | «припади — посмотрим, лучше ли поэтов» | `cuni` | **только hard** | USER cuni |

**Вопрос M-hard:** swallow отдельно или один `mouth` + band/roll flavor?

### Noble (редко)

| # | promise id | Уговор | hold | break |
|---|------------|--------|------|-------|
| MN1 | `noble_verse` soft | «цените поэзию? в подсобке — стих / взгляд» | `hug_waist` / look | `petting` |
| MN2 | `noble_favor` hard | «милость губ за покровительство слогу» | `mouth` | — |

---

# Сандра

**Тон soft:** кухня, коротко, «пока рагу», без cuni.  
**Тон hard:** прагматика, губы/грудь/рука, кладовая.  
**Место:** **только kitchen**.

### Soft

| # | promise id | Уговор | hold | break % | break | scene hold | scene break | status |
|---|------------|--------|------|---------|-------|------------|-------------|--------|
| S1 | `kitchen_waist` | «обнять у печи / за талию» | `hug_waist` | 60 | `petting` | `hug_waist_sandra` | `petting_sandra` | hold есть; petting USER |
| S2 | `heavy_breast` | «обхвати / подержать грудь» | `look_tits` | 65 | `tits_lick` | `look_tits_sandra` | `tits_lick_sandra` | есть |
| S3 | `kitchen_hand_hint` *(нов.)* | «ладонью сквозь фартук / сукно — и к плите» | `cock_touch_cloth` | 65 | `hand` | `cock_touch_cloth_sandra` | `hand_sandra` | cloth есть; hand USER |

**Вместо** `kitchen_backroom_rest` — **S3** с телом.

**Вопрос S-soft:** rest оставить как soft hold 100% без break? Или три телесных S1–S3.

### Hard

| # | promise id | Уговор | act | status |
|---|------------|--------|-----|--------|
| S4 | `titjob` | грудью | `titjob` | USER merchant/traveler |
| S5 | `hand_pragmatic` | рукой — и назад | `hand` | USER |
| S6 | `swallow_trade` | губы + сделка/глоток | `mouth` | USER mid/late |

**Канон:** hard **без cuni**.

### Noble

| # | | |
|---|--|---|
| SN | **Редко / off** | Дворянин на кухне слабо; **предложение:** noble **не** для Сандры **или** 1 rare soft |

---

## Сводная матрица soft (v0)

| Ступень 0 hold | Аманда | Мелисса | Сандра |
|----------------|--------|--------|--------|
| смотреть грудь | A1 `look_tits` | M1 `look_line` | S2 `heavy_breast`→hold look |
| талия / объятие | A2 `hug_kiss` | M3 `poem_corner`→hug | S1 `kitchen_waist` |
| пах сквозь ткань | A3 `touch_cock` | — | S3 `kitchen_hand_hint` |
| бедро | — | M2 `touch_thigh` | — |

| Soft break (+1) | → |
|-----------------|-----|
| look → | `tits_lick` |
| hug → | `petting` |
| cloth cock → | `hand` |
| thigh → | `pussy_touch` (**не** cuni) |

---

## Сводная hard (v0)

| | Аманда | Мелисса | Сандра |
|--|--------|--------|--------|
| рот | spit / swallow | mouth_price | swallow_trade |
| рука | hand_finish | hand_strict | hand_pragmatic |
| особое | *(cuni?)* | **cuni_grade** | **titjob** |
| cuni | optional / нет | **да hard** | **нет** |
| titjob | нет | нет | **да** |

---

## Noble (общая схема 5b)

```
if client = noble (редкий roll / table):
  style soft|hard по band
  promise из noble-пула девушки (AN / MN / SN)
else:
  promise из обычного soft|hard пула
```

| Девушка | Soft noble | Hard noble | Включаем? |
|---------|------------|------------|-----------|
| Аманда | flatter / угол | mouth | **да** (сильный fit) |
| Мелисса | verse / поэзия | favor mouth | **да** |
| Сандра | — | — | **скорее нет** |

---

## PromiseBreakTail (логика, без prose)

Хвост после peek **только если** `PromiseBreak=1` и style soft:

| promise family | хвост (смысл) |
|----------------|---------------|
| look_* | «только смотреть» → руки/язык на груди |
| hug_* / poem | «только обнять» → руки ниже / petting |
| touch_cock / kitchen_hand | «сквозь ткань» → уже hand |
| touch_thigh | «снаружи» → пальцы под ткань |

Hard: короткий generic «взял больше / докинул серебро».

---

## Что не в таблице уговора (но есть в missing)

Late random без отдельного soft id: `mouth_balls`, `deepthroat`, `anilingus`, under_table mouth, mom_craftsman —  
остаются в `PickPrivateAct` band 3 / special keys (debug skip / hard mouth + late stage).  
**Не** плодим soft promise на anilingus.

---

## Открытые вопросы (после v0.2)

### Закрыто владельцем
- seq **β** · A5 **LITE** · A7 **ок** · H0 **да, split** · term-rand = **last only**

### Soft v0.4
1. S3-A (A1h→A2h→A3h) или S3-B?
2. Что = **high-флаг** (открытие S3)?
3. Hard H0.a с какой soft-фазы?
4. A2h свой cuni да/нет?
5. S2 break %?

### Hard / прочее
6. Разрез H0 a/b ok?
7. A7 finish anilingus?
8. M/S та же soft-лесенка?

---

## Следующий шаг

1. Подтвердить разрез H0.a/b.  
2. Soft A1–A3 freeze.  
3. M/S.  
4. v1 final table → wiring.

**Prose / код не трогаем.**

---

## История решений в чате (кратко)

- Просмотрен `hall_missing_bargain_text` + logic + agent files.
- Структура **A**; soft break **3a**; Аманда compliance **4a**; noble **5b**.
- Все уговоры переделываем; таблицы first.
- **2026-07-30:** лесенка; A1–A3; A4–A6 mouth; A7 noble.
- **v0.2:** **β** full sub; term-rand **last only**; A5 **LITE**; H0 **split** a→A4→b→A5→A6; A7 N3 ok.

*Документ: `docs/design-hall-missing-bargain-catalog.md`.*
