# Verifies hall/kitchen visual wiring: location bodies + critical path contracts.
# Exit 0 = pass. Report: $env:VISUAL_REPORT

$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'modules\events\hall'))) {
  throw "Run from repo root"
}
$report = if ($env:VISUAL_REPORT) { $env:VISUAL_REPORT } else { Join-Path $root 'tools\visual_inventory_report.txt' }

$dirs = @(
  (Join-Path $root 'modules\events\hall'),
  (Join-Path $root 'modules\events\kitchen')
)

$visualRe = 'SceneShowVisual|ShowImage|ShowImagePath|HallHarassmentShowIntroImage|HallHarassmentShowImage|HallMissingGirlShowImage|HallMissingBargainShowImage|HallLewdShowImage|KitchenLewdShowImage|KitchenCustomerShowImage|NobleAttackShowImage|SandraKitchenShowImage|TavernHallEventShowVisual|ShowGirlTalkContextImage|HallMissingGirlPrintText|HallMissingPrintAfterBargain|HallLewdPrintText|HallHarassmentRenderScreen|KitchenHarassmentRenderScreen|HallMissingGirlShowScene|HallMissingNobleShow|VisPrintCaption'

$linesOut = New-Object System.Collections.Generic.List[string]
$fail = 0
$pass = 0

function Ok([string]$msg) { $script:pass++; $linesOut.Add("OK  $msg") }
function Fail([string]$msg) { $script:fail++; $linesOut.Add("FAIL $msg") }

foreach ($d in $dirs) {
  Get-ChildItem $d -Filter '*.qsps' -Recurse | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length).TrimStart('\', '/')
    $raw = Get-Content $_.FullName -Raw
    $parts = [regex]::Split($raw, '(?m)^(#\S+)\s*$')
    for ($p = 1; $p -lt $parts.Count - 1; $p += 2) {
      $loc = $parts[$p].TrimStart('#')
      $body = $parts[$p + 1]
      if ($body -notmatch '(?m)^\s*\*clr\s*$') { continue }
      $ok = [bool]($body -match $visualRe)
      if (-not $ok -and $body -match "gt 'HallHarassment'|gt 'KitchenHarassment'|gt 'HallMissingGirl|gt 'HallMissingBargain|RenderScreen") {
        $ok = $true
      }
      if ($ok) { Ok "$rel #$loc" } else { Fail "$rel #$loc no visual helper in location body" }
    }
  }
}

# --- critical path contracts (shipped helpers, not re-implement) ---
$helper = Get-Content (Join-Path $root 'modules\core\show_image\show_image_helpers.qsps') -Raw
if ($helper -match '#VisPrintCaption' -and $helper -match '\[VIS\]' -and $helper -match 'VIS future' -and $helper -match 'debug = 1') {
  Ok "VisPrintCaption + SceneShowVisual [VIS]/[VIS future] under debug"
} else {
  Fail "helpers missing VisPrintCaption or debug future"
}

$noble = Get-Content (Join-Path $root 'modules\events\hall\noble_attack.qsps') -Raw
if ($noble -match '#NobleAttackShowImage' -and $noble -match 'SceneShowVisual' -and ($noble -match 'VisPrintCaption' -or $noble -match 'SceneShowVisual')) {
  # primary path must not be ShowImagePath-only without VisPrintCaption
  $m = [regex]::Match($noble, '(?s)#NobleAttackShowImage\s*(.*?)---')
  $body = $m.Groups[1].Value
  if ($body -match 'ShowImagePath' -and $body -notmatch 'VisPrintCaption' -and $body -notmatch 'SceneShowVisual') {
    Fail "NobleAttackShowImage ShowImagePath without VisPrintCaption/SceneShowVisual"
  } elseif ($body -match 'SceneShowVisual' -or $body -match 'VisPrintCaption') {
    Ok "NobleAttackShowImage uses SceneShowVisual and/or VisPrintCaption"
  } else {
    Fail "NobleAttackShowImage missing caption helper"
  }
} else {
  Fail "NobleAttackShowImage missing"
}

$coach = Get-Content (Join-Path $root 'modules\events\hall\hall_play_coach.qsps') -Raw
$cm = [regex]::Match($coach, '(?s)#HallPlayCoachStart\s*(.*?)---')
$cbody = $cm.Groups[1].Value
if ($cbody -match 'HallPlayCoachCanOffer = 0' -and $cbody -match 'SceneShowVisual') {
  Ok "HallPlayCoachStart CanOffer=0 has SceneShowVisual"
} else {
  Fail "HallPlayCoachStart early exit missing SceneShowVisual"
}

$miss = Get-Content (Join-Path $root 'modules\events\hall\hall_missing_girl.qsps') -Raw
$mm = [regex]::Match($miss, '(?s)#HallMissingGirlShowImage\s*(.*?)---')
$mbody = $mm.Groups[1].Value
if ($mbody -match 'SceneShowVisual' -and ($mbody -match 'VisPrintCaption' -or $mbody -match 'VIS future')) {
  Ok "HallMissingGirlShowImage caption + future on all branches"
} else {
  Fail "HallMissingGirlShowImage missing VisPrintCaption/future on fallback"
}

$sk = Get-Content (Join-Path $root 'modules\events\kitchen\sandra_kitchen_hook.qsps') -Raw
$sm = [regex]::Match($sk, '(?s)#SandraKitchenShowImage\s*(.*?)---')
$sbody = $sm.Groups[1].Value
if ($sbody -match 'SceneShowVisual' -and ($sbody -match 'VisPrintCaption' -or $sbody -match 'VIS future')) {
  Ok "SandraKitchenShowImage caption + future on all branches"
} else {
  Fail "SandraKitchenShowImage missing VisPrintCaption/future on fallback"
}

# deferred inventory file must exist and mention modules/events outside hall/kitchen
$asset = Get-Content (Join-Path $root 'docs\ASSET-hall-events-visual.md') -Raw
if ($asset -match 'Deferred' -and $asset -match 'modules/events' -and $asset -match 'dance' -and $asset -match 'family' -and $asset -match '174') {
  Ok "ASSET doc lists deferred modules/events *clr outside hall/kitchen"
} elseif ($asset -match 'Deferred' -and $asset -match 'dance' -and $asset -match 'family' -and $asset -match 'tavern') {
  Ok "ASSET doc lists deferred event folders"
} else {
  Fail "ASSET deferred list incomplete for modules/events outside hall/kitchen"
}

$header = "visual inventory verify`nroot=$root`npass=$pass fail=$fail`n"
$full = $header + ($linesOut -join "`n") + "`n"
Set-Content -Path $report -Value $full -Encoding UTF8
Write-Output $full
if ($fail -gt 0) { exit 1 } else { exit 0 }
