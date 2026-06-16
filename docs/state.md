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
- `tavern_gross_income` - gross income before daily expenses.
- `tavern_daily_expenses` - staff/work expenses.
- `tavern_expected_profit` - final expected daily profit.
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

`ProcessTavernWorkDay` is the normal daily application path. It updates money, stock, reputation, and event bonuses.

## Last Day Summary

Owner: `modules/core/time/next_day.qsps`.

These values mirror the previous work day for the morning summary:

- `LastDayProfit`
- `LastDayFoodIncome`
- `LastDayWineIncome`
- `LastDayBeerIncome`
- `LastDayExpenses`
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
- `$LastHallChoiceGirl`
- `LastHallChoiceDay`
- `LastHallChoiceTime`
- `HallChoiceTotal`
- `HallChoiceByEvent[event]`
- `HallChoiceByGirl[girl]`
- `$LastGirlChoiceEvent[girl]`
- `$LastGirlChoiceChoice[girl]`
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
