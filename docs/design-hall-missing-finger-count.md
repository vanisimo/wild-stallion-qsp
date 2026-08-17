# Design: подсчёт пальцев — petting (клиент) и мастурбация (себе)

**Статус:** снимок кода 2026-08  
**Система:** hall missing  
**Код:**  
- `#HallMissingHugFingerCount` — `modules/events/hall/hall_missing_girl.qsps`  
- `#HallMissingPrintSelfFingers` — там же  
- prose: `hall_missing_agent_*_text.qsps` (hug_waist Explicit, deepthroat / self-play)

**Связано:** `design-hall-soft-high-explicit-ladders.md` · `design-hall-missing-bargain-catalog.md` · pack petting/hand

---

## 0. Два разных «подсчёта»

| # | Кто трогает | Переменная | Где в сцене | Смысл |
|---|-------------|------------|-------------|--------|
| **A. Client fingers** | клиент **внутрь** девушки (petting / hug Explicit) | `HallMissingHugFingers` 1…4 | hug page 2 (Explicit) | сколько пальцев **он** засовывает |
| **B. Self fingers** | девушка **себе** (мастурбация во время сцены) | тот же счётчик через `PrintSelfFingers` | deepthroat и др. self-play | сколько пальцев **она** себе + клитор |

Оба используют **одну** функцию счёта `#HallMissingHugFingerCount` (зависит от `sluttiness[girl]`).  
Имена исторические (`Hug*`), но счётчик = **ёмкость / опыт** девушки, не «только обнимашки».

---

## 1. Формула счёта (`#HallMissingHugFingerCount`)

```
HallMissingHugFingers = 1
if sluttiness[girl] >= 100 → 4
elseif sluttiness[girl] >= 50 → 3
elseif sluttiness[girl] >= 30 → 2
else → 1
```

| `sluttiness` | Пальцев |
|--------------|---------|
| 0…29 | **1** |
| 30…49 | **2** |
| 50…99 | **3** |
| 100+ | **4** |

**Нет** зависимости от: phase, Explicit, initiative, uniform, client type, HardStep.  
Только **личная** `sluttiness` на момент вызова.

Вызов: `gs 'HallMissingHugFingerCount'` **перед** строками, где нужны ветки по пальцам (обычно в начале hug / перед PrintSelfFingers).

---

## 2. A — клиент засовывает пальцы (petting / hug)

### 2.1 Когда

| Условие | Поведение |
|---------|-----------|
| Act `hug_waist` / petting-линия, **Explicit = 1** | page 2: пальцы **внутри** + строки «N пальцев» |
| Explicit = 0, initiative **high** | гладит губы/клитор **снаружи**, **внутрь не пускает** (Аманда) / только бёдра–клитор (Мелисса) — **без** счётчика в prose |
| Explicit = 0, soft | попа / бёдра поверх ткани — **без** счётчика |
| `pussy_touch` как отдельный act | отдельная prose; **не** обязана вызывать HugFingerCount (сейчас счётчик в основном на **hug Explicit**) |

### 2.2 Где в prose (сейчас)

| Девушка | Счётчик | Ветки «N пальцев» в тексте |
|---------|---------|----------------------------|
| **Аманда** | `gs 'HallMissingHugFingerCount'` в `hug_waist` start | page2 Explicit: 4 / 3 / 2 / 1 («узенькая») |
| **Мелисса** | то же | page2 Explicit: 4 / 3 / else («горячо») — **нет** отдельной ветки «2» |
| **Сандра** | вызывается | page2 Explicit: ласка губ/клитор **без** строк «N пальцев» (тон зрелый, без подсчёта вслух) |

### 2.3 Канон реплик (клиент → внутрь)

**Аманда (Explicit):**
- 4: «ненасытная… **четыре** пальца легко берёт»
- 3: «**три** пальца внутри тонут… мокрая»
- 2: «**два** пальчика… горячо»
- 1: «узенькая…» осторожно **одним**

**Мелисса (Explicit):**
- 4: «ненасытная… **четырьмя**»
- 3: «**три** тонут в соках»
- else (1–2): «горячо как в печи» (без числа)

**Сандра:** без озвучки числа — «ласкает губки и клитор» → оргазм page3.

### 2.4 Soft / high / Explicit (petting + пальцы)

| Тон | Клиент | Пальцы |
|-----|--------|--------|
| **soft** | обнять, попа поверх | **0 внутри** |
| **high** | под юбку, клитор / губы снаружи | **0 внутри** (или лёгкое касание без count) |
| **Explicit** | внутрь + оргазм (page3 у A/S) | **1…4** по slut |

Break soft (catalog): «пальцы внутрь + оргазм» = по смыслу **Explicit petting**, не отдельный act id.

---

## 3. B — мастурбация себе (self fingers)

### 3.1 Helper `#HallMissingPrintSelfFingers`

Снова вызывает `HallMissingHugFingerCount`, затем:

| Fingers | Строка (код) |
|---------|----------------|
| ≥4 | `Себе: клитор и четыре пальца.` |
| ≥3 | `Себе: клитор и три пальца.` |
| ≥2 | `Себе: клитор и два пальца.` |
| 1 | `Себе: клитор, один палец.` |

Это **короткий служебный/нарративный маркер** (не всегда «диалог клиента»).

### 3.2 Где вызывается сейчас

| Сцена | Девушка | Вызов |
|-------|---------|--------|
| **deepthroat** (page1) | Аманда | `gs 'HallMissingPrintSelfFingers'` — она себе под юбкой, пока берёт в горло |
| hand / cuni / mouth | — | **не** везде; часто **хардкод** в prose (напр. Мелисса hand: «**два** пальца…» без helper) |

### 3.3 Регистрация

`#HallMissingRegisterSelfPlay` [orgasm 0|1]:  
`masturbate[girl] += 1`, опционально `orgasms[girl] += 1`.

Используется после deepthroat finish (Аманда: orgasm если `cum_throat`).

### 3.4 Канон: мастурбация vs клиентские пальцы

| | Client fingers (A) | Self fingers (B) |
|--|--------------------|------------------|
| Кто | клиент | девушка |
| Типичный act | hug Explicit, petting break, cuni bridge | handjob + себе; DT; oral wait |
| Счёт | `HallMissingHugFingers` | тот же roll |
| Prose | «N пальцев **внутри**» (он) | «себе: клитор + N» / вплетено в сцену |
| Finish | её оргазм от **его** руки | её оргазм от **своих** пальцев (+ его акт) |

---

## 4. Handjob (мастурбация **ему**) — не путать

`#HallMissingHandPickFinish` / `#HallMissingRegisterHand` — это **рука на члене клиента**, не пальцы в киске.

| Explicit | Finish pool |
|----------|-------------|
| Explicit=1 | mouth / face / breast / panties (если есть бельё) |
| high или Сандра | `hands` (на ладони) |
| soft | `floor` |

**Подсчёта пальцев на члене нет** (хватает «ладонь / кулак» в prose).

Self-fingers у **неё** во время hand — только если prose/helper явно вызывают (сейчас чаще DT, не hand).

---

## 5. Что есть / чего нет

### Есть
- Единый порог slut → 1…4 пальца  
- Amanda/Melissa hug Explicit с ветками по `HallMissingHugFingers`  
- PrintSelfFingers на DT Аманда  
- RegisterSelfPlay / RegisterHand  

### Нет / дыры
- Сандра hug: **нет** озвучки «N пальцев»  
- Melissa hug: нет чёткой ветки **2** пальца  
- `pussy_touch` / `petting` act: **не** всегда зовут HugFingerCount  
- Handjob scenes: self-fingers **не** на helper (иногда хардкод «два пальца»)  
- Нет отдельной var `HallMissingClientFingers` vs `HallMissingSelfFingers` (один счётчик)  
- Нет роста пальцев от `HallMissingGirlPrivateCount` / phase (только slut)

---

## 6. Рекомендации (если допиливать)

1. **Всегда** `gs 'HallMissingHugFingerCount'` в начале page, где клиент лезет внутрь (hug Explicit, pussy_touch Explicit, petting break).  
2. Self-play: везде `PrintSelfFingers` **или** prose с тем же порогом, без «магических двух пальцев» вразрез со slut.  
3. Опционально позже:  
   - client fingers bias +1 при Explicit + stage high;  
   - self fingers min(client, 4) или отдельно soft self = 1 всегда.  
4. USER-OWNED: менять только числа/ветки в agent text с разрешения; helper — в `hall_missing_girl.qsps`.

---

## 7. Быстрая шпаргалка

```
sluttiness → HallMissingHugFingers (1/2/3/4)

PETTING / HUG Explicit:
  client → N пальцев внутрь + (часто) оргазм девушки

HIGH (не Explicit):
  снаружи / клитор; внутрь — нет или без count

SOFT:
  поверх ткани

SELF (мастурбация себе):
  PrintSelfFingers → «клитор + N пальцев»
  RegisterSelfPlay

HANDJOB (ему):
  HandPickFinish → mouth|face|breast|panties|hands|floor
  пальцы в киске — только если self-play в той же сцене
```

---

*Источник истины runtime: `hall_missing_girl.qsps` §HugFingerCount / PrintSelfFingers; prose — agent text.*

---

## Changelog ladder (2026-08, Amanda)

| | |
|--|--|
| **S-AM-04 touch_thigh** | **снят** с h0a / free-random; legacy → `hug_waist` |
| **h0a** | look_tits → hug → hug Explicit → cuni (**без** thigh) |
| **S-AM-06 wipe/taste** | только **soft\|high** мост к spit/swallow; Explicit в сцене = high |
| **free mouth** | terminals spit/swallow only, **не** wipe/taste |
