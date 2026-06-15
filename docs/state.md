# Game State Notes

This file documents important global state so new scenes do not create accidental duplicates.

## Global Setup

- `$RuntimeProfile` - startup profile, usually `dev` or `release`.
- `debug` - enables developer output and debug-only actions.
- `debug_images` - enables image debug details.
- `USEHTML` - enables HTML output.
- `$ONNEWLOC`, `$ONSTAT`, `$ONOBJSEL` - global QSP handlers.

## Date And Time

- `day`, `month`, `week`, `year` - current date.
- `time` - current time slot.
- Time slots currently use `1..5`: morning, noon, day, evening, night.

## Player And Tavern

- `money` - player money.
- `tavernfame` - tavern fame.
- `tavern_reputation` - tavern reputation.
- `tavern_sex_appeal` - tavern sex appeal.
- `tavernvisitors` - visitor pressure/count.
- `beer_price`, `wine_price`, `food_price` - prices.
- `productnum`, `winenum`, `beernum` - supplies.

## Characters

- `$AllGirlNames` - central ordered list of girl ids, initialized by `InitGirlsRegistry`.
- Character base data is initialized through `GirlsInitAll` and `GirlInitBase`.

## Daily Intimacy Limits

- `max_daily_cum` - daily player orgasm limit.
- `daily_cum_count` - current daily count.

## Maintenance Rule

When adding a new global variable, add a one-line note here with the owning module and intended meaning.
