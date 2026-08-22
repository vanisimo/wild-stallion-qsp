# Structural checks: Amanda/Melissa missing ladder invariants (thigh off, mouth bridge, free terminals).
# Exit 0 = pass. Report: $env:MISSING_LADDER_REPORT

$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$report = if ($env:MISSING_LADDER_REPORT) { $env:MISSING_LADDER_REPORT } else { Join-Path $root 'tools\missing_ladder_report.txt' }

$fail = 0
$pass = 0
$lines = New-Object System.Collections.Generic.List[string]
function Ok([string]$m) { $script:pass++; $lines.Add("OK  $m") }
function Fail([string]$m) { $script:fail++; $lines.Add("FAIL $m") }

$bargain = [System.IO.File]::ReadAllText((Join-Path $root 'modules\events\hall\hall_missing_bargain.qsps'))
$girl = [System.IO.File]::ReadAllText((Join-Path $root 'modules\events\hall\hall_missing_girl.qsps'))
$amanda = [System.IO.File]::ReadAllText((Join-Path $root 'modules\events\hall\hall_missing_agent_amanda_text.qsps'))
$melissa = [System.IO.File]::ReadAllText((Join-Path $root 'modules\events\hall\hall_missing_agent_melissa_text.qsps'))

# piggy_look / bud_smell must not assign touch_thigh
$piggyRe = "(?s)piggy_look':(.*?)bud_cuni"
$m = [regex]::Match($bargain, $piggyRe)
if ($m.Success) {
  if ($m.Groups[1].Value -match "PrivateAct = 'touch_thigh'") {
    Fail "piggy_look/bud_smell still assigns touch_thigh"
  } else {
    Ok "h0a piggy_look/bud_smell has no touch_thigh act"
  }
} else {
  Fail "could not find piggy_look/bud_smell block"
}

# free sister mouth: HardLadderDone -> spit/swallow
if (($bargain -match 'HallMissingHardLadderDone\[\$HallMissingGirl\] = 1') -and ($bargain -match "Finish = 'spit'") -and ($bargain -match "Finish = 'swallow'")) {
  Ok "free sister mouth uses HardLadderDone spit/swallow path"
} else {
  Fail "free sister mouth HardLadderDone spit/swallow missing"
}

# Amanda thigh redirect
if ($amanda -match 'S-AM-04' -and $amanda -match "gs 'HallMissingScene_hug_waist_amanda'") {
  Ok "Amanda S-AM-04 redirects to hug_waist"
} else {
  Fail "Amanda S-AM-04 hug redirect missing"
}

# Melissa thigh redirect
if ($melissa -match 'S-ML-04' -and $melissa -match "gs 'HallMissingScene_hug_waist_melissa'") {
  Ok "Melissa S-ML-04 redirects to hug_waist"
} else {
  Fail "Melissa S-ML-04 hug redirect missing"
}

# Amanda/Melissa mouth bridge: after mouth_taste loc, Explicit sets initiative high
$amClamp = [regex]::Match($amanda, "(?s)#HallMissingScene_mouth_taste_amanda\s*(.{0,400}?)HallMissingInitiative = 'high'")
if ($amClamp.Success -and $amClamp.Groups[1].Value -match 'HallMissingBargainExplicit = 1') {
  Ok "Amanda mouth_taste clamps Explicit to high"
} else {
  Fail "Amanda mouth_taste Explicit->high clamp missing"
}
$meClamp = [regex]::Match($melissa, "(?s)#HallMissingScene_mouth_taste_melissa\s*(.{0,400}?)HallMissingInitiative = 'high'")
if ($meClamp.Success -and $meClamp.Groups[1].Value -match 'HallMissingBargainExplicit = 1') {
  Ok "Melissa mouth_taste clamps Explicit to high"
} else {
  Fail "Melissa mouth_taste Explicit->high clamp missing"
}

# dispatch
if ($girl -match "touch_thigh_amanda" -and $girl -match "HallMissingScene_hug_waist_amanda" -and $girl -match "touch_thigh_melissa" -and $girl -match "HallMissingScene_hug_waist_melissa") {
  Ok "girl dispatch maps touch_thigh A/M to hug scenes"
} else {
  Fail "girl dispatch thigh->hug incomplete"
}

$header = "hall missing ladder verify`nroot=$root`npass=$pass fail=$fail`n"
$full = $header + ($lines -join "`n") + "`n"
[System.IO.File]::WriteAllText($report, $full, [System.Text.UTF8Encoding]::new($false))
Write-Output $full
if ($fail -gt 0) { exit 1 } else { exit 0 }
