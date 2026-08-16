# Verifies game-wide *clr screens have a visual path (SceneShowVisual / ShowImage /
# location image helpers / domain *ShowImage). Exit 0 = pass.
# Report: $env:VISUAL_REPORT (default tools/visual_gamewide_report.txt)
# Scope: connected modules — events, locations, actions, core, menu, npc, debug.

$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'modules\events'))) {
  throw "Run from repo root"
}
$report = if ($env:VISUAL_REPORT) { $env:VISUAL_REPORT } else { Join-Path $root 'tools\visual_gamewide_report.txt' }

$scopeDirs = @(
  'modules\events',
  'modules\locations',
  'modules\actions',
  'modules\core',
  'modules\menu',
  'modules\npc',
  'modules\debug'
)

# Any of these in the location body means the *clr screen paints or dispatches to a painter.
$visualRe = @(
  'SceneShowVisual',
  'VisPrintCaption',
  'ShowImagePath',
  'ShowImage',
  'ShowLocationImage',
  'ShowLocationTimeImage',
  'ShowLocationScreenTitle',
  'TavernMainShowLocationImage',
  'KitchenShowLocationImage',
  'ShowTavernHallImage',
  'ShowTavernKitchenImage',
  'ShowTavernKitchenWorkImage',
  'ShowTavernExteriorImage',
  'HallHarassmentShowIntroImage',
  'HallHarassmentShowImage',
  'HallMissingGirlShowImage',
  'HallMissingBargainShowImage',
  'HallLewdShowImage',
  'KitchenLewdShowImage',
  'KitchenCustomerShowImage',
  'NobleAttackShowImage',
  'SandraKitchenShowImage',
  'TavernHallEventShowVisual',
  'ShowGirlTalkContextImage',
  'HallMissingGirlPrintText',
  'HallMissingPrintAfterBargain',
  'HallLewdPrintText',
  'HallHarassmentRenderScreen',
  'KitchenHarassmentRenderScreen',
  'HallMissingGirlShowScene',
  'HallMissingNobleShow',
  'SexSceneShowActionImage',
  'ShowGirlInLocation',
  'ShowWorkImage'
) -join '|'

$linesOut = New-Object System.Collections.Generic.List[string]
$fail = 0
$pass = 0
$skipDispatch = 0

function Ok([string]$msg) { $script:pass++; $linesOut.Add("OK  $msg") }
function Fail([string]$msg) { $script:fail++; $linesOut.Add("FAIL $msg") }
function Skip([string]$msg) { $script:skipDispatch++; $linesOut.Add("SKIP $msg") }

foreach ($relDir in $scopeDirs) {
  $d = Join-Path $root $relDir
  if (-not (Test-Path $d)) { continue }
  Get-ChildItem $d -Filter '*.qsps' -Recurse | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length).TrimStart('\', '/')
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    $parts = [regex]::Split($raw, '(?m)^(#\S+)\s*$')
    for ($p = 1; $p -lt $parts.Count - 1; $p += 2) {
      $loc = $parts[$p].TrimStart('#')
      $body = $parts[$p + 1]
      if ($body -notmatch '(?m)^\s*\*clr\s*$') { continue }

      if ($body -match $visualRe) {
        Ok "$rel #$loc"
        continue
      }

      # Pure dispatch only: location *clr then gt without painting *pl/*p.
      # Do NOT treat gt inside act: blocks as OK — those menus still paint text.
      $hasPl = ($body -match '(?m)^\s*\*pl\b') -or ($body -match '(?m)^\s*\*p\b')
      $hasGt = $body -match '(?m)^\s*gt\s'
      if ($hasGt -and -not $hasPl) {
        Skip "$rel #$loc pure-gt-dispatch"
        continue
      }

      Fail "$rel #$loc no visual helper in location body"
    }
  }
}

# Critical shared helpers still present
$helper = [System.IO.File]::ReadAllText((Join-Path $root 'modules\core\show_image\show_image_helpers.qsps'))
if ($helper -match '#SceneShowVisual' -and $helper -match '#VisPrintCaption' -and $helper -match '\[VIS\]') {
  Ok "helpers SceneShowVisual + VisPrintCaption"
} else {
  Fail "helpers missing SceneShowVisual or VisPrintCaption"
}

$header = "gamewide visual verify`nroot=$root`npass=$pass fail=$fail skip_dispatch=$skipDispatch`n"
$full = $header + ($linesOut -join "`n") + "`n"
[System.IO.File]::WriteAllText($report, $full, [System.Text.UTF8Encoding]::new($false))
Write-Output $full
if ($fail -gt 0) { exit 1 } else { exit 0 }
