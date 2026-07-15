# Session handoff — 2026-07-14

Сводка для **другой машины**. Ветка: `main`.  
Читать вместе: `docs/state.md`, `docs/design-character-intimacy-arc.md` (§ live-NTR + § Обида-дни), `docs/economy.md` (§0–0c), `AGENTS.md`.

---

## Git / сборка

```powershell
git pull origin main
powershell -File scripts/build.ps1 -Profile dev
```

| | |
|--|--|
| Репо | `vanisimo/wild-stallion-qsp` |
| Ветка | `main` |
| Сборка (эта линия) | ~2520 локаций, OK |
| Коммиты (код 4b + доки) | `4e49b23` … `eba59b6` (см. log) |

---

## Сделано в коде (уже на main)

### 4b — кнопки сцены / policy после ужина (`4e49b23`)

| | |
|--|--|
| Сцена | **Защитить / Наблюдать / Отвернуться** (`protect_hard` / `watch` / `ignore`) |
| Гейт тройки | **`FamilyLiberationGateOpen`** (не `Act1IsHonestPhase`) |
| До ужина | только **Защитить** (+ policy **сдержанно**) |
| Policy | **Вести себя сдержанно / Решать самой / Вести себя расковано** |
| Файлы | `hall_harassment.qsps`, `kitchen_harassment.qsps`, `girl_work_policy_talk.qsps` |

Ранее (уже в main): economy 70/15/7.5/7.5, tips, wallet spends, dreams eavesdrop, family council 6 screens + dinner image + gate.

---

## Сделано в дизайне (доки, код TODO)

**Полный текст:** `docs/design-character-intimacy-arc.md`

### 1. Профили (не кнопки на старте)

- **Чистый / смешанный / грязный** = **канвы** поведения  
- Чистый: системная узда → сёстры **не** срываются в hard NTR «сами»  
- Грязный: max gates live, не 100% exclusive за один прогон  
- Смешанный: per-girl  

### 2. Live-NTR (сёстры)

- Hard NTR только **live** (видимая **искра** + не пресёк)  
- Пропуск окна → **never auto-sex**; soft + **повтор позже**  
- **Нет** утреннего «уже было, пока тебя не было»  
- Home first закрывает **NPC-first race**, не вечную броню  
- Запрет = **да/нет** only  
- Сандра+Драупнир = своя жизнь; ГГ **пока не** лезет  

**Audit (чинить в коде):** `step_aside` / `leave` на гонках могут ставить FirstSex + `PlayerKnows=0` — **против канона**.

### 3. OffenseDays (обида-дни)

```
OffenseDays = 4 start
−1 / сутки (может пройти сама)
talk: выговор → Извиниться (−1) | «Я прав» (×1) | gift
cheap: −дни +stats↓; expensive: =0 +stats↓
нет эскалации в NTR
```

| Reason | Режим |
|--------|--------|
| dual protect / policy (зал+**кухня**) | **накопление K=3** (1× ignore ≠ lock; гонка!) |
| 7 дней без mismatch | count слабеет |
| intercept | накопление ~3 |
| ban_* | **сразу** |
| Сандра `daughter_no_protect` | сразу; мама узнала **без** присутствия ГГ ok |
| Бекки `neglect_dance` | только если ГГ **был** на танцах |
| Лизетта / Жоржетта | **без** обид |
| Легаре / мэр / Эдди | свои конфликты |

**v1 кода:** движок + сёстры + dual K=3 + ban + Сандра-за-дочь  
**v2:** dance_boundary, Бекки/Инга neglect, Кларисса  
**v3:** gg_harass  

Коммиты доков: `a6a8931`, `eba59b6`.

---

## Статус кода (после `1f77539`)

Пункты 1–5 ниже **в коде**. Дальше: **playtest v1**, не OffenseDays v2.

**QA-чеклист:** [`docs/qa-checklist-paths-offense-v1.md`](qa-checklist-paths-offense-v1.md)

### Было TODO (закрыто в `1f77539`)

1. ~~Гонки: step_aside/leave~~  
2. ~~watch live-beat~~  
3. ~~OffenseDays v1~~  
4. ~~4c тексты~~  
5. ~~Spark queue AFK~~  

---

## Куда смотреть

| Тема | Файл |
|------|------|
| Live-NTR + обиды + audit | `docs/design-character-intimacy-arc.md` |
| Ужин / gate / кнопки зала | `docs/economy.md` §0–0c |
| Переменные / краткий lock | `docs/state.md` |
| Экономика / подарки flat | `docs/economy.md` |
| Агент-правила | `AGENTS.md` / `Agents.md` |
| Голоса | `docs/design-npc-voices.md`, `design-stefan-voice.md` |

---

## Не делать

- Менять `qsp-project.json` без просьбы  
- Подключать `archive/old`  
- Hidden hard NTR сестёр при узде  
- 1× «не защитил» = полный talk-lock (только K=3)  
- Обиды Лизетты/Жоржетты; Драупнир-«лезешь» (пока)  

---

*Handoff 2026-07-14 — пути, live-NTR, OffenseDays, 4b в коде.*
