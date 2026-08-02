# Design: уговор missing + обида / отказ / нобиль / слух

**Статус:** код v1 **вшит** (2026-08-01). Prose — **черновик**, владелец правит вкус.  
**Не** отдельная сцена уговора: клиент говорит **как в обычной ветке**, при обиде меняется **только ответ** девушки.

---

## 0. Файлы

| Файл | Роль |
|------|------|
| `modules/events/hall/hall_missing_bargain.qsps` | phase, pick promise, start UI |
| `modules/events/hall/hall_missing_bargain_hooks.qsps` | **CODE:** `TryOffenseAnswer`, rumor gates |
| `modules/events/hall/hall_missing_bargain_text.qsps` | **TEXT:** уговоры `[B-…]` + отказы + rumor + noble dig |
| `modules/core/family/offense_days*.qsps` | `GirlOffenseDays[girl]` |

### Где править prose

| Что | Локация / якорь |
|-----|-----------------|
| Обычные уговоры (клиент + «да») | `#HallMissingBargainPrintAmanda` / `PrintMelissa` / `PrintSandra` — ветки `$p = …` |
| **Отказ при обиде** (только ответ) | `#HallMissingBargainOffenseAnswerText` — по `$op` = `$HallMissingPromise` |
| **Нобиль + обида** (не отказ) | ветки `elseif $p = 'noble'` внутри PrintAmanda / PrintMelissa |
| Намёк «распутные» | `#HallMissingBargainRumorHintText` |
| Пьяный отказ | начало Print* — `drunk_guest` (всегда отказ) |

---

## 1. Поток экрана «УГОВОР»

```
#HallMissingBargainPrintText
  лид (тень / кухня)
  optional rumor hint (substantial gate, ~55%)
  PrintAmanda | PrintMelissa | PrintSandra
    → пьяный? → всегда отказ, Refused=1, exit ветки
    → ветка $p (обычный клиент из [B-…])
    → *pl ' '
    → gs 'HallMissingBargainTryOffenseAnswer'
         if обида и promise ≠ noble:
            Refused=1, OffenseAnswered=1
            gs 'HallMissingBargainOffenseAnswerText'   // только ответ
         if noble: no-op (не отказ)
    → if OffenseAnswered = 0:
            обычное «да» из этой же ветки
    → noble + GirlOffenseDays>0:
            «да» + укол Стефану (язык / взгляд) + NobleOffenseDig=1
  if Refused: «уговор сорвался…»
  elif NobleOffenseDig: «разговора не будет, гордо ушла…»  // без «поговорим»
  else: хвост «уходят в подсобку / кухня»
```

Кнопки (`hall_missing_bargain.qsps`):

| | |
|--|--|
| `Refused = 1` | «Вернуться к работе» → `TavernMain` (missing **не** идёт) |
| иначе | «Слушать дальше…» → `HallMissingBargainContinue` → missing |

---

## 2. Обычный уговор + обида = слой `if`

**Канон:** не отдельный блок «отказ-уговор».  
Клиент = **тот же** текст ветки `[B-AM-01]` и т.д.  
Обида = **другой ответ** вместо «да».

В коде после реплики клиента:

```
gs 'HallMissingBargainTryOffenseAnswer'
if HallMissingBargainOffenseAnswered = 0:
    …обычное согласие…
end
```

Повторный вызов в многошаговом soft (Сандра): если уже `Refused=1` — **не** печатать отказ второй раз.

---

## 3. Реальные `$HallMissingPromise` (только они в отказах)

### Аманда

| `$p` | Уговор (якорь) | Отказ при обиде — о чём |
|------|----------------|-------------------------|
| `look_tits` | B-AM-01 глазком / аккуратные | нет «глазком»; Стефан сам сиськи |
| `hug_waist` | B-AM-02 обнять / запах | нет обнимашек; с ним обнимайся |
| `touch_cock` | B-AM-03 тесно в штанах / ручки | нет сквозь ткань / «до капли» |
| `piggy_look` | B-AM-H0a копилка / мамина | нет уголка / копилки |
| `piggy_cuni` | B-AM-H0b губами / вылижу | нет «снова в угол» |
| `mouth_hard` / `facial` / `deepthroat` | B-AM-MT губками / рот | нет минета; к хозяину |
| `noble` | B-AM-N | **не отказ** — см. §4 |
| *(else)* | generic | закрыта подсобка |

**Нет** у Аманды: `titjob`, `look_line`, `bud_*`, `hand` как отдельные id.

### Мелисса

| `$p` | Уговор | Отказ — о чём |
|------|--------|----------------|
| `look_tits` / `look_line` | B-ME-01 вырез / взгляд / спинтрии | печаль, книги; сам сиськи |
| `hug_waist` | B-ME-02 стан / атлас | не лезь; стан к Стефану |
| `touch_cock` | B-ME-03 штурвал / корень | метафоры из штанов — нет |
| `bud_smell` | B-ME-H0a бутончик | нос / книги |
| `bud_cuni` | B-ME-H0b язык | нет |
| `mouth_hard` / `facial` / `deepthroat` | B-ME-MT | губы/рот — нет |
| `noble` | B-ME-N | **не отказ** — §4 |

### Сандра (кухня)

| `$p` | Уговор | Отказ — о чём |
|------|--------|----------------|
| `look_tits` / `tits_lick` | B-SA-01 грудь у печи | кухня=готовка; скалка |
| `hug_waist` / `petting` | B-SA-02 попа / под столом | к сыну тискай; скалка |
| `touch_cock` / `hand` | B-SA-03 рука / готовка | не по голове — «чем думаешь» |
| `mouth_hard` / `mouth_mid` / `mouth_swallow` / `mouth_show` / `facial` / `deepthroat` | B-SA-MT | колени у печи — нет |
| `titjob` | B-SA-TJ | между сисек — нет (только Сандра) |
| *(else)* | generic | кухня для готовки |

---

## 4. Нобиль + обида (исключение)

**Канон:** выпал `noble` при `GirlOffenseDays > 0` → девушка **не отказывает**.

1. Обычный уговор дворянина + обычное «да».  
2. **Доп. слой** (только при обиде):  
   - **Аманда** — дерзко показывает **язык** Стефану из тени, берёт дворянина, **гордо** уходит, без разговора.  
   - **Мелисса** — **довольный** взгляд на Стефана, гордо в подсобку, молчание.  
3. `HallMissingNobleOffenseDig = 1` → хвост PrintText: «разговора не будет…» (не talk с ГГ).  
4. `TryOffenseAnswer` для `noble` — **exit** (не Refused).

Сандра нобиля в pick обычно **нет**.

---

## 5. Пьяный

`drunk_guest` / `drunk` в **начале** Print*:

- **всегда** отказ (policy 3 мягче / иначе жёстче);  
- **не** зависит от обиды;  
- `Refused = 1`.

---

## 6. Rumor hint (намёк «распутные / пропадают»)

| | |
|--|--|
| CODE | `HallMissingBargainRumorHintCan` + `TryRumorHint` |
| TEXT | `HallMissingBargainRumorHintText` |
| Когда | substantial: SoftPlayDone / hard phase / HardStep / FlagFaceDone; не soft A1–A3 alone + PrivateCount&lt;2 без backroom/easy |
| Шанс | ~55% |
| Ротация | `HallMissingRumorLine` 0..3 (зал vs кухня Сандра) |

**Backlog (не в уговоре):** dirty на T3 harass; service ambient в осмотре зала — `docs/design-tavern-client-ambient.md`.

---

## 7. Связь с OffenseDays (общий канон)

| Пока `GirlOffenseDays[girl] > 0` | |
|--------------------------------|--|
| Talk / intimate с ГГ | закрыто (движок offense) |
| **Обычный** bargain | клиент говорит → **отказ** (§2–3) |
| **Нобиль** bargain | **соглашается** + укол (§4) |
| Play → missing (если уговор не сорван) | нобиль/успех → missing может идти; отказ → нет |
| Harass intro refuse | **backlog** (зал/кухня без bargain) — intimacy-arc |

Полный движок дней/reasons: `docs/design-character-intimacy-arc.md` § Обида-дни.

**Уточнение 2026-08:** «нет bargain при обиде» **неверно** для missing-уговора — bargain **показывается**, ответ другой (кроме нобиля).

---

## 8. Чеклист правки текстов (владелец)

1. `[B-AM-*]` / `[B-ME-*]` / `[B-SA-*]` — клиент + «да» (уже канон-промт).  
2. `#HallMissingBargainOffenseAnswerText` — отказы по `$op` (таблица §3).  
3. Noble dig в ветках `$p = 'noble'` (Аманда / Мелисса).  
4. `#HallMissingBargainRumorHintText` — слухи.  
5. Пьяный — в начале Print* (трогать осторожно).  
6. **Не** плодить promise id, которых нет в PickPromise/Print*.  
7. **Не** bulk-rewrite USER-OWNED «да» без нужды — только слой отказа / dig.

---

## 9. Переменные

| Var | Смысл |
|-----|--------|
| `GirlOffenseDays[girl]` | дни обиды |
| `HallMissingBargainRefused` | 1 → нет missing, кнопка назад |
| `HallMissingBargainOffenseAnswered` | 1 → не печатать «да» |
| `HallMissingNobleOffenseDig` | 1 → хвост «гордо ушла» |
| `$HallMissingPromise` / `$op` | id уговора |
| `HallMissingRumorLine` | 0..3 для rumor text |

---

*Документ для правки prose. Код: hooks + вшитый `TryOffenseAnswer` в ветках Print*.*
