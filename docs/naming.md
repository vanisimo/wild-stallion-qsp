# Naming Rules

## Files

- Use lowercase snake_case for new files: `amanda_legare_intro.qsps`.
- Put long text variants in a paired `_text.qsps` file.
- Avoid double dots, spaces, and mixed transliteration in filenames.

## Locations

- Use PascalCase location ids: `TavernMain`, `AmandaRoom`, `MarketDance`.
- Use explicit action/result suffixes for scene sublocations: `AmandaLegareDanceStart`, `AmandaLegareDanceResult`.

## Variables

- Use `$Name` for text values and `Name` for numeric values.
- Keep shared arrays centralized where possible, such as `$AllGirlNames` in `InitGirlsRegistry`.
- Prefix temporary local variables with `_` when they are only used inside one location.

## Images

- Use stable semantic names: `tavern_day.png`, `player_room.png`, `amanda.png`.
- Avoid names tied to temporary prompts or generation attempts.
