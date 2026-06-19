# Creates the images/ folder tree used by ShowImage / ShowLocationTimeImage / events.
# Safe to re-run: only creates missing directories.

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\images')).Path

$girls = @(
    'sandra', 'melissa', 'amanda', 'becky', 'inga', 'greta',
    'lizette', 'georgett', 'clarissa', 'irma', 'juliette'
)
$tavernGirls = @('sandra', 'melissa', 'amanda')

$hallLewdScenes = @('bend', 'waist', 'sit_near', 'lap', 'kiss', 'floor', 'ladder', 'fall')
$hallMissingPlaces = @('under_table', 'storage', 'kitchen', 'stairs', 'second_floor')
$hallHarassJobs = @('waitress', 'cleaning', 'kitchen')

$kitchenScenes = @(
    'bad_food', 'wrong_order', 'drunk_enters', 'grab', 'pantry_corner', 'satisfied_slap'
)

$sexActions = @('kiss', 'touch', 'oral', 'vaginal', 'anal', 'foreplay', 'finish', 'after', 'group')

$talkMoods = @('calm', 'happy', 'tired', 'angry')

$tavernDayKeys = @(
    'caravan_morning', 'rats_storage', 'rats_brawl', 'hall_brawl', 'guard_inspection',
    'harvest_festival', 'minstrels_hall', 'storm_outside', 'pilgrims_hall',
    'broken_barrel', 'cellar_thief', 'carpenter_repair'
)

$legareConflictKeys = @('first_conflict', 'supply_pressure', 'clarissa_suspicion')

$amandaLegareKeys = @(
    'visit', 'second_meet', 'outside_wall', 'outside_meet', 'major_risk'
)

$danceAmandaLegareKeys = @('notice', 'invite', 'after_dance', 'dance')

$dirs = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

function Add-Dir([string]$rel) {
    if ([string]::IsNullOrWhiteSpace($rel)) { return }
    $norm = $rel -replace '\\', '/'
    [void]$dirs.Add($norm)
}

Add-Dir 'common'
Add-Dir 'common/ui'
Add-Dir 'common/ui/actions'
Add-Dir 'common/ui/portraits'

foreach ($g in $girls) {
    Add-Dir "portraits/$g"
    Add-Dir "girls/$g"
    Add-Dir "dance/$g"
    Add-Dir "sex/$g"
    Add-Dir "events/$g"
    Add-Dir "events/girl_talk/$g"
    Add-Dir "events/sex/$g"

    foreach ($act in $sexActions) {
        Add-Dir "sex/$g/$act"
    }
}

foreach ($g in $tavernGirls) {
    Add-Dir "events/$g/hall_lewd/reaction"
    Add-Dir "events/$g/kitchen_customer/reaction"
    Add-Dir "events/$g/hall_harass/reaction"

    foreach ($job in $hallHarassJobs) {
        Add-Dir "events/$g/hall_harass/$job"
    }

    foreach ($scene in $hallLewdScenes) {
        Add-Dir "events/$g/hall_lewd/$scene"
    }

    foreach ($place in $hallMissingPlaces) {
        Add-Dir "events/$g/hall_missing/$place"
    }

    foreach ($scene in $kitchenScenes) {
        Add-Dir "events/$g/kitchen_customer/$scene"
    }
}

Add-Dir 'events/tavern/day'
foreach ($k in $tavernDayKeys) { Add-Dir "events/tavern/day/$k" }

Add-Dir 'events/tavern/legare_conflict'
foreach ($k in $legareConflictKeys) { Add-Dir "events/tavern/legare_conflict/$k" }

Add-Dir 'events/tavern/amanda_legare'
foreach ($k in $amandaLegareKeys) { Add-Dir "events/tavern/amanda_legare/$k" }

Add-Dir 'events/dance/amanda_legare'
foreach ($k in $danceAmandaLegareKeys) { Add-Dir "events/dance/amanda_legare/$k" }

Add-Dir 'events/port/amanda_lizette'
Add-Dir 'events/church'
Add-Dir 'events/georgette'
Add-Dir 'events/hall'

Add-Dir 'locations/tavern/hall'
Add-Dir 'locations/tavern/kitchen'
Add-Dir 'locations/market/market'
Add-Dir 'locations/market/dance'
Add-Dir 'locations/port/capital_ship'
Add-Dir 'locations/port/general'
Add-Dir 'locations/port/alley'
Add-Dir 'locations/church/general'
Add-Dir 'locations/guard/post'
Add-Dir 'locations/wine/shop'
Add-Dir 'locations/becky/shop'
Add-Dir 'locations/becky/house'
Add-Dir 'locations/irma/shop'
Add-Dir 'locations/street'
Add-Dir 'locations/mayor/office'
Add-Dir 'locations/craftsmen/draupnir'
Add-Dir 'locations/craftsmen/quarter'
Add-Dir 'locations/rooms/player'
Add-Dir 'locations/rooms/sandra'
Add-Dir 'locations/rooms/melissa'
Add-Dir 'locations/rooms/amanda'
Add-Dir 'locations/tavern/second_floor'
Add-Dir 'locations/tavern/management'

$created = 0
$sorted = $dirs | Sort-Object
foreach ($rel in $sorted) {
    $full = Join-Path $root $rel
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        $created++
    }
    $keep = Join-Path $full '.gitkeep'
    if (-not (Test-Path $keep)) {
        Set-Content -Path $keep -Value '' -Encoding UTF8
    }
}

Write-Host "images root: $root"
Write-Host "folders ensured: $($sorted.Count) (new: $created)"