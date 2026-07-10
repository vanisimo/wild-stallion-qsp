# Girl-pair gossip pools (design)

Дизайн болтовни пар NPC: пул фраз по флагам, подслушивание, лимиты визитов.
Код-эталон: `AmandaLizaTalk` (`amanda_liza_talk_pick.qsps`, `amanda_liza_overhear.qsps`).

Статус: **дизайн** (реализация поэтапно). SexScene girl orgasm cap + marathon pending — отдельно.

---

## 1. Lizette + Amanda — канон расписания

### Цепочка знакомства

| Шаг | Когда | Где | Что |
|-----|-------|-----|-----|
| 1 | День корабля (не воскресенье) | `Port`, у трапа | `PortAmandaLizette` — осмотр → `AmandaMetLizette`, `LizetteKnown`, `LizetteVisitStage = 1` |
| 2 | Рабочие дни, трактир открыт | `TavernMain` | Аманда **работает**; Лизетта в `Market` / `Port` — в зал приходит **в гости** (лимит визитов) |
| 3 | Воскресенье день + вечер | `AmandaRoom` | Обе по `npc_city_schedule` (`sunday_visits`): Аманда дома, Лизетта в комнате Аманды |
| 4 | Воскресенье утро / полдень | `Church` | Служба / исповедь — **не** болтовня пары (другие системы) |

**Правило:** в **комнате** подслушивание и сюжетный `room_visit` — **только** `week = 7` и фаза `sunday_visits` (`time` 3–4). В остальное время Аманда не «сидит в комнате с Лизеттой» — она в зале / порту / дома без гостьи.

**Расхождение с кодом (исправить при реализации):** `AmandaLizaTalkCanTrigger` для `amandaroom` сейчас не требует `week = 7`; фактически Лизетта в `AmandaRoom` только в воскресенье — но лучше зафиксировать явно в гейте.

### Два типа контента в комнате (воскресенье)

| Тип | Локатор | Частота |
|-----|---------|---------|
| **Сюжетный визит** | `AmandaLizetteTryEvent` → `room_visit` | 1 раз (`LizetteVisitStage` 1→2), не пул |
| **Пул фраз** | `AmandaLizaTalk` в `AmandaRoom` | По лимиту визитов + roll |

### Зал (рабочие дни)

- Триггер: вход в активность зала (`tavern_hall_activity` → `AmandaLizaTalkTryStart`).
- **Не чистый random:** лимит **визитов Лизетты в зал** на неделю + roll внутри визита.
- Гейт зала: `LizetteKnown`, Аманда в `TavernMain`, трактир открыт, Лизетта «пришла в гости» (`AmandaLizaHallVisitReady = 1`).

---

## 2. Лимиты визитов (предложение)

### Переменные

```
AmandaLizaHallVisitsWeek      ! сколько раз Лизетта зашла в зал на этой неделе
AmandaLizaRoomTalksWeek       ! подслушивания в комнате (воскресенье)
AmandaLizaTalkHeardTotal      ! всего (статистика, опционально)
```

Сброс: в `next_day` при смене `week` (как другие недельные счётчики).

### Квоты

| Канал | Макс / неделя | Roll при визите | Примечание |
|-------|---------------|-----------------|------------|
| **Зал** | **2** визита | 40% → кнопка «Подслушать» | Визит = отдельный флаг дня `AmandaLizaHallVisitDay[day]` |
| **Комната (вс)** | **1** пул-болтовня | 55% (как сейчас) | Не считать сюжетный `room_visit` |
| **Часть дня** | 1 overhear | `AmandaLizaTalkUsedKey = day_time` | Уже есть |

**Когда назначать визит в зал:** при `UpdateGirlLocations` / входе в `TavernMain`, если `AmandaLizaHallVisitsWeek < 2` и roll 25% — `AmandaLizaHallVisitReady = 1`, `$GirlLocation['lizette']` временно `TavernMain` (или только флаг без смены локации на карте).

**Корабль:** день судна не +1 к залу; только порт-знакомство.

---

## 3. Общий алгоритм пула (все пары)

```
1. Триггер (визит / воскресенье / зал)
2. Проверить лимиты и *HomeSex / witness флаги канала
3. BuildPool — все PhraseEligible
4. Pool пуст → Tier 0 «просто болтовня»
5. Иначе PickPhrase (вес по tier)
6. Текст + ApplyEffects (bond, Friends, oral ladder…)
7. One-shot фразы: PhraseHeard[id] = 1 исключают повтор
```

### Tier

| Tier | Смысл | Пример гейта |
|------|--------|--------------|
| 0 | Фон | всегда (если пул иначе пуст) |
| 1 | ГГ **видел** | `EventWitnessed`, peek-флаги |
| 2 | Сама пережила | `*HomeSex`, Legare flags, статы |
| 3 | Редкое / cooldown 7д | marathon pending, новая форма |

---

## 4. Amanda + Lizette — таблица фраз

### Уже в коде (`AmandaLizaTalkPhraseEligible`)

| id | tier | Гейт (кратко) | В pool | One-shot |
|----|------|---------------|--------|----------|
| `naive_children` | 0 | slut≤8, sexacts=0 | да | нет |
| `naive_hole` | 0 | slut≤8, sexacts=0 | да | нет |
| `naive_not_only_kiss` | 0 | slut≤8, sexacts=0 | да | нет |
| `naive_mother_many_kids` | 0 | slut≤8, sexacts=0 | да | нет |
| `curious_stefan` | 0 | slut>8, sexacts=0 | да | нет |
| `curious_oral` | 0 | slut>8, sexacts=0 | да | нет |
| `curious_first_time` | 0 | slut>8, sexacts=0 | да | нет |
| `curious_before_wedding` | 0 | slut>8, sexacts=0 | да | нет |
| `ban_legare_low` | 1 | LegareInstruction≥1, slut<25 | да | нет |
| `ban_legare_high` | 1 | LegareInstruction≥1, slut≥25 | да | нет |
| `ban_lizette` | 1 | LizetteBanned | да | нет |
| `ban_guys` | 1 | AmandaProhibitGuys | да | нет |
| `legare_suck_advice` | 1 | LegareInterest≥8, oral>0, no Legare first sex | да | нет |
| `legare_give_him` | 1 | LegareInterest≥10, no Legare first sex | да | нет |
| `oral_but_virgin` | 2 | sexacts>0, virginity=1 | да | нет |
| `bed_deflower_talk` | 2 | AmandaHomeSex, sexacts<20 | да | нет |
| `stefan_brother_fuck` | 2 | AmandaHomeSex | да | нет |
| `legare_deflower` | 2 | AmandaLegareFirstSexDone | да | **да** |
| `legare_married_rumors` | 2 | AmandaLegareFirstSexDone | да | нет |
| `whore_joy` | 2 | slut≥50, not virgin | да | нет |
| `marriage_worry` | 2 | slut<50, not virgin | да | нет |
| `lizette_anal_hint` | 2 | LizaInfluence≥3, anal/Legare anal/slut | да | нет |
| `lizette_oral_practice` | 2 | oral ladder 1→2 | да | oral bump |
| `lizette_balls_hint` | 2 | oral ladder 2→3 | да | oral bump |
| `lizette_atm_clean` | 2 | oral ladder 3→5 + anal talk | да | oral bump |
| `lizette_rim_fair` | 2 | oral ladder 5→6 | да | oral bump |

### Запланировать (следующие итерации текста)

| id | tier | Гейт | Кто говорит |
|----|------|------|-------------|
| `ambient_dress_new` | 0 | IrmaUniform / новая форма у сестёр | обе |
| `ambient_no_panties` | 1 | witness / флаг «без трусов в зале» | Amanda → Lizette |
| `ambient_sleep_naked` | 1 | `SexClothesStage` / домашний peek | Amanda |
| `witness_legare_hall` | 1 | `AmandaLegareInstruction` + ГГ peek major | Amanda |
| `witness_neighbors` | 1 | `EventWitnessed['amanda_neighbors_*']` | Amanda |
| `witness_lewd_hall` | 1 | Hall lewd event + witness | Amanda |
| `stefan_stairs` | 2 | Amanda home stage / ladder event | Amanda |
| `stefan_anal` | 2 | analfromyou≥1, AmandaHomeSex | Amanda |
| `stefan_atm` | 2 | AmandaOralAtmCalmDone / analfromyou≥2 | Amanda |
| `stefan_rim_him` | 2 | AmandaOralStage≥6 | Amanda |
| `stefan_rim_her` | 2 | anilingus stat / rim in scene | Amanda |
| `legare_same_things` | 2 | AmandaLegareFirstSexDone + AmandaHomeSex | Amanda |
| `marathon_exhausted` | 3 | `SexMarathonGossipPending['amanda']`, cooldown 7д | Amanda |
| `lizette_to_amanda_advice` | 0–2 | обратное: Lizette ведёт, те же гейты | Lizette → Amanda |

**Эффекты (без новых глобальных флагов):** `AmandaLizaInfluence`, `Friends['lizette']`, `AmandaOralOnOverhearPhrase` где уже есть; marathon → сброс pending + `AmandaLizaInfluence += 1`.

---

## 5. Sandra + Becky — таблица фраз (план)

Точка: `SundayVisitBeckySandra` (+ опционально пул вне воскресенья — **нет**, только вс).

### Приоритет в `SundayVisitBeckySandraText` (сверху вниз)

1. Gear gossip (церковь) — сюжет  
2. `SandraBeckySundayScandal` — Becky → Sandra, **`BeckyHomeSex = 1`**  
3. Marathon / откровенное — по pending + **`SandraHomeSex = 1`** (Sandra → Becky)  
4. Draupnir gossip — **`PlayerKnows_SandraDraupnirFriday`** / affair stage  
5. **BuildPool** Tier 0–2  
6. Базовый текст (уже есть)

### Фразы пула (id → гейт)

| id | tier | Направление | Гейт |
|----|------|-------------|------|
| `ambient_family_tavern` | 0 | обе | всегда fallback |
| `ambient_sunday_church` | 0 | обе | всегда |
| `becky_two_men` | 1 | Becky → Sandra | `FactHappened['becky_two_men']` + ГГ witness |
| `becky_stefan_gossip` | 2 | Becky → Sandra | **`BeckyHomeSex = 1`** (есть scandal-ветка) |
| `sandra_stefan_marathon` | 3 | Sandra → Becky | pending marathon + **`SandraHomeSex = 1`**, bond≥12, cooldown 7д |
| `sandra_stefan_first` | 2 | Sandra → Becky | **`SandraHomeSex = 1`**, one-shot |
| `sandra_lewd_hall` | 1 | Sandra → Becky | witness hall policy / uniform |
| `sandra_gnome_friday` | 1 | Sandra → Becky | `SandraDraupnirAffairStage` / Friday witness |
| `becky_reverse_comfort` | 0 | Becky → Sandra | bond, без секса |

**Эффекты:** `SandraBeckyBond += 1`, `Friends['becky']` / `Friends['sandra']` у слушателя не нужно — ГГ подслушивает; при желании `FamilyTension` для скандальных tier.

**Не говорить без флага:** про секс со Стефаном — только `*HomeSex` или `FactWitnessed`; про гнома — только после affair/friday флагов.

---

## 6. Melissa + Clarissa (кратко, следующий файл)

Уже есть вставка `MelissaHomeSex` + bond≥12 в `SundayVisitClarissaMelissaText`. Расширить тем же `BuildPool` — отдельная таблица в v2 документа.

---

## 7. Inga + Irma (задел)

Воскресенье, `IrmaShop` закрыта, Инга у двери: bond шитьё, Tier 0–1. Таблица — v2.

---

## 8. Порядок реализации

| Этап | Что | Зависимости |
|------|-----|-------------|
| **A** | SexScene girl cap 8/7/6 + marathon pending/cooldown 7д | нет |
| **B** | Лимиты визитов Lizette (зал 2/нед, комната 1/нед) + гейт `week=7` для room talk | schedule |
| **C** | 5–8 новых id Amanda pool (marathon, uniform, witness_*) | A, факты witness |
| **D** | `SundayVisitBeckySandraBuildPool` + 4–6 id | SandraHomeSex, pending |
| **E** | Melissa+Clarissa pool | MelissaHomeSex |
| **F** | Inga+Irma воскресенье | Inga romance |

**Сейчас (следующий коммит по дизайну):** этап **A** + **B** в коде; тексты **C** пачками по 3–5 id.

---

## 9. Факты для witness (регистрировать при подгляде)

При реализации witness-сцен вызывать `EventKnowledgeRegisterFact` — id для пула:

- `amanda_legare_peek_*`
- `amanda_neighbors_peek_*`
- `amanda_hall_lewd_witness`
- `becky_two_men_witness`
- `sandra_draupnir_friday` (частично есть)

Пул читает `FactHappened[id]` или `EventWitnessed[id]`, не дублировать сотню булевых флагов.