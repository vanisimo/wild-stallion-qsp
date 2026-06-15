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
- `modules/events/amanda` - Amanda-specific event entry points.
- `modules/events/shops` - shopkeeper and shop-family event entry points.
- `modules/events/quests` - quest-oriented event modules.
- `modules/events/tavern` - tavern-wide event flow and tavern pressure scenes.

## Location Subfolders

- `modules/locations/tavern` - tavern interior and tavern management locations.
- `modules/locations/rooms` - private rooms.
- `modules/locations/town` - city and outdoor locations.
- `modules/locations/shops` - shop locations and shop-specific scenes.

## Menu Subfolders

- `modules/menu/panels` - status panels and dashboard-like UI blocks.
- `modules/menu/girls` - girl overview, actions, conditions, and sidebars.
- `modules/menu/npc` - NPC click handlers and description panels.
- `modules/menu/system` - global buttons, status update hooks, and menu library helpers.

## Core Subfolders

- `modules/core/system` - startup, global helpers, debug helpers, and location refresh utilities.
- `modules/core/girls` - shared girl data, jobs, location, key, and intimacy helpers.
- `modules/core/init_npc` - NPC and girl initialization registry/data.
- `modules/core/time` - calendar, time, schedules, day transitions.
- `modules/core/tavern` - tavern state, income, reputation, and tavern event state.
- `modules/core/economy` - supply economy and stock calculations.
- `modules/core/knowledge` - event knowledge ids and knowledge tracking.
- `modules/core/show_image` - image display and image debug helpers.

## Action Subfolders

- `modules/actions/dialogs` - direct dialog entry points and conversation actions.
- `modules/actions/flirts` - flirting actions.
- `modules/actions/sex` - intimacy scene actions and registration helpers.
- `modules/actions/tavern` - tavern work, uniform, and work policy actions.

## NPC Subfolders

- `modules/npc/amanda` - Amanda-specific scenes and Amanda-related branches.
- `modules/npc/family` - close family NPC initialization.
- `modules/npc/shops` - shopkeeper families and shop-linked NPCs.
- `modules/npc/port` - port-side NPCs and related families.
- `modules/npc/legare` - Legare family NPC initialization.
- `modules/npc/town` - town NPCs and supporting characters.

## Suggested Rule

Use `core` for reusable mechanics, `events` for triggers and event flow, and `story` for long narrative branches.
