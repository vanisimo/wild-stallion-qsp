# Archive

Old code kept for reference **outside** the active QSP build (`qsp-project.json` only connects `modules/*`).

Before restoring anything from here, check whether a newer module already replaced it.

## Layout

- `archive/old/` — disabled modules moved out of `modules/`
- nested paths mirror former module paths when useful

## Moved dead / legacy (2026-07-17)

Whole files with **no** `gt`/`gs`/`LOC` callers in the active tree (or already marked LEGACY):

| Former path | Locations | Notes |
|-------------|-----------|--------|
| `modules/events/market/market_events.qsps` | `MarketRandomEvents`, `MarketEvent_*` | Never hooked from `#Market` |
| `modules/events/tavern/daily_tavern_events.qsps` | `DailyTavernEvents` | Replaced by `tavern_day_events.qsps` |
| `modules/locations/town/church_menus.qsps` | `BuildChurchMenu` | Replaced by routing in `church.qsps` |
| `modules/locations/town/church_pure_hearts_room.qsps` | `ChurchPureHeartsRoom` | No callers; confession uses other locs |
| `modules/locations/town/drevo_group_stub.qsps` | `DrevoGroupStub`, `DrevoTreeStub` | Unwired stubs |
| `modules/locations/shops/irma_shop_spy.qsps` | `IrmaShopSpyStub` | Unwired stub |
| `modules/actions/dialogs/dialogs.qsps` | `TalkWithAmanda/Melissa/Sandra/Inga` | Superseded by `GirlTalk` |
| `modules/menu/girls/amanda_show_info.qsps` | `Amanda_ShowInfo` | No callers |
| `modules/menu/girls/girls_quick_overview.qsps` | `GirlsQuickOverview` | No callers |
| `modules/menu/npc/npc_show_description.qsps` | `NpcShowDescription` | Use `NpcShowDescriptionPanel` |
| `modules/actions/sex/intim_entry.qsps` | `IntimEntry` | No callers; live path is `GirlIntim*` / `SexScene*` |
| `modules/actions/sex/intim_menu.qsps` | `MenuGirlIntim` | No callers |
| `modules/actions/sex/intim_poses.qsps` | `Intim_VaginalPoses`, `Intim_AnalPoses` | No callers |
| `modules/core/time/week_control.qsps` | `OLD_WeekControl` | Dead debug day-picker |
| `modules/locations/town/amanda_dark_alley.qsps` | `AmandaDarkAlley*` | Replaced by `events/dance/amanda_dark_alley.qsps` (`AmandaDanceAlley*`) |

Also previously archived:

- `archive/old/girl_work_rules*.qsps` — replaced by `GirlUniformTalk` / policy talk
- `archive/old/gifts/*` — old gift shelf system

## Not moved (false positives)

- `FUNC('ArtLevelText', …)` / similar — live via FUNC, not gt/gs string scan
- `Init*` NPC files — may be included via registry patterns
- `onstatusupdate`, `#Start` — engine entry hooks
- `becky_house.qsps` — `#IngaRoom` is live; only thin `#BeckyHouse` wrapper is unused
- `amanda_events.qsps` — neighbor-boys chain still used from debug/gates
- Text/print helpers called only by variable id
