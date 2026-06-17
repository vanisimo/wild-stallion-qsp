# Game State Notes

This file documents important global state so new scenes do not create accidental duplicates.

## Global Setup

- `$RuntimeProfile` - startup profile, usually `dev` or `release`; set in `TraKtir.qsps`.
- `debug` - enables developer output and debug-only actions.
- `debug_images` - enables image debug details.
- `USEHTML` - enables HTML output.
- `$ONGLOAD`, `$ONSTAT`, `$ONOBJSEL` - global QSP handlers.

Owners:

- `TraKtir.qsps` chooses the runtime profile.
- `modules/core/system/game_init.qsps` initializes a new game and derives `debug` / `debug_images`.
- `scripts/build.ps1 -Profile release` changes the profile only in the temporary build source.

## Date And Time

- `day`, `month`, `week`, `year` - current date.
- `time` - current time slot.
- `$MonthName`, `$WeekDay`, `$TimeOfDay` - display names from `GetDateTimeNames`.
- `MonthDays` - temporary result from `GetMonthDays`.

Time slots currently use `1..5`:

- `1` - morning.
- `2` - noon.
- `3` - day.
- `4` - evening.
- `5` - night.

Daily transition owner: `modules/core/time/next_day.qsps`.

`NextDay`:

- applies the previous tavern work day;
- advances date and resets `time` to `1`;
- rolls month/year forward through `AdvanceMonthIfNeeded`;
- resets daily counters and flags;
- updates `tavernvisitors`.

## Player And Daily Limits

- `money` - player money.
- `max_daily_cum` - daily player orgasm limit.
- `daily_cum_count` - current daily count; reset by `NextDay`.
- `cametoday` - legacy daily sex flag; reset by `NextDay`.
- `ChurchDonatedToday` - daily church donation flag; reset by `NextDay`.

Daily intimacy helpers live in `modules/actions/sex`.

## Tavern Economy

Base owner: `modules/core/tavern/tavern_income.qsps`.

Core values:

- `tavernfame` - legacy fame value.
- `tavern_reputation` - normal tavern reputation, clamped to `0..100`.
- `tavern_sex_appeal` - broad appeal/lewdness baseline.
- `tavernvisitors` - visitor count/pressure for the current day.
- `beer_price`, `wine_price`, `food_price` - sale prices.
- `productnum`, `winenum`, `beernum` - food, wine, and beer stock.

Daily calculation values:

- `tavern_food_income`, `tavern_wine_income`, `tavern_beer_income` - income parts.
- `tavern_gross_income` - gross income before daily expenses and city tax.
- `tavern_daily_expenses` - staff/work expenses.
- `tavern_city_tax_today` - city tax for the current calculation (`tavern_gross_income * TaxPercent / 100`).
- `TavernCityTaxTotal` - cumulative city tax paid across the whole game.
- `TaxPercent` - city tax rate on tavern gross income; default `10`, owner `InitBusinessSchedule`.
- `tavern_expected_profit` - final expected daily profit after expenses and city tax.
- `tavern_stock_penalty` - low stock penalty.
- `tavern_food_used`, `tavern_wine_used`, `tavern_beer_used` - stock consumed by the previous work day.
- `tavern_can_serve_food`, `tavern_can_serve_drinks` - service availability flags.
- `tavern_food_staff_mult`, `tavern_drink_staff_mult`, `tavern_rep_mult` - calculation multipliers.

Work capacity values are calculated by tavern/girl job helpers:

- `tavern_waitress_power`
- `tavern_kitchen_power`
- `tavern_cleaning_power`
- `tavern_work_efficiency`
- `tavern_overload_penalty`

`ProcessTavernWorkDay` is the normal daily application path. It updates money, stock, reputation, event bonuses, and accumulates `TavernCityTaxTotal`.

City tax flow:

1. `CalculateTavernIncomePreview` computes gross income and staff expenses.
2. `ApplyTavernCityTaxToProfit` subtracts `tavern_city_tax_today` from `tavern_expected_profit`.
3. `TavernWorkDayEvent` and supply modifiers may change profit further.
4. `AccumulateTavernCityTax` adds `tavern_city_tax_today` to `TavernCityTaxTotal` before money is updated.

Mayor gate target for stage 1: `TavernCityTaxTotal >= 600`.

## Birth Certificate Arc (stage 1 / point 1)

Owners:

- `modules/events/family/birth_certificate_core.qsps`
- `modules/events/family/birth_certificate_text.qsps`
- `modules/locations/rooms/sandra_room.qsps` — chest search
- `modules/locations/town/mayor_office.qsps` — clerk talk

Discovery:

1. `day >= BirthCertificateSearchMinDay` (default `7`).
2. Sandra is not in `SandraRoom`.
3. Not night (`time <> 5`).
4. `BirthCertificateFound = 0`.

Player action: `SandraRoom` → «Осмотреть сундук внимательнее».

Content:

- Father in the record: `$BirthCertificateFatherName` (default `Томас Лермонт`), `$BirthCertificateFatherTitle` (default `дворянин`).
- Not Longcock; registration seal field is empty.

After read:

- `BirthCertificateFound = 1`, `BirthCertificateRead = 1`.
- Knowledge id: `Stefan_BirthCertificateFound_1`.
- `FamilyTension += 2`.

Mayor hook:

- `MayorOffice` → «Показать клерку свидетельство о рождении».
- Clerk explains: magistrate will reject without seal; need mayor audience first.

Debug: `DebugBirthCertificateArcPanel`.

## Tavern Upgrades / Draupnir (stage 1 / PR3)

Owners:

- `modules/core/tavern/tavern_upgrades.qsps`
- `modules/locations/shops/draupnir_upgrades.qsps`
- `modules/locations/shops/draupnir_upgrades_text.qsps`
- `modules/events/family/melissa_music_stage.qsps`
- `modules/locations/town/craftsmen_quarter.qsps`

Unlock: `TavernCarpenterUpgradesUnlocked = 1` (from mayor clerk workoff in PR4b; debug can force).

Rules:

- Pay immediately; work completes after N days via `TavernUpgradeAdvanceDay` in `NextDay`.
- No tavern closure or power penalty while work is pending.
- **Sign first** (`TavernUpgradeSignDone`); other Draupnir upgrades require sign done, any order after that.
- **Music stage** only after Melissa musician branch (below) sets `MelissaMusicStageOfferDone = 1`. Not in clerk checklist.

| Upgrade | Cost | Days | Effect when done |
|---------|------|------|------------------|
| sign | 120 | 1 | rep +3, visitors +2 |
| exterior | 200 | 2 | rep +5, softer bad day-events |
| kitchen | 180 | 2 | kitchen power +8 |
| bar | 150 | 1 | waitress power +5, drink income +5% |
| cellar | 100 | 1 | rat food loss −30% |
| doors | 90 | 1 | 35% brawl without repair flag |
| lamp | 70 | 1 | evening visitors +1 |
| stage | 250 | 3 | Friday beer +10%, minstrels event bonus, `MelissaMusicianInterest +2` |

Emergency repair (`TavernRepairNeeded`) stays separate from permanent upgrades.

Debug: `DebugTavernUpgradesPanel`.

## Melissa Musician Branch (planned / scaffold)

Owners:

- `modules/events/family/melissa_musician_arc.qsps` — flags and gates
- `modules/events/family/melissa_musician_arc_text.qsps` — texts (stage talk only so far)
- `modules/events/family/melissa_music_stage.qsps` — stage talk scene

Order (all required before stage talk):

1. `MelissaDanceDressReady` — dance dress ready (Irma / family; **TODO**).
2. `MelissaFridayDanceAttended` — Melissa at Friday dances in dress (**TODO**).
3. `MelissaMinstrelMet` — meet travelling minstrel (**TODO**).
4. `MelissaMinstrelKissDone` — kiss after dance (**TODO**).
5. `MelissaMusicStageOfferDone` — talk about tavern stage (`MelissaMusicStageTalk`).
6. Order stage at Draupnir (`TavernUpgradeStageDone`).
7. `MelissaMinstrelAffairStage` — minstrel continues with Melissa (**TODO**, separate events).

`MelissaMusicStageCanOffer` uses `MelissaMusicianArcCanOfferStageTalk` — no early unlock by friendship alone.

Personal story `melissa_musician` in `girl_talk_personal` is a later confession, not the stage gate.

## Mayor Office Gate (stage 1)

Owners:

- `modules/locations/town/mayor_office.qsps`
- `modules/locations/town/mayor_office_text.qsps`
- `modules/locations/town/street.qsps` — link to `MayorOffice`
- `modules/core/time/business_schedule.qsps` — `IsMayorOfficeOpen`

Schedule: Wednesday and Thursday, noon or day (`time = 2 or 3`).

Flow (stage 1 main arc):

1. `BirthCertificateRead = 1` — свидетельство найдено.
2. Pay tavern tax until `TavernCityTaxTotal >= MayorCityTaxGate` (default `600`).
3. `MayorOffice` → «Просить приём у мэра» → pay `MayorAudienceBribe` (default `180`). Money is **not** refunded.
4. Mayor refuses (`MayorAudienceRefused = 1`, `MayorFirstTalkDone` stays `0`).
5. Player demands refund → clerk helps (`MayorOfficeClerkRefundTalk` → `MayorOfficeClerkAdviceTalk`): narrative advice, not a UI checklist.
6. Advice sets `MayorClerkAdviceGiven = 1`, `TavernCarpenterUpgradesUnlocked = 1`, `MayorClerkMentionedStaff = 1`.
7. Later (when work is done): mayor accepts — `MayorFirstTalkDone = 1` (**TODO** completion gate).
8. Magistrate submit blocked until `MayorFirstTalkDone = 1`.

Key state:

- `MayorCityTaxGate`, `MayorAudienceBribe`
- `MayorBribePaid`, `MayorAudienceRefused`, `MayorClerkAdviceGiven`, `MayorClerkMentionedStaff`
- `MayorFirstTalkDone` — only after future acceptance, not after bribe

Knowledge ids: `Stefan_MayorClerkAdvice_1`, later `Stefan_MayorFirstTalk_1`.

Debug: `DebugMayorArcPanel` (debug panel).

## Hired Staff (stage 1 / PR2)

Owner: `modules/core/tavern/tavern_hired_staff.qsps`.

Unlock (`CheckTavernHiredStaffUnlocked`):

- `MelissaStaffHired = 1` — after mother hires staff (main arc point 3, **TODO**). Clerk only mentions this in advice until then.

Until unlock, hire buttons are hidden. If unlock is lost before hire (should not happen in normal play), active hires are cleared in `ApplyTavernHiredStaffEffects`.

Flags:

- `TavernHiredKitchen`, `TavernHiredWaitress`, `TavernHiredCleaning` — `0/1` per role.

Power added to daily staff calculation:

- kitchen `28`, waitress `25`, cleaning `22`.

Daily cost (included in `tavern_daily_expenses`):

- kitchen `12`, waitress `12`, cleaning `10`.

Overload relief: `-5` penalty per active hired worker.

UI: `PanelStaffInfo` → block `PanelHiredStaffBlock`, toggle via `PanelHiredStaffToggle`.

## Last Day Summary

Owner: `modules/core/time/next_day.qsps`.

These values mirror the previous work day for the morning summary:

- `LastDayProfit`
- `LastDayGrossIncome`
- `LastDayFoodIncome`
- `LastDayWineIncome`
- `LastDayBeerIncome`
- `LastDayExpenses`
- `LastDayCityTax`
- `LastDayHiredStaffCost`
- `LastDayFoodUsed`
- `LastDayWineUsed`
- `LastDayBeerUsed`
- `LastDayWorkEfficiency`
- `LastDayOverloadPenalty`
- `LastDayStockPenalty`
- `$LastDayTavernEventText`
- `LastDayEventProfitBonus`
- `LastDayEventReputationBonus`

## Supply Economy

Owner: `modules/core/economy/tavern_supply_economy.qsps`.

Persistent supply state:

- `TavernSupplyEconomyInited` - soft init marker.
- `TavernSupplyCostLevel` - supplier price pressure level.
- `TavernDailyCostBonus` - flat daily supply cost.
- `TavernSupplyPenalty` - disruption penalty level.
- `TavernAlcoholShortage` - wine/beer shortage flag.
- `TemporaryAlcoholSuppliers` - temporary expensive supplier flag.
- `ClarissaWineRouteUnlocked` - wine route relief flag.
- `ClarissaBeerRouteUnlocked` - beer route relief flag.

Calculation values from `ApplyTavernSupplyEconomyModifiers`:

- `TavernSupplyProfitBefore`
- `TavernSupplyProfitResult`
- `TavernSupplyCostLoss`
- `TavernDailyCostLoss`
- `TavernAlcoholShortageLoss`
- `TavernSupplyPenaltyLoss`
- `TavernTemporarySupplierLoss`
- `TavernClarissaRouteSave`
- `TavernSupplyTotalLoss`
- `$TavernSupplyEconomyReport`

## Tavern Event State

Owner: `modules/core/tavern/tavern_event_state_core.qsps`.

Global tavern scales:

- `TavernReputation` - event-system reputation, clamped to `0..100`.
- `TavernScandal` - scandal level, clamped to `0..100`.
- `TavernLewdFame` - late lewd reputation, clamped to `0..100`.
- `TavernGirlsEasyRumor` - binary rumor that girls are available.
- `TavernBackroomRumor` - binary backroom/private corner rumor.
- `TavernKitchenRumor` - binary kitchen rumor.

Per-girl tavern arrays:

- `GirlWorkPolicy[girl]` - hall policy: `0` none, `1` decent/call Stefan, `2` decide herself, `3` keep client for tips.
- `GirlKitchenPolicy[girl]` - kitchen policy: `0` none, `1` call Stefan/decent, `2` decide herself, `3` keep client at any cost.
- `GirlUniformLevel[girl]` - `0` normal uniform, `1` revealing uniform.
- `GirlHallLewdStage[girl]` - hall lewd progression, clamped to `0..4`.
- `GirlPublicAttention[girl]` - public attention, clamped to `0..100`.
- `GirlNpcPath[girl]` - NPC-facing path pressure, clamped to `0..100`.
- `GirlSecretiveness[girl]` - secrecy, clamped to `0..100`.
- `GirlRebellion[girl]` - rebellion, clamped to `0..100`.
- `GirlTrustStefan[girl]` - trust in Stefan, clamped to `0..100`.

Use `ClampTavernEventState` after changing these values.

## Characters

- `$AllGirlNames` - central ordered list of girl ids, initialized by `InitGirlsRegistry`.
- Character base data is initialized through `GirlsInitAll` and `GirlInitBase`.
- `$RealName[person]`, `$RealName2[person]`, `$RealName3[person]` - display names/cases.
- `age[person]`, `beauty[girl]`, `attractiveness[guy]`, `Friends[person]`, `otkroven[person]` - core character values.
- `$CurrentLoc[person]` - current location key.

Important girl ids currently used across tavern systems:

- `amanda`
- `melissa`
- `sandra`
- `inga`
- `becky`
- `clarissa`

When adding a new girl to tavern/hall systems, make sure the relevant init/clamp helpers include her where needed.

## Hall Memory And Family State

Recent hall memory owner: `modules/events/hall/hall_recent_memory.qsps`.

- `$LastHallMemoryGirl`
- `$LastHallMemoryType`
- `$LastHallMemoryPlace`
- `LastHallMemorySeverity`
- `LastHallMemoryDay`
- `LastHallMemoryTime`
- `LastHallMemoryDiscussed`
- `HallMemoryCount[girl]`
- `HallMemorySeriousCount[girl]`
- `HallMemoryDirtyCount[girl]`

Choice memory owner: `modules/events/hall/hall_choice_memory.qsps`.

- `$LastHallChoiceEvent`
- `$LastHallChoiceChoice`
- `$LastHallChoiceType`
- `$LastHallChoiceGirl`
- `$LastHallChoiceArea`
- `LastHallChoiceDay`
- `LastHallChoiceTime`
- `HallChoiceTotal`
- `HallChoiceByEvent[event]`
- `HallChoiceByGirl[girl]`
- `$LastGirlChoiceEvent[girl]`
- `$LastGirlChoiceChoice[girl]`
- `$LastGirlChoiceType[girl]`
- `$LastGirlChoiceArea[girl]`
- `LastGirlChoiceDay[girl]`
- `LastGirlChoiceTime[girl]`
- `HallChoiceProtectTotal`, `HallChoiceNeutralTotal`, `HallChoiceDirtyTotal`, `HallChoiceControlTotal`
- `HallChoiceProtectByGirl[girl]`, `HallChoiceNeutralByGirl[girl]`, `HallChoiceDirtyByGirl[girl]`, `HallChoiceControlByGirl[girl]`

Family state owner: `modules/events/hall/hall_family_state.qsps`.

- `FamilyTrust` - family trust, clamped to `0..100`.
- `FamilyTension` - family tension, clamped to `0..100`.
- `FamilyCorruptionPoints` - accumulated corruption pressure, clamped to `0..100`.
- `FamilyCorruptionStage` - derived stage, clamped to `0..5`.
- `HallFamilyStateLastApplied`
- `$HallFamilyStateLastEvent`
- `$HallFamilyStateLastGirl`
- `$HallFamilyStateLastChoice`
- `HallFamilyStateLastTrustDelta`
- `HallFamilyStateLastTensionDelta`
- `HallFamilyStateLastCorruptionDelta`

Use `HallFamilyStateApply` for new hall/kitchen consequences instead of changing family state directly.

## Context Girl Talk Hooks

Owners:

- `modules/actions/dialogs/girl_talk_family.qsps`
- `modules/actions/dialogs/girl_talk_tavern.qsps`

These topics add short context paragraphs to the main `family` and `tavern` talk options in `GirlTalkResult`.

Hook flags are keyed by `girl + '_' + day`:

- `GirlTalkFamilyHallHookDiscussed[key]` - family talk already referenced today's hall choice.
- `GirlTalkTavernHallHookDiscussed[key]` - tavern talk already referenced today's hall choice.
- `GirlTalkTavernDayHookDiscussed[key]` - tavern talk already referenced `$LastDayTavernEventText`.

These flags do not replace the dedicated hall-topic menu. Full follow-up scenes such as `HallChoiceFamilyTalk` and `HallRecentTalk` keep their own `*Discussed` flags.

## Personal Girl Talk

Owner: `modules/actions/dialogs/girl_talk_personal.qsps`.

The `Личный разговор` menu item appears only when:

- `otkroven[girl]` is high enough for that girl;
- at least one personal story is unlocked and not yet discussed.

Menu visibility thresholds:

- `amanda` - `otkroven >= 14`
- `melissa` - `otkroven >= 16`
- `sandra` - `otkroven >= 18`

Story keys and per-story `otkroven` minimums:

- `amanda_legare` - 14
- `amanda_boys` - 18
- `melissa_musician` - 16
- `sandra_carpenter` - 18
- `sandra_priest` - 20

State:

- `GirlPersonalStoryDiscussed[story_key]` - girl already told this confession to Stefan.
- `GirlPersonalStoryUnlock[story_key]` - future-event hook for stories not yet wired into gameplay.

Unlock sources:

- Amanda / Legare: `Fact_AmandaLegareOutsideMeet`, `Fact_AmandaLegareMajorRisk`, `Fact_AmandaLegarePrivateTalk`, `AmandaNpcPath >= 12`, or matching `FactHappened` ids.
- Amanda / boys: `HallMissingGirlPrivateCount['amanda'] >= 1`, `sluttiness['amanda'] >= 22`, or `GirlNpcPath['amanda'] >= 22`.
- Melissa / musician: `GirlPersonalStoryUnlock['melissa_musician']` or `FactHappened['melissa_musiciannotice_1']`.
- Sandra / carpenter: `GirlPersonalStoryUnlock['sandra_carpenter']` or `FactHappened['sandra_carpentersecret_1']`.
- Sandra / priest: `GirlPersonalStoryUnlock['sandra_priest']` or church complaint facts.

Each chosen story counts as one useful `personal` talk through `npc_talk_limits.qsps`.

## Tavern Day Events (neutral)

Owner: `modules/events/tavern/tavern_day_events.qsps`.

Macro events roll in `TavernDailyUpdate` after `NextDay` (not on Friday/Sunday). Replaces legacy `daily_tavern_events.qsps` girl rolls.

Roll chance: 25% on eligible weekdays (not Friday/Sunday).

Current events:

- `caravan` — profit+, visitors+, staff busy all day, tired in evening.
- `rats` — stock loss, repair needed, optional evening brawl if unrepaired.
- `brawl` — profit-, reputation-, repair needed (bar damage).
- `guard` — pass if `tavern_reputation >= 55` and `tavern_cleaning_power >= 35`, else fine.
- `harvest` — profit+, visitors+, reputation+.
- `minstrels` — profit+, visitors+, light festive mood.
- `storm` — fewer visitors; small profit if reputation is decent.
- `pilgrims` — profit-, reputation+.
- `broken` — beer/wine stock loss, repair needed.
- `thief` — food/wine stock loss, profit-, reputation-.

Repair: `CraftsmenQuarter` → `TavernDayEventCarpenterRepair` when `TavernRepairNeeded = 1`.

Key state:

- `$TavernDayEventId`, `TavernDayEventActive`
- `TavernStaffBusyDay`, `TavernStaffTiredEvening` (caravan only)
- `TavernRepairNeeded`, `TavernRepairOrdered`, `$TavernRepairSource` (`rats` / `brawl` / `broken`)
- `TavernDayEventGuardPassed`
- `TavernDayEventProfitBonus`, `TavernDayEventReputationBonus`
- `TavernDayBrawlHappened` (rats evening only)
- `TavernDayEventImageShown`, `TavernDayEventHallDescPrinted`

Images: `modules/events/tavern/tavern_day_event_images.qsps`

- folder `images/events/tavern/day/`
- keys include: `caravan_morning`, `rats_storage`, `rats_brawl`, `hall_brawl`, `guard_inspection`, `harvest_festival`, `minstrels_hall`, `storm_outside`, `pilgrims_hall`, `broken_barrel`, `cellar_thief`, `carpenter_repair`
- debug briefs print when `debug = 1` or `debug_images = 1`

Hall girl scenes stay in `tavern_event_dispatcher.qsps`.

## Knowledge And Rumors

Owner: `modules/core/knowledge/event_knowledge_system.qsps`.

- `FactHappened[event]` - event happened.
- `FactDay[event]`, `FactTime[event]` - event timestamp.
- `PlayerKnows[event]` - player knows event.
- `PlayerKnowledgeDay[event]`
- `$PlayerKnowledgeSource[event]` - source such as `rumor`, `witness`, `confession`, `talk`, or `peek`.
- `EventRumor[event]`, `EventRumorPower[event]`, `EventRumorLastDay[event]`, `EventRumorStrong[event]`
- `EventWitnessed[event]`
- `EventWitness[witness_event]`, `EventWitnessDay[witness_event]`
- `EventConfessed[event]`, `EventConfessionDay[event]`
- `NpcSuspects[npc_event]`, `NpcSuspicionDay[npc_event]`
- `NpcKnows[npc_event]`, `NpcKnowledgeDay[npc_event]`, `$NpcKnowledgeSource[npc_event]`
- `CityRumorTotal`

Preferred API names use the `EventKnowledge*` prefix. Legacy aliases live in `modules/core/system/compatibility_aliases.qsps`.

## Kitchen Customer Event

Owner: `modules/events/kitchen/kitchen_customer_event.qsps`.

- `KitchenCustomerEventDisabled` - disables the event.
- `KitchenCustomerEventCanStart` - result from availability check.
- `$KitchenCustomerSelectedGirl` - candidate selected by `KitchenCustomerPickCandidate`.
- `KitchenCustomerCandidateCount`, `$KitchenCustomerCandidate[index]` - temporary candidate list.
- `KitchenCustomerLastDay[girl]` - per-girl daily cooldown.
- `KitchenCustomerLastGlobalDay`, `KitchenCustomerLastGlobalTime` - global cooldown.
- `$KitchenCustomerGirl`, `$KitchenCustomerScene`, `$KitchenCustomerClient` - active scene state.
- `KitchenCustomerStage`, `KitchenCustomerChance` - selection/progression calculation values.

## Daily Resets

`NextDay` currently resets or refreshes:

- `daily_cum_count`
- `cametoday`
- `ChurchDonatedToday`
- daily girl flags via `GirlsResetDailyFlags`
- sex daily flags via `ResetSexDailyFlags`
- tavern bar work flags via `ResetTavernBarWorkDailyFlags`
- visitor pressure via `TavernDailyUpdate`

`GirlsResetDailyFlags` includes:

- `HarassToday['amanda'|'melissa'|'sandra']`
- `AmandaVar['askzalettoday']`
- `MelissaVar['MomDressComplaint']`
- `SandraVar['knowmolodost']`
- `becky_children_bought_today`
- `clarissa_bought_today`
- `IngaDanceRefused`
- `IngaGuardIgnored`

## Compatibility State

Owner: `modules/core/system/compatibility_aliases.qsps`.

This file keeps old location names callable while active scenes are being migrated to newer systems. Prefer new owner APIs in new code.

Active compatibility bridges still used by current systems:

- `KnowledgeRegisterFact` redirects to `EventKnowledgeRegisterFact`.
- `HallChoiceMemorySave` redirects to `HallChoiceMemoryRegister`.
- `HallChoiceConsequencePrint` redirects to `HallChoiceConsequencesApply`.
- `GirlPolicyResponseEvaluate` redirects to `GirlPolicyResponseCalc`.
- `DailyAftermathPrintMorning` is called from `NextDay`.

Legacy bridges and placeholders:

- `AdvanceTimePart`, `NextTimePart`, and `ProcessNewDay` bridge old time calls.
- openness milestone locations such as `AmandaOtkroven45` route to `OtkrovenMilestoneStub`;
- missing NPC talks such as `TalkWithEddie` route to `TalkWithNpcStub`.

Compatibility cleanup rule:

- Do not delete an alias while it has active callers.
- New code should prefer the owner location directly.
- If an alias becomes a public bridge, document it here and group it in `compatibility_aliases.qsps`.
- If an alias is only a placeholder, keep it grouped as legacy until the real scene exists.

## Maintenance Rule

When adding a new global variable:

- add it to the owner module's init/clamp/reset helper when appropriate;
- add a one-line note here with the owning module and intended meaning;
- prefer arrays keyed by stable ids such as `amanda` or `hall_missing`;
- avoid creating a second variable for the same concept under a slightly different name.
