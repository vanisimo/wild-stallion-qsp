# Project Structure

`TraKtir.qsps` is the entry point. The compiled game is `game.qsp`.

See also the generated tree: `project_tree.txt` (modules + archive).

## Build folders (`qsp-project.json`)

Only these are compiled:

- `modules/actions`
- `modules/core`
- `modules/menu`
- `modules/debug`
- `modules/events`
- `modules/locations`
- `modules/npc`

Not compiled: `archive/`, `modules/story/`, `modules/system/` (reserved), `images/` (assets only).

## Folder roles

| Folder | Role |
|--------|------|
| `modules/actions` | Player-initiated actions: dialogs, flirts, sex, tavern rules |
| `modules/core` | Shared engines: time, economy, girls data, images, knowledge, offense days |
| `modules/debug` | Debug panels / smoke tests |
| `modules/events` | Story triggers, scene chains, aftermath (by **theme/character**) |
| `modules/locations` | Playable places: rooms, shops, tavern, town map |
| `modules/menu` | UI: panels, NPC click, girl sidebar |
| `modules/npc` | **NPC init / base data only** (`#InitAmanda`, …) |
| `modules/story` | Reserved for huge arcs (empty placeholder) |
| `modules/system` | Reserved low-level helpers (empty placeholder) |
| `archive/old` | Dead/legacy modules (not in build) |
| `images` | Art assets |

## Events layout (character / theme)

| Path | Content |
|------|---------|
| `events/amanda/` | Neighbor boys, Liza overhear/talk, oral ladder, **Lizette chain** |
| `events/melissa/` | Home chain, dance, dark alley, minstrel arc |
| `events/sandra/` | Home chain, staff hire, Lermont letter, Becky reconcile, Draupnir Friday |
| `events/becky/` | Home chain, dance, talk texts |
| `events/inga/` | Dance, Lucas arc, romance |
| `events/eddie/` | Eddie arc |
| `events/family/` | Shared family: Act1, council, birth cert, aftermath, kinks, Amanda home first sex / path |
| `events/dance/` | Friday dance core, Amanda–Legare dance branch, Amanda dance / alley |
| `events/hall/`, `kitchen/` | Harassment, policy, hall systems |
| `events/tavern/` | Day events, dispatcher, Legare tavern pressure / visits / aftermath |
| `events/church/`, `port/`, `georgette/`, `legare/`, `quests/`, `shops/`, `visits/` | As named |
| `events/engine/` | Shared event engine helpers |

## Locations layout

| Path | Content |
|------|---------|
| `locations/rooms/` | Family rooms, player room/chest |
| `locations/tavern/` | Main hall, kitchen, management, activity hooks |
| `locations/shops/` | Becky / Irma / wine / sweets / Draupnir / house+Inga room |
| `locations/town/` | Street, market, market_dance, port, church, mayor, guard, craftsmen |

## NPC layout

| Path | Content |
|------|---------|
| `npc/amanda/amanda.qsps` | `#InitAmanda` only |
| `npc/family/` | Melissa, Sandra init |
| `npc/shops/`, `port/`, `legare/`, `town/` | Other NPC inits |

## Design docs (selected)

- `docs/economy.md`
- `docs/policy-flow.md`
- `docs/design-hall-harassment.md`
- `docs/design-hall-scene-unified.md` — harassment / lewd / missing: общие кнопки и policy
- `docs/design-interaction-schemes.md`
- `docs/handoff.md`

## Rule of thumb

- **core** — reusable mechanics (no long narrative scenes)
- **events** — triggers and scene flow (group by character/theme)
- **locations** — map entry points and shop hubs
- **npc** — init stats/names only; put arcs under `events/`
- **actions** — player menus and systems (talk, sex, policy)
- Do not put new code under `archive/` unless retiring it
