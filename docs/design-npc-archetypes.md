# Типажи NPC для диалогов и поведения

**Статус:** канон согласован (2026-06-19).  
**Связь:** `AGENTS.md`, `docs/design-stefan-voice.md`, `docs/design-port-church-arc.md`, `docs/import-traktir-legacy.md`, `docs/design-character-intimacy-arc.md`.

---

## Главный герой

**Стефан Лонгкок** — отдельный канон голоса и границ: [`docs/design-stefan-voice.md`](design-stefan-voice.md).

Кратко: молодой бывший раздолбай, грубовато-шутливый; в Act 1 **ещё не раскован** — пробует границы; женщины смотрят иначе, но он **не умеет** этим пользоваться; рад наследству; алкоголь — фон; дружелюбен, но **не отдаёт своё** без убеждения.

---

## Пять полей типажа

Каждый NPC для сценариста и кода описывается пятью полями:

| Поле | Вопрос | Пример |
|------|--------|--------|
| **Роль** | Какую функцию несёт в сюжете? | «мать-прагматик порта» |
| **Драйвер** | Чего хочет / чего боится? | «дочь не слушает; деньги на детей» |
| **Голос** | Как говорит? | насмешливо, устало, с материнской жёсткостью |
| **Граница** | Что не делает в Act 1–2? | не лезет в семью Лонгкоков без повода |
| **Темп** | Как быстро открывается? | медленно через порт → церковь → подворотня |

Маска (T1–T12) — **ярлык для меню и тона**, не единственная черта персонажа.

---

## Двенадцать масок (T1–T12)

| Код | Маска | Суть | Типичный голос |
|-----|-------|------|----------------|
| T1 | Хранительница | мораль, дом, «так принято» | спокойно, требовательно |
| T2 | Контролёр | порядок, риски, ревность к хаосу | сжато, тревожно |
| T3 | Бунтарка | тоска по другой жизни | вспышки, потом стыд |
| T4 | Вдова-прагматик | выживание без иллюзий | тепло + расчёт |
| T5 | Спасаемая | нуждается в защите / выборе ГГ | робко → благодарно |
| T6 | Ревнивая союзница | дружба + укол ревности | «я же предупреждала» |
| T7 | Хищник-статус | власть, статус, чужие девушки | уверенно, с улыбкой |
| T8 | Катализатор | приносит искушение и связи | лёгко, остро |
| T9 | Наблюдатель | видит город, мало судит | коротко, точно |
| T10 | Лицемер | публичная маска ≠ ночная жизнь | в церкви смиренно |
| T11 | Соперник | конкурирует с ГГ за влияние | холодно или насмешливо |
| T12 | Фон семьи | упоминания, задел, без своего меню | в чужих репликах |

---

## Согласованные решения (канон)

### Грета — T12, фон

- **Маска:** T12 (фон семьи).
- **Меню:** отдельного `GirlTalk` **нет**; только упоминания через Бекки, церковь, будущую арку.
- **Арка:** позже, опираясь на legacy (сестра Бекки, «непутевая»).
- **Код:** не роутить в `GirlTalkBuildTownMainMenu`; при прямом вызове — только `smalltalk`.

### Жоржетта — отдельное меню, legacy-истории

- **Маски:** T4 (прагматик порта) + T10 (церковное лицемерие) + T8 (катализатор для Лизетты).
- **Меню:** `GirlTalkBuildGeorgetteMainMenu` — **не** generic town.
- **Источник тем:** `docs/design-port-church-arc.md` § IntGeorgettTalk; тексты — адаптация legacy, без трактир-проституции и glory hole.
- **Файлы:** `girl_talk_georgette.qsps`, `girl_talk_georgette_text.qsps`; события порта — `modules/events/georgette/`.

### Альбер (Легаре) — три фазы

| Фаза | Условие (черновик) | Маска | Поведение в talk |
|------|-------------------|-------|------------------|
| **1. Усталый отец** | по умолчанию | T4 + оттенок T7 | дети от первого брака, лавка, Кларисса, усталость |
| **2. Хищник** | до примирения с ГГ; `LegareConflictStage` / арка Аманды | T7, T11 | интерес к Аманде — **сюжетные act**, не болтовня |
| **3. Наставник** | после примирения (`LegareReconciledWithStefan = 1`) | T7 → старший друг | совет по торговле, городу, семье; без токсичного тона legacy 1:1 |

- **Меню:** `TalkWithAlber` (как `TalkWithBecky`), не `GirlTalk`.
- **Legacy:** `docs/legacy-text-extracts/clarissa/IntAlberTalk.legacy.txt` — помириться / обругание — адаптировать под фазу 3, не копировать грубость дословно.

---

## Таблица NPC → маска → меню → шкалы

| NPC | Ключ | Маска | Меню talk | Главные шкалы / флаги |
|-----|------|-------|-----------|------------------------|
| Сандра | `sandra` | T1, T10 | `GirlTalkBuildSandraMainMenu` | `SandraTrust`, `SandraMoralResistance`, `SandraPragmatism` — голос: [`design-npc-voices.md`](design-npc-voices.md) §1 |
| Мелисса | `melissa` | T2, T6 | универсальный трактир | `MelissaControlNeed`, `MelissaJealousy` — голос: [`design-npc-voices.md`](design-npc-voices.md) §3 |
| Аманда | `amanda` | T3, T5 | универсальный + act Легаре | `AmandaRebellion`, `AmandaLegareInterest` — голос: [`design-npc-voices.md`](design-npc-voices.md) §2 |
| Бекки | `becky` | T4 | `TalkWithBecky` | `BeckyHomeStage`, `HusbandStory` — голос: [`design-npc-voices.md`](design-npc-voices.md) §11 |
| Инга | `inga` | T4, T9 | `GirlTalkBuildIngaMainMenu` | `IngaRomanceUnlocked` — голос: [`design-npc-voices.md`](design-npc-voices.md) §10 |
| Кларисса | `clarissa` | T4, T6 | `GirlTalkBuildClarissaMainMenu` | `ClarissaTrustStefan`, `ClarissaJealousy` — голос: [`design-npc-voices.md`](design-npc-voices.md) §12 |
| Лизетта | `lizette` | T8 | `GirlTalkBuildLizetteMainMenu` | `AmandaLizaInfluence`, `Friends` — голос: [`design-npc-voices.md`](design-npc-voices.md) §13 |
| Ирма | `irma` | T9, T10 | `GirlTalkBuildIrmaMainMenu` | `Friends`, `otkroven`, пороги лавки — голос: [`design-npc-voices.md`](design-npc-voices.md) §14 |
| **Жоржетта** | `georgett` | T4, T10, T8 | **`GirlTalkBuildGeorgetteMainMenu`** | `GeorgetteKnown`, `GeorgettePortSexDone` — голос: [`design-npc-voices.md`](design-npc-voices.md) §15 |
| **Грета** | `greta` | **T12** | stub (`GirlTalkBuildGretaStubMenu`) | — — голос: [`design-npc-voices.md`](design-npc-voices.md) §18 |
| Жюльетта | `juliette` | T9 | `GirlTalkBuildTownMainMenu` | `Friends` — голос: [`design-npc-voices.md`](design-npc-voices.md) §17 |
| **Альбер** | `alber` | T4 → T7 → наставник | **`TalkWithAlber`** | `Friends['alber']`, `LegareReconciledWithStefan`, `LegareConflictStage` — голос: [`design-npc-voices.md`](design-npc-voices.md) §16 |
| **Отец Герхард** | `gerhard` | T10, T7, T11 | `TalkWithGerhard` (stub → церковь) | `PriestConfessionCorruption`, пожертвования — голос: [`design-npc-voices.md`](design-npc-voices.md) §4 |
| Эдди | `eddie` | зависть, куртуаз | `TalkWithEddie` | `EddieSawGeorg`, `EddieBestFriend` — голос: [`design-npc-voices.md`](design-npc-voices.md) §5 |
| **Драупнир** | `draupnir` | T4, «свекор» | мастерская, пятница | `SandraDraupnirAffairStage` — голос: [`design-npc-voices.md`](design-npc-voices.md) §6 |
| **Мэр** | `mayor` | T7, T11 | `MayorOffice` | `MayorFirstTalkDone`, налоги — голос: [`design-npc-voices.md`](design-npc-voices.md) §7 |
| **Грюн** | `grun` | T7, порядок | ивенты лавки/трактира | `IngaGuardBribed` — голос: [`design-npc-voices.md`](design-npc-voices.md) §8 |
| **Тайефер** | `taiefer` | T8, романтик | трактир, пятница | `MelissaMusicianInterest` — голос: [`design-npc-voices.md`](design-npc-voices.md) §9 |

---

## Темы Жоржетты (полезные разговоры)

| Тема | Ключ | Гейт |
|------|------|------|
| Порт и корабли | `georgette_port` | `GeorgetteKnown = 1` |
| Лизетта | `georgette_lizette` | `LizetteMentionedByGeorgette = 1` или `PortMeetWitnessed = 1` |
| Биография | `georgette_bio` | `GeorgetteKnown = 1` |
| Клиенты | `georgette_clients` | `Friends['georgett'] >= 14` |
| Церковь | `georgette_church` | `GeorgettePortSexDone = 1` |
| Эдди | `georgette_eddie` | `Friends['georgett'] >= 18`, `EddieSawGeorg >= 1` |

Болтовня (`smalltalk`) и комплимент — вне лимита полезных разговоров.

---

## Темы Альбера (фаза 1 и 3)

| Тема | Ключ | Гейт |
|------|------|------|
| Дети и лавка | `alber_shop` | всегда в лавке |
| Дом и Кларисса | `alber_home` | `Friends['alber'] >= 6` |
| Лизетта | `alber_lizette` | witness / `LizetteKnown` (фаза 1–2, без хищничества в тексте) |
| Совет наставника | `alber_mentor` | `LegareReconciledWithStefan = 1` |
| Помириться | act в меню | конфликт с ГГ (будущая арка) |

---

## Связь типаж → код

1. **Маска** задаёт тон в `*_text.qsps`.
2. **Меню** — отдельный билдер или редирект (`becky`, `georgett`, `alber`).
3. **Полезные темы** регистрируются в `npc_talk_limits.qsps` → `GirlTalkTopicIsUseful`.
4. **Сюжетные кнопки** остаются `act` в `girl_talk.qsps` или event-файлах, не дублируют меню.

---

## Чеклист реализации

- [x] Канон: Грета T12, Жоржетта отдельное меню, Альбер три фазы
- [x] `girl_talk_georgette.qsps` + тексты
- [x] `talk_with_alber.qsps` (фаза 1 + задел фазы 3)
- [x] Этап B Жоржетты — поиск дочь + ночной порт (`design-port-church-arc.md` §B)
- [x] Этап C Жоржетты — служба, меню прихожан, секс в соборе (`design-port-church-arc.md` §C)
- [ ] Этапы D–G Жоржетты — исповедь, spy, Лизетта на службе, подворотня  
  **Контрольная точка теста:** этапы **A–C** готовы (`DebugPortChurchArcPanel` при `debug=1`)
- [x] Примирение с Альбером + флаг `LegareReconciledWithStefan`
- [ ] Арка Греты (отдельный этап; stub `GirlTalkBuildGretaStubMenu` готов)