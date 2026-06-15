# Project Structure

`TraKtir.qsps` is the entry point. The compiled game is `game.qsp`.

## Folders

- `modules/actions` - player actions: dialogs, flirting, sex scenes, tavern actions.
- `modules/core` - shared systems: initialization, time, economy, image display, character data, helpers.
- `modules/debug` - debug panels and developer-only helpers.
- `modules/events` - event chains, dispatchers, consequences, reactions.
- `modules/locations` - playable locations.
- `modules/menu` - UI panels, status updates, clickable NPC links.
- `modules/npc` - NPC-specific initialization and scenes.
- `modules/story` - reserved for larger story arcs that should not live directly in `events`.
- `modules/system` - reserved for low-level technical helpers if `core` becomes too broad.
- `images` - location images and portraits.
- `archive` - old code kept for reference outside the active build.

## Event Subfolders

- `modules/events/engine` - shared event engine and dispatch helpers.
- `modules/events/npc` - NPC-specific event entry points.
- `modules/events/quests` - quest-oriented event modules.
- `modules/events/tavern` - tavern-wide event flow and tavern pressure scenes.

## Suggested Rule

Use `core` for reusable mechanics, `events` for triggers and event flow, and `story` for long narrative branches.
