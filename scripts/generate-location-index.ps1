param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$repoRootPrefix = $repoRoot.TrimEnd('\') + '\'
$projectPath = Join-Path $repoRoot 'qsp-project.json'
$indexPath = Join-Path $repoRoot 'docs\location-index.md'

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

    $lines = [System.IO.File]::ReadAllLines($file)
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^\s*#\s*(\S+)\s*$') {
            $locationFile = $relative -replace '\\', '/'
            $locations.Add([pscustomobject]@{
                Name = $Matches[1]
                File = $locationFile
                Line = $i + 1
                Group = $group
            })
        }
    }
}

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('# Location Index')
[void]$sb.AppendLine()
[void]$sb.AppendLine('Generated from active project files in `qsp-project.json`.')
[void]$sb.AppendLine()
[void]$sb.AppendLine("- Source files: $($files.Count)")
[void]$sb.AppendLine("- Locations: $($locations.Count)")
[void]$sb.AppendLine()

foreach ($group in ($locations | Select-Object -ExpandProperty Group -Unique | Sort-Object)) {
    $groupLocations = $locations | Where-Object { $_.Group -eq $group } | Sort-Object Name, File, Line

    [void]$sb.AppendLine("## $group")
    [void]$sb.AppendLine()
    [void]$sb.AppendLine('| Location | File | Line |')
    [void]$sb.AppendLine('| --- | --- | --- |')

    foreach ($location in $groupLocations) {
        $name = $location.Name
        $file = $location.File
        $line = $location.Line
        [void]$sb.AppendLine("| ``$name`` | ``$file`` | $line |")
    }

    [void]$sb.AppendLine()
}

$content = $sb.ToString()

if ($Check) {
    if (-not (Test-Path $indexPath)) {
        Write-Host "Location index is missing: $indexPath"
        exit 1
    }

    $existing = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)
    if ($existing -ne $content) {
        Write-Host 'Location index is out of date. Run scripts\generate-location-index.ps1.'
        exit 1
    }

    Write-Host 'Location index is up to date.'
    exit 0
}

[System.IO.File]::WriteAllText($indexPath, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote $($locations.Count) locations to $indexPath"
