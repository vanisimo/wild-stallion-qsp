param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$repoRootPrefix = $repoRoot.TrimEnd('\') + '\'
$projectPath = Join-Path $repoRoot 'qsp-project.json'
$reportPath = Join-Path $repoRoot 'docs\location-analysis.md'

if (-not (Test-Path $projectPath)) {
    throw "Project file not found: $projectPath"
}

$project = Get-Content -Raw $projectPath | ConvertFrom-Json
$module = $project.project[0]
$files = New-Object System.Collections.Generic.List[string]

foreach ($file in $module.files) {
    $path = Join-Path $repoRoot $file.path
    if (-not (Test-Path $path)) {
        throw "Missing project file: $($file.path)"
    }
    $files.Add((Resolve-Path $path).Path)
}

foreach ($folder in $module.folders) {
    $path = Join-Path $repoRoot $folder.path
    if (-not (Test-Path $path)) {
        throw "Missing project folder: $($folder.path)"
    }

    Get-ChildItem -Path $path -Recurse -File -Filter *.qsps |
        Sort-Object FullName |
        ForEach-Object { $files.Add($_.FullName) }
}

$locations = New-Object System.Collections.Generic.List[object]
$calls = New-Object System.Collections.Generic.List[object]
$dynamicCalls = New-Object System.Collections.Generic.List[object]
$callPattern = "(?i)\b(?:gs|gt|xgt)\s*'([^']+)'"
$externalLocationPrefixes = @('Table.')

foreach ($file in $files) {
    $relative = $file
    if ($file.StartsWith($repoRootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $relative = $file.Substring($repoRootPrefix.Length)
    }

    $group = ($relative -split '[\\/]', 3)[0]
    if ($relative.StartsWith('modules\', [System.StringComparison]::OrdinalIgnoreCase)) {
        $parts = $relative -split '[\\/]'
        if ($parts.Count -ge 2) {
            $group = "modules/$($parts[1])"
        }
    }

    $locationFile = $relative -replace '\\', '/'
    $lines = [System.IO.File]::ReadAllLines($file)

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        $lineNumber = $i + 1
        $isComment = $line.TrimStart().StartsWith('!')

        if ($line -match '^\s*#\s*(\S+)\s*$') {
            $locations.Add([pscustomobject]@{
                Name = $Matches[1]
                File = $locationFile
                Line = $lineNumber
                Group = $group
            })
        }

        if ($isComment) {
            continue
        }

        foreach ($match in [regex]::Matches($line, $callPattern)) {
            $target = $match.Groups[1].Value
            $afterCall = $line.Substring($match.Index + $match.Length).TrimStart()

            if ($target -match '[<$"+]' -or $afterCall.StartsWith('+')) {
                $dynamicCalls.Add([pscustomobject]@{
                    Target = $target
                    Source = "${locationFile}:${lineNumber}"
                })
                continue
            }

            $isExternalLocation = $false
            foreach ($prefix in $externalLocationPrefixes) {
                if ($target.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                    $isExternalLocation = $true
                }
            }

            if ($isExternalLocation) {
                continue
            }

            $calls.Add([pscustomobject]@{
                Target = $target
                Source = "${locationFile}:${lineNumber}"
            })
        }
    }
}

$incoming = @{}
foreach ($location in $locations) {
    $incoming[$location.Name] = New-Object System.Collections.Generic.List[string]
}

foreach ($call in $calls) {
    if ($incoming.ContainsKey($call.Target)) {
        $incoming[$call.Target].Add($call.Source)
    }
}

$entryPatterns = @(
    '^Start$',
    '^Debug',
    'Debug',
    '^Init',
    '^OLD_',
    '^Menu\.',
    '^Menu',
    '^NPC_',
    '^Npc',
    '^EventKnowledge',
    '^Knowledge',
    '^HallKnowledge',
    '^Register',
    '^Panel',
    '^Show',
    '^TalkWith',
    '^Random',
    '^Refresh',
    '^Set',
    '^Daily',
    '^Confirm',
    '^TavernMain',
    '^Tavern.*Event',
    '^Tavern.*Harass',
    '^GroupSexMenu$',
    '^Intim_',
    '^otd_lib_menu$',
    '^Get',
    '^Is',
    '^Calculate',
    '^Check',
    '^Apply',
    '^Can',
    '^LOC$',
    '^onstatusupdate$',
    '^ItemPanelClick$',
    'Stub$',
    'Start$',
    'Try$',
    'TryEvent$',
    'TryAutoStart$',
    'Queue$',
    'CanRun$',
    'Clear$',
    'Flirt$',
    'Otkroven',
    '\.\{',
    'Mark',
    'Text$',
    'NormalizeKey$',
    'EnsureName$',
    'Overview$',
    'Clamp',
    'Reset',
    'Print',
    'BuildMenu$',
    'CanStart$',
    'CanShow$',
    'CanDiscuss$',
    'TryAutoStart$'
)

$unused = New-Object System.Collections.Generic.List[object]
$classifiedUnused = New-Object System.Collections.Generic.List[object]

foreach ($location in ($locations | Sort-Object Name, File, Line)) {
    $incomingCount = $incoming[$location.Name].Count
    if ($incomingCount -gt 0) {
        continue
    }

    $kind = 'review'
    foreach ($pattern in $entryPatterns) {
        if ($location.Name -match $pattern) {
            $kind = 'entry/helper'
            break
        }
    }

    if ($location.Name -eq 'Start') {
        $kind = 'start'
    }

    $item = [pscustomobject]@{
        Name = $location.Name
        File = $location.File
        Line = $location.Line
        Group = $location.Group
        Kind = $kind
    }

    if ($kind -eq 'review') {
        $unused.Add($item)
    }
    else {
        $classifiedUnused.Add($item)
    }
}

$calledLocations = ($incoming.GetEnumerator() | Where-Object { $_.Value.Count -gt 0 }).Count
$uncalledLocations = $locations.Count - $calledLocations
$topCalled = $incoming.GetEnumerator() |
    Sort-Object { $_.Value.Count } -Descending |
    Select-Object -First 25

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('# Location Analysis')
[void]$sb.AppendLine()
[void]$sb.AppendLine('Generated from active project files in `qsp-project.json`.')
[void]$sb.AppendLine()
[void]$sb.AppendLine("- Source files: $($files.Count)")
[void]$sb.AppendLine("- Locations: $($locations.Count)")
[void]$sb.AppendLine("- Locations with direct incoming calls: $calledLocations")
[void]$sb.AppendLine("- Locations without direct incoming calls: $uncalledLocations")
[void]$sb.AppendLine("- Review candidates without direct incoming calls: $($unused.Count)")
[void]$sb.AppendLine("- Classified entry/helper locations without direct incoming calls: $($classifiedUnused.Count)")
[void]$sb.AppendLine("- Dynamic call sites: $($dynamicCalls.Count)")
[void]$sb.AppendLine()

[void]$sb.AppendLine('## Review Candidates')
[void]$sb.AppendLine()
[void]$sb.AppendLine('These locations have no direct literal incoming calls and are not classified as common entry/helper/debug/text locations. Review before deleting; QSP can call locations dynamically.')
[void]$sb.AppendLine()
[void]$sb.AppendLine('| Location | File | Line | Group |')
[void]$sb.AppendLine('| --- | --- | --- | --- |')

foreach ($item in $unused) {
    $name = $item.Name
    $file = $item.File
    $line = $item.Line
    $group = $item.Group
    [void]$sb.AppendLine("| ``$name`` | ``$file`` | $line | ``$group`` |")
}

[void]$sb.AppendLine()
[void]$sb.AppendLine('## Classified Entry Or Helper Locations')
[void]$sb.AppendLine()
[void]$sb.AppendLine('These also have no direct incoming calls, but their names suggest debug panels, start entries, text helpers, init/reset helpers, menus, or compatibility stubs.')
[void]$sb.AppendLine()
[void]$sb.AppendLine('| Location | File | Line | Kind |')
[void]$sb.AppendLine('| --- | --- | --- | --- |')

foreach ($item in $classifiedUnused | Sort-Object Kind, Name, File, Line) {
    $name = $item.Name
    $file = $item.File
    $line = $item.Line
    $kind = $item.Kind
    [void]$sb.AppendLine("| ``$name`` | ``$file`` | $line | ``$kind`` |")
}

[void]$sb.AppendLine()
[void]$sb.AppendLine('## Top Directly Called Locations')
[void]$sb.AppendLine()
[void]$sb.AppendLine('| Location | Incoming calls |')
[void]$sb.AppendLine('| --- | --- |')

foreach ($entry in $topCalled) {
    $name = $entry.Key
    $count = $entry.Value.Count
    [void]$sb.AppendLine("| ``$name`` | $count |")
}

[void]$sb.AppendLine()
[void]$sb.AppendLine('## Dynamic Call Sites')
[void]$sb.AppendLine()
[void]$sb.AppendLine('These calls use dynamic names or string concatenation and cannot be resolved safely by this script.')
[void]$sb.AppendLine()
[void]$sb.AppendLine('| Target expression | Source |')
[void]$sb.AppendLine('| --- | --- |')

foreach ($call in $dynamicCalls | Sort-Object Source, Target) {
    $target = $call.Target
    $source = $call.Source
    [void]$sb.AppendLine("| ``$target`` | ``$source`` |")
}

$content = $sb.ToString()

if ($Check) {
    if (-not (Test-Path $reportPath)) {
        Write-Host "Location analysis is missing: $reportPath"
        exit 1
    }

    $existing = [System.IO.File]::ReadAllText($reportPath, [System.Text.Encoding]::UTF8)
    if ($existing -ne $content) {
        Write-Host 'Location analysis is out of date. Run scripts\analyze-locations.ps1.'
        exit 1
    }

    Write-Host 'Location analysis is up to date.'
    exit 0
}

[System.IO.File]::WriteAllText($reportPath, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote location analysis to $reportPath"
