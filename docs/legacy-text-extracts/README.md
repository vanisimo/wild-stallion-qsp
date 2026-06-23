# Legacy text extracts (`traktr_old.txt`)

**Источник:** `E:\Games\Albedo\Traktir Wild Stallion 0.05\traktr_old.txt`
**Кодировка:** UTF-16 LE

Полные фрагменты локаций для PR-I. Статус переноса — см. `design-character-intimacy-arc.md` §Сверка.

| Папка | Локации |
|-------|---------|
| `becky/` | InitBecky, IntBeckyTalk, IntBeckyDance, BeckyInviteHome, BeckyHomeFront, BeckyHome, IntBeckyGuest, IntBeckySex, BeckyLoversInStore, IntBeckyDressChange, BeckyQuestInit, IntBeckyTalkSherwood |
| `eddie/` | IntEddieTalk, BeckyEddieJoinFirst, IntEddieBeckySex, GeorgettBeckyVisit |
| `becky_church/` | IntBeckyAfterCermon, ChurchAfterCermon |
| `amanda/` | InitAmanda, IntAmandaTalk, IntAmandaDance, IntAmandaDressChange, IntAmandaSex, AmandaSexDanceStreet, AmandaLoverSex, AmandaLegareDanceSequence, AfterDanceSexLegare, AfterDanceLegare, TavernAmandaRoom, AmandaAtHomeCode |
| `melissa/` | InitMelissa, IntMelissaTalk, IntMelissaDressChange |
| `sandra/` | InitSandra, IntSandraTalk, IntSandraDressChange |
| `inga/` | InitInga |
| `clarissa/` | IntAlberTalk |
| `lizette/` | InitLiza, IntLizaTalk, IntLizaDressChange, IntLizaSex, IntLizettAfterCermon, EventAmandaLizettTalk, EventAmandaLizettTalk2, InitAmandaLizaTalkItems |
| `town_npcs/` | IntRobinTalk, IntZimmerTalk, FrancheskaTalk, EventAmandaLegareCreateDance |
| `cut_reference/` | AmandaAtGloryHole, SexProstTavern |

## Статусы (ключевые)

| Локация | Решение |
|---------|---------|
| `AmandaAtGloryHole` | CUT |
| `AmandaSexDanceStreet` | ADAPT — заменено amanda_dark_alley event |
| `BeckyEddieJoinFirst` | TAKE — упростить до 2–3 шагов |
| `BeckyHome` | TAKE |
| `BeckyHomeFront` | TAKE — только Инга+Лукас |
| `BeckyInviteHome` | TAKE |
| `BeckyLoversInStore` | ADAPT — моряки DP |
| `ChurchAfterCermon` | ADAPT — разбить на church_spy_* |
| `GeorgettBeckyVisit` | CUT — оргия за столом, не в v1 |
| `IntAmandaDance` | PARTIAL — уже amanda_dance.qsps |
| `IntAmandaDressChange` | TAKE — самопокупка д.28 |
| `IntBeckyAfterCermon` | TAKE — укороченно, ongoing Бекки |
| `IntBeckyDance` | TAKE — becky_dance.qsps |
| `IntBeckyGuest` | TAKE — ужин укороченный |
| `IntBeckySex` | ADAPT — SexSceneStart |
| `IntBeckyTalk` | TAKE — слить в talk_with_becky |
| `IntBeckyTalkSherwood` | CUT — Шервуд, опционально позже |
| `IntEddieBeckySex` | CUT menu — только narrative 2–3 шага |
| `IntEddieTalk` | TAKE |
| `IntMelissaDressChange` | TAKE — самопокупка д.35 |
| `SexProstTavern` | CUT — порт вместо трактира |
