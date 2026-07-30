# Каталог уговоров hall missing — обсуждение (продолжение)

**Дата:** 2026-07-30  
**Статус:** черновик v0 — **таблицы на обсуждение**, prose и wiring **ещё не трогаем**  
**Контекст:** после разбора `hall_missing_bargain_text` + связки bargain → missing  
**Цель на другой машине:** ответить на **открытые вопросы** в конце → зафиксировать **таблицу v1** → потом wiring, prose позже

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

## Открытые вопросы владельцу (ответить развёрнуто)

Ответы → **таблица v1 final** → wiring plan → prose позже.

### Наборы soft

1. **Аманда soft:** A1–A3 ок? Менять A2 (поцелуй vs только талия)?
2. **Мелисса soft:** M1+M2+M3 ок? Чулки отдельным id? M3 = стих или «на бумагу»?
3. **Сандра soft:** S1–S3 вместо rest — ок? Rest оставить?

### Hard

4. **Аманда hard cuni:** да / нет / редко?
5. **Мелисса hard:** один `mouth` или spit/swallow раздельно?
6. **Сандра hard:** titjob+hand+mouth — ок, cuni off?

### Noble

7. **Сандра noble:** off?
8. Noble: **1 soft + 1 hard** на сестру или только soft?

### Объём

9. Soft всегда **ровно 3** promise на девушку (равные веса ~33%)?
10. Break %: единые 65% или **low initiative → меньше break** (hold чаще)?

### Имена id

11. Чистить id (`hug_kiss`, `look_line`, `poem_corner`) или **максимум старых** (`hug_waist`, `look_tits`) ради меньшего wiring?

### Формат короткого ответа (шаблон)

```
1 …
2 …
3 …
4 …
5 …
6 …
7 …
8 …
9 …
10 …
11 …
+ любые правки таблиц A/M/S / noble
```

---

## Следующий шаг (после ответов)

1. Таблица **v1 final** (только id + hold/break + scene key + %).
2. Матрица «scene key → файл → есть/нет» (чеклист prose **позже**).
3. Wiring plan: `PickPromise` / `ApplyPromiseToAct` / girl-first print — **без** правок строк prose.

**Prose и `hall_missing_agent_*` / `hall_missing_bargain_text` не трогаем**, пока v1 не утвердим.

---

## История решений в чате (кратко)

- Просмотрен `hall_missing_bargain_text` + logic + agent files.
- Обсуждена структура A vs B vs C → выбрано **A**.
- Soft break → **3a** (+1, не cuni).
- Аманда compliance → **4a**.
- Noble → **5b**.
- Все уговоры переделываем; сначала **таблицы**, prose нет.

*Документ сохранён, чтобы продолжить с другой машины с этого места.*
