# Session handoff — 2026-08-14

Продолжение на другой машине. Ветка: `main` → `origin/main`.  
Репозиторий: `vanisimo/wild-stallion-qsp`.  
Не трогать `qsp-project.json`. Отвечать по-русски.

Карта сцен: `docs/prose-hall-missing-map.md`.  
Голоса: `docs/design-npc-voices.md`. Форма u0/u1/nop: `docs/design-hall-scene-unified.md` §0.2.

---

## Где остановились

**Круг перекладки Hall Missing (M3) закрыт.**  
Последнее в коде: форма/бельё на куни и бедре (`HallMissingPrintSkirtAccess`).  
`touch_thigh` — один first-show на слоте h0a, в free-рандом не класть. Флаг «раз и навсегда даже после защиты» **не** ставили.

Следующая сессия — **не** новая большая сцена missing. Дальше другой контур (см. § Следующие шаги).

---

## Лесенка missing (как в коде)

Фазы: `soft_intro` → `soft_play` → `hard` → `free`.  
Шаг двигается после peek/ignore, не после «Защитить».

### soft_intro ×3

`look_tits` → `hug_waist` → `hand`  
(`cock_touch_cloth` слит в `hand`). После 3-го у сестёр нобиль tier 1.

### soft_play ×3 (`HallMissingSoftPlayNeed = 3`)

Те же акты, не строго по порядку. Иногда cuni / titjob Сандры.

### hard — сёстры (5 слотов)

| Слот | Сколько первых | Что |
|------|----------------|-----|
| h0a `piggy_look` / `bud_smell` | 4 | грудь → **бедро** → hug Explicit → cuni |
| рот `mouth_hard` | 5 | mid → taste → spit → hold_spit(=spit) → swallow |
| h0b `piggy_cuni` / `bud_cuni` | 2 | cuni / у сестёр флаг анилингуса |
| лицо `facial` | **2** | soft **на грудь** → high **низ лица+рот** → `FlagFaceDone` |
| горло `deepthroat` | 5 | try → partial → full → в рот → в горло |

После закрытия лица: `HallMissingBargainExplicit = 1` навсегда (`FlagFaceDone`).  
`PickPromise` тогда ещё ставит `Initiative = high`. Soft-ветки в `if Explicit / elseif high / else` больше не играются.

**Explicit ≠ грубый текст.** Мат и шлепки членом — только **повторный** swallow (после лица).  
Explicit в минете = она себе (клитор + пальцы по sluttiness 0–29/30–49/50–99/100+ = 1/2/3/4).

Первый swallow на лесенке **до** лица → только soft/high, без Explicit-слоя.

### hard — Сандра

Один слот рта ×6: mid → swallow → show → facial → DT в рот → DT в горло.  
`Explicit` у неё от `FlagMouthMature` (после её глотка), раньше чем у сестёр.  
Без soft, без анилингуса, titjob только она. Кухня, не подсобка.  
Проза рта/лица/DT — **USER-OWNED**, не переписывать без «можно править тексты».

### free

Рандом soft-актов или hard-терминалов. Нобиль сестёр в пул после горла (`NobleInRandom`).

---

## Слои сцен (сёстры)

| Акт | soft | high | Explicit |
|-----|------|------|----------|
| look_tits | смотрит | руки | лижет + кончает **на грудь** (стр. 3) |
| hug | поверх | под платье, клитор, не внутрь | пальцы + её оргазм. Аманда киска, Мелисса **попа**. Пальцы = sluttiness, не RegisterSex |
| hand | сбоку → **пол** | колени, язык/яйца → **руки** | грудь наружу, яйца в рот → рот/лицо/грудь/трусы |
| cuni | целует вокруг, клитор → пол | язык внутрь, сама подмахивает, жмёт голову → пол | язык на клиторе + пальцы (Мелисса **в попе**) → **на киску** |
| cuni стр. 3 | — | — | анилингус если `CuniToAnilingus` **или** Explicit+high → **на попу**, на киску в этом проходе нет |
| swallow | яйца+рука, глоток | рука, лижет яйца, покажи, глоток | шлепки, мат, она себе, в рот, её оргазм, глотает |
| facial | **на грудь** | низ лица + рот | на лицо, покрасуйся, собирает, ест |
| DT | нет слоёв | нет | уже после лица: глубина+финиш, грудь наружу, она себе. Оргазм только **в горло** |

Сандра: look без стыда, Explicit look → titjob стр. 3–4. Hug сразу high / Explicit киска. Hand сразу high.

Слито: `tits_lick`→look Explicit; `petting`/`pussy_touch`→hug; cloth→hand; titjob сестёр→look; anil сестёр→cuni_3; anil Сандры→cuni.

---

## Статистика

Клиент missing: типы актов считаем. `HadSex` (половые акты с гг) **не** растёт.  
Один тип в одной сцене = +1.

Хелперы в `hall_missing_girl.qsps`:

- `HallMissingRegisterHand` — handjob + финиш. Пол не считаем.
- `HallMissingRegisterCuni` — cuniacts + её оргазм + cumbody если на тело / анилингус.
- `HallMissingRegisterMouth` — oralacts; глоток / лицо / горло / taste по ключу сцены.
- `HallMissingRegisterLookTits` — только Explicit, cumbody.
- `HallMissingRegisterTitjob` — tittyfuck + cumbody; моряк ещё facialcum.
- `HallMissingRegisterSelfPlay` Args[0]=1 если её оргазм — masturbate + опционально orgasms.
- `HallMissingPrintSelfFingers` / `HallMissingHugFingerCount`
- `HallMissingPrintSkirtAccess` [`thigh`|pussy] — u0 длинная / u1 бельё / u1+nop голое.

Новый счётчик: `orgasms[girl]` (init + `girls_desc` + `RegisterSex` тип `orgasm`).

`sex_register.qsps`: cuni, cumbody (слиты breast/hands), cumpanties, masturbate, fisting×2, dp, orgasm.  
Пол (`cumfloor`) нет.

Вечер «зайдёшь» по-прежнему `HadSex>=1` (только гг).

---

## Форма

`HallMissingUniform` 0/1 из `GirlUniformLevel`.  
`GirlNoPantiesWork[girl]`.  
На груди u0/u1 не пишем. На hug уже было. На куни/бедре — хелпер (убрали враньё «всегда голое»).

---

## Файлы этой сессии (missing)

- `modules/events/hall/hall_missing_agent_amanda_text.qsps`
- `modules/events/hall/hall_missing_agent_melissa_text.qsps`
- `modules/events/hall/hall_missing_agent_sandra_text.qsps`
- `modules/events/hall/hall_missing_girl.qsps`
- `modules/events/hall/hall_missing_bargain.qsps`
- `modules/debug/debug_hall_missing.qsps`
- `modules/actions/sex/sex_register.qsps`
- `modules/core/init_npc/girl_init_base.qsps`
- `modules/core/init_npc/girls_desc.qsps`
- `docs/prose-hall-missing-map.md`

В дереве были ещё правки **harass / кухня** (окна H2, kitchen hook) — не эта перекладка M3, но на диске лежали. Их тоже залили, чтобы вторая машина не потеряла.

---

## Следующие шаги

1. **Harass / кухня** — kitchen hook + **H2 сестёр after_beat × client** закрыты (2026-08-15).
2. **Картинки** — hall pipeline: harass/lewd/missing/noble/play_coach → stub+[VIS] / shipped. Инвентарь `docs/ASSET-hall-events-visual.md`. Полный sweep locations/actions — later (`plan-weekend-visual-sweep.md`).
3. **Рот Сандры** — не трогать prose без явного «можно править тексты». Регистр на last page уже стоит.
4. **`mouth_show` сестёр (вариант E, 2026-08):** канон в comments + map — show = swallow high; отдельная локация late/debug only. Prose/redirect/delete **не** делали.
5. Не делать: `under_table`; titjob сестёр; анилингус Сандры; бедро в рандом; два финиша куни+анил в одном проходе.

### Сделано в этой сессии (после pull)

- Фикс escalate: `SandraKitchenChoose` watch+roll → `SandraKitchenEscalateBridge` → Scene.
- Prose kitchen: без «занавески» в refuse/bridge.
- **Kitchen hook доделан (H1–H4):**
  - H1: «Подсмотреть» + «Не обращать внимания» (оффскрин без Follow)
  - H3: protect/watch/offscreen × клиенты; escalate-мост × 3 клиента
  - H4: «ПОСЛЕ: КУХНЯ», after-talk по choice, **policy** (сдержанно/сама/расковано) через `SandraKitchenPolicyChoose`
  - Visual H4: protect (она у двери) / offscreen (ignore)
- **H2 сестёр after_beat:** `HallHarassAfterClientBits` + protect/watch/ignore × girl × beat × client; без «занавески» на кухне.
- **mouth_show сестёр (E):** comments в agent amanda/melissa + `ApplyPromise` + `ResolveSceneKey` + prose map; путь late/debug сохранён.
- **Kitchen H3–H4 prose polish:** protect/watch/end/escalate/offscreen/after × клиенты; голос матери/хозяйки; escalate без «минет-меню» в мосте.
- **Pack v1–v3 → missing:** hand Amanda/Melissa/Sandra, spit/cuni/meets Sandra; карта `docs/prose-hall-missing-pack-map.md`.

---

## Как подхватить на другой машине

```powershell
git pull origin main
```

Сборка: Sublime `qsp-build-and-run`, старт `TraKtir.qsps`, выход `game.qsp`, QSP 5.90.

Дебаг missing: `modules/debug/debug_hall_missing.qsps` (anilingus Сандры → cuni; сестёр → cuni + флаг).
