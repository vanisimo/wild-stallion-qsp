# Verifies SFW art batch files exist on disk for SceneShowVisual keys.
# List: tools/art_batch_sfw_keys.txt (path without extension, one per line)
# Exit 0 = all exist as .webp (or .png). Report: $env:ART_BATCH_REPORT

$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$listFile = Join-Path $root 'tools\art_batch_sfw_keys.txt'
if (-not (Test-Path $listFile)) {
  throw "Missing $listFile"
}
$report = if ($env:ART_BATCH_REPORT) { $env:ART_BATCH_REPORT } else { Join-Path $root 'tools\art_batch_files_report.txt' }

$linesOut = New-Object System.Collections.Generic.List[string]
$fail = 0
$pass = 0

Get-Content $listFile -Encoding UTF8 | ForEach-Object {
  $line = $_.Trim()
  if ($line -eq '' -or $line.StartsWith('#')) { return }
  $key = ($line -split '\|')[0].Trim()
  if ($key -eq '') { return }
  $webp = Join-Path $root ($key + '.webp')
  $png = Join-Path $root ($key + '.png')
  if (Test-Path $webp) {
    $script:pass++
    $sz = (Get-Item $webp).Length
    $linesOut.Add("OK  $key.webp size=$sz")
  } elseif (Test-Path $png) {
    $script:pass++
    $sz = (Get-Item $png).Length
    $linesOut.Add("OK  $key.png size=$sz")
  } else {
    $script:fail++
    $linesOut.Add("FAIL $key (no .webp/.png)")
  }
}

$header = "art batch file verify`nroot=$root`npass=$pass fail=$fail`n"
$full = $header + ($linesOut -join "`n") + "`n"
[System.IO.File]::WriteAllText($report, $full, [System.Text.UTF8Encoding]::new($false))
Write-Output $full
if ($fail -gt 0) { exit 1 } else { exit 0 }
