# Design: Hall Missing — слои act / finish / client / corruption

**Статус:** канон утверждён (обсуждение 2026-07).  
**Связь:** `docs/design-hall-scene-unified.md` (§0.5–0.6), `hall_missing_girl.qsps`, `hall_missing_girl_text.qsps`  
**Тон late/dirty:** лёгкая игра, подколы, «смотрел — значит можно»; без морали и без «зал делает вид».

---

## 0. Решения (зафиксировано)

| # | Вопрос | Решение |
|---|--------|---------|
| 1 | Ось коррупции | **Все три:** `sluttiness[girl]` + `FamilyCorruptionStage` + `HallMissingGirlPrivateCount` (и stage/band как сейчас) |
| 2 | Finish | **Отдельный roll** `$HallMissingFinish`, bias от client + tier |
| 3 | «Как мама» (craftsman) | **И к Аманде, и к Сандре** (и при желании намёк к Мелиссе — реже). Реакции — см. §4 |
| 4 | Sister_kiss («поцелуй сестру после») | **Act 2+** — не в missing v1 |
| 5 | `drunk_guest` | **Никогда** в missing / play (канон v2) |
| 6 | Первый пакет прозы | **Все три девушки**, storage, mouth-line + 3 client + finish mouth/show/face (эталон) |

**Мелисса + anilingus:** любимый late-act; **доп. описания** обязательны (она получает кайф, не «терпит»). После первых аналов с ГГ/NPC — шутки вокруг анала/языка в попу (уже канон hall play `on_face`).

---

## 1. Склейка экрана `peek_scene`

```
[place body]     — storage / under_table / kitchen / stairs; форма u0|u1|u1+nop
+ [act core]     — $HallMissingPrivateAct
+ [finish]       — $HallMissingFinish (куда кончил + что она сделала)
+ [client line]  — 1–2 реплики гостя (тип × band)
+ [girl → client]
+ [girl → stefan] — если дверь / взгляд; иначе в peek_meet
```

Roll finish + client bits **один раз** при старте missing; все экраны читают те же флаги.

---

## 2. CorruptionDetailTier (считается 1 раз)

Не новая глобальная шкала — локальный tier для текста:

```
tier = 1
if sluttiness[girl] >= 35 or HallMissingGirlStage >= 4:
    tier = 2
if sluttiness[girl] >= 50 and (HallMissingActBand = 3 or PrivateCount[girl] >= 2):
    tier = 3
if sluttiness[girl] >= 65 and FamilyCorruptionStage >= 3 and GirlWorkPolicy[girl] >= 2:
    tier = 4
```

| tier | show-рот | deepthroat / balls pool | facial | no_wipe | sister_kiss |
|------|----------|-------------------------|--------|---------|-------------|
| 1 | нет | нет | нет | нет | нет |
| 2 | редко | нет | нет | нет | нет |
| 3 | да | да | roll | нет | нет |
| 4 | часто | да | чаще | roll | **Act2+ only** |

Band act (уже в коде):

| Band | Acts |
|------|------|
| 1 early | petting, tits_lick, pussy_touch, cock_touch, hand |
| 2 mid | hand, mouth, cuni (+ titjob Sandra) |
| 3 late | mouth_balls, deepthroat, anilingus, cuni (+ titjob Sandra) |

**Мелисса late:** вес `anilingus` **выше**, чем у сестёр (например +15–20% pool за счёт deepthroat/cuni).  
**Аманда:** bias mouth / show / «смотрят».  
**Сандра:** bias cuni / ass / body cum; меньше болтовни.

---

## 3. Finish ids (отдельный roll)

| id | Суть | Min tier | Act bias |
|----|------|----------|----------|
| `cum_mouth` | в рот, глотает тихо | 2 | mouth, deepthroat |
| `cum_show` | полный рот → показать → сглотнуть | 3 | mouth+ |
| `cum_face` | на лицо / губы / щёки | 3 | mouth, hand |
| `cum_throat` | глубоко + «держи» | 3 | deepthroat |
| `cum_body` | на попу / поясницу / живот | 2 | cuni, anilingus, hand |
| `cum_hand_lick` | на ладонь → слизала | 2 | hand |
| `clean_all` | член/яйца дочиста языком, поцелуй головки | 3 | mouth+ |
| `no_wipe` | «не вытирай» | 4 | face/body |
| `sister_kiss` | «поцелуй сестру» | 4 + **Act2** | rare |

**Client finish bias:**

| Client | Предпочтения |
|--------|----------------|
| `rich_merchant` | cum_mouth, cum_show, clean_all (контроль, «качество») |
| `craftsman` | cum_mouth, cum_face (реже), «как мама»-реплика в mid-line |
| `traveler` | cum_face, cum_throat, cum_body (грубее/веселее) |
| `drunk_guest` | **не roll** — не в missing |

---

## 4. Craftsman: «как мама» / «с детства»

Доступно **Аманде и Сандре** (local familiar). Мелиссе — редко или другая формулировка («как в книжке…» не «мама»).

### Реакции (не мораль, не «не говори такое»)

| Девушка | Реакция на «как мама» / «с детства» |
|---------|-------------------------------------|
| **Аманда** | **Усиление возбуждения** — краснеет, берёт глубже / трёт себя сильнее, иногда тихо «не надо…» без остановки |
| **Мелисса** | **Стыд** — одёргивает кучеряшку, сжимает губы, на миг теряет «королевскую» ровность; продолжает, но жёстче/тише |
| **Сандра** | **Не спорит словами.** Прикусывает губу / сдавливает член **сильнее** (рука или бёдра), дыхание тяжелее — тело отвечает, рот почти молчит |

Запрет: праведный отпор, слёзы-обвинение, mid-Act1 «как ты смеешь про мать».

---

## 5. Клиенты — портрет и реплики (направление)

| id | Тело / сцена | Тон реплик |
|----|--------------|------------|
| **rich_merchant** | **Пузо** — под ним тесно (under_table / колени у бочки); серебро | «Хорошая девочка», «за монету — глубже», спокойная пошлость |
| **craftsman** | «Свой», запанибрата | «Старательная, как мама»; «с детства такая?»; к Сандре — «хозяйка сама» + мама-линия late |
| **traveler** | Моряк / военный | «Ваш город всё больше нравится»; «в порту так не кормят» |
| **drunk_guest** | — | **вне** missing/play |

### Девушка × клиент (шутки)

| | Merchant | Craftsman | Traveler |
|--|----------|-----------|----------|
| **Аманда** | пузо, серебро, попа; грудь — **редко** | мама → +возбуждение; смотр-фетиш | город + «снова на колени» |
| **Мелисса** | «я сама», торг, кучеряшка | стыд на «семья/мама»; короче | «чёрт», она ведёт |
| **Сандра** | «тише / не рычи», большая попа + животик **красиво** | сдавить сильнее, мало слов | минимум реплик |

**Мелисса anilingus (обязательный слой):**  
клиент раздвигает ягодицы, язык в анус; она **подставляется**, стонет иначе, чем на cuni; late — сама чуть подаёт попу; шутка (tier3+): намёк «там лучше, чем в романе» / без морали.

---

## 6. Переменные (скелет кода)

```
$HallMissingClient          ! rich_merchant | craftsman | traveler  (не drunk)
HallMissingDetailTier       ! 1..4
$HallMissingPrivateAct      ! уже есть
$HallMissingFinish          ! cum_mouth | cum_show | cum_face | …
$HallMissingClientLineId    ! optional key для debug
HallMissingMomLine          ! 0/1 — craftsman сказал «как мама»
HallMissingSisterKissReady  ! 0 в Act1; Act2+ rare
```

### Порядок gs (peek_scene)

1. `HallMissingCalcDetailTier`
2. `HallMissingPickPrivateAct` (уже; + Melissa anilingus weight)
3. `HallMissingPickFinish` (act + client + tier)
4. `HallLewdFillClientBits`
5. Print: place → act body → finish → client dialog → girl dialog  
6. `HallMissingGirlReaction` / peek_meet / interrupt — тон dirty play, без упрёков

---

## 7. Тон UI-реакций (late / FromPlay / dirty)

| Было (плохо) | Стало |
|--------------|--------|
| «Реши, хозяин ты или зритель» | «Смотрел и молчал… тебе нравится?» / «Не мешай» |
| Сандра «без слёз», праведный взгляд | сжато, хочет довести; злость на **срыв**, не на «ты плохой» |
| Мелисса ледяной упрёк | ровно, чуть сверху, подкол; anilingus — кайф |
| «Зал делает вид…» | конкретный гость **или** никак |
| Мета «голос ровный» | только действие + реплика |

---

## 8. Пакеты прозы (очередь)

| Пакет | Содержание |
|-------|------------|
| **P1** | storage, mouth-line, 3 client, finish `cum_mouth` / `cum_show` / `cum_face`, **все 3 girl**, tier ≥3 dirty |
| **P2** | under_table + merchant пузо; craftsman mom-line + реакции §4 |
| **P3** | late acts: deepthroat, mouth_balls, **Melissa anilingus++** |
| **P4** | clean_all, cum_body, no_wipe (tier4) |
| **P5 Act2** | sister_kiss rare |

---

## 9. Физика / фетиши (напоминание)

| | |
|--|--|
| **Аманда** | маленькая грудь (шутки **редко**); красивая попа; **смотрит / на неё смотрят** = фетиш |
| **Мелисса** | не любит кучеряшки (одёргивает); **anilingus / анал** — сильный кайф late |
| **Сандра** | большая попа + лёгкий животик — **оба красивые** |
| **Форма** | u0 подол ~середина голени; u1 выше колена ~середина бедра, декольте; u1+nop |

---

## 10. Культ чистоты (после finish — обязательно)

После любого cum **не уходят «как есть»**. Всегда один из слоёв:

| id | Что | Когда |
|----|-----|--------|
| `wipe_cloth` | вытереть фартуком / краем юбки / тряпкой | tier 2+ всегда доступно |
| `wipe_hand` | пальцем снять → на ткань | mid+ |
| `lick_self` | слизать с губ / пальцев / подбородка / тела | tier 2–3+ (Аманда охотнее) |
| `clean_cock` | облизать член / головку / остатки клиенту | **late only** (tier 3–4 / high stage) |
| `clean_full` | член + яйца + поцелуй головки | **late high** (tier 4) |

**Правило:** сцена заканчивается **чистой** (или явно «привела себя в порядок»), не «сбежала в сперме».  
`no_wipe` («не вытирай, ходи так») — **исключение dirty rare**, не норма; если есть — потом всё равно убирает до выхода в зал (или только на private place).

Порядок после finish:

```
cum → (optional clean_cock late) → wipe/lick self → поправить одежду → [peek_meet / уход]
```

---

## 11. Не делать

- Drunk в missing/play  
- Sister_kiss в Act1  
- Уход без уборки (кроме rare no_wipe → всё равно вытереть до зала)  
- Полные тексты на каждый cross-product — только **слои**  
- USER-OWNED rewrite без явного OK  
- Мораль / «ты меня не защитил» в late dirty FromPlay  
- Мета-описания тона в `*pl`
