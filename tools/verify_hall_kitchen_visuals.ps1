# Verifies each QSP location with *clr in hall/kitchen has a visual helper in its body.
# Exit 0 = pass. Report: $env:VISUAL_REPORT or tools/visual_inventory_report.txt

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

$visualRe = 'SceneShowVisual|ShowImage|ShowImagePath|HallHarassmentShowIntroImage|HallHarassmentShowImage|HallMissingGirlShowImage|HallMissingBargainShowImage|HallLewdShowImage|KitchenLewdShowImage|KitchenCustomerShowImage|NobleAttackShowImage|SandraKitchenShowImage|TavernHallEventShowVisual|ShowGirlTalkContextImage|HallMissingGirlPrintText|HallMissingPrintAfterBargain|HallLewdPrintText|HallHarassmentRenderScreen|KitchenHarassmentRenderScreen|HallMissingGirlShowScene|HallMissingNobleShow'

$linesOut = New-Object System.Collections.Generic.List[string]
$fail = 0
$pass = 0

foreach ($d in $dirs) {
  Get-ChildItem $d -Filter '*.qsps' -Recurse | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length).TrimStart('\', '/')
    $raw = Get-Content $_.FullName -Raw
    # Split on location headers keeping names
    $parts = [regex]::Split($raw, '(?m)^(#\S+)\s*$')
    # parts[0]=preamble, then pairs (name, body)
    for ($p = 1; $p -lt $parts.Count - 1; $p += 2) {
      $loc = $parts[$p].TrimStart('#')
      $body = $parts[$p + 1]
      if ($body -notmatch '(?m)^\s*\*clr\s*$') { continue }
      # cut at next --- end of location if present for first chunk only - body already until next #
      $ok = [bool]($body -match $visualRe)
      # Delegating starts: jump to another location that shows image
      if (-not $ok -and $body -match "gt 'HallHarassment'|gt 'KitchenHarassment'|gt 'HallMissingGirl|gt 'HallMissingBargain|gt 'HallLewd|RenderScreen") {
        $ok = $true
      }
      if ($ok) {
        $pass++
        $linesOut.Add("OK  $rel #$loc")
      } else {
        $fail++
        $linesOut.Add("FAIL $rel #$loc no visual helper in location body")
      }
    }
  }
}

$helper = Join-Path $root 'modules\core\show_image\show_image_helpers.qsps'
$h = Get-Content $helper -Raw
if ($h -match '\[VIS\]' -and $h -match 'VIS future' -and $h -match 'debug = 1') {
  $pass++
  $linesOut.Add('OK  SceneShowVisual [VIS] + debug future path')
} else {
  $fail++
  $linesOut.Add('FAIL SceneShowVisual missing caption or debug future')
}

$header = "visual inventory verify`nroot=$root`npass=$pass fail=$fail`n"
$full = $header + ($linesOut -join "`n") + "`n"
Set-Content -Path $report -Value $full -Encoding UTF8
Write-Output $full
if ($fail -gt 0) { exit 1 } else { exit 0 }
