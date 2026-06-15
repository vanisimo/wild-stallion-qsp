param(
    [switch]$ShowWarnings,
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$repoRootPrefix = $repoRoot.TrimEnd('\') + '\'
$projectPath = Join-Path $repoRoot 'qsp-project.json'
$locationIndexScript = Join-Path $PSScriptRoot 'generate-location-index.ps1'
$locationAnalysisScript = Join-Path $PSScriptRoot 'analyze-locations.ps1'

if (-not (Test-Path $projectPath)) {
    throw "Project file not found: $projectPath"
}

$project = Get-Content -Raw $projectPath | ConvertFrom-Json
$module = $project.project[0]
$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$files = New-Object System.Collections.Generic.List[string]

function Add-Error([string]$Message) {
    $script:errors.Add($Message)
}

function Add-Warning([string]$Message) {
    $script:warnings.Add($Message)
}

foreach ($file in $module.files) {
    $path = Join-Path $repoRoot $file.path
    if (Test-Path $path) {
        $files.Add((Resolve-Path $path).Path)
    }
    else {
        Add-Error "Missing project file: $($file.path)"
    }
}

foreach ($folder in $module.folders) {
    $path = Join-Path $repoRoot $folder.path
    if (-not (Test-Path $path)) {
        Add-Error "Missing project folder: $($folder.path)"
        continue
    }

    $folderFiles = Get-ChildItem -Path $path -Recurse -File -Filter *.qsps | Sort-Object FullName
    if (-not $folderFiles) {
        Add-Warning "Project folder has no qsps files: $($folder.path)"
        continue
    }

    foreach ($item in $folderFiles) {
        $files.Add($item.FullName)
    }
}

$locations = @{}
$callPattern = "(?i)\b(?:gs|gt|xgt)\s*'([^']+)'"
$imagePattern = "images/[A-Za-z0-9_./-]+\.(?:png|jpg|jpeg|webp|gif)"
$literalCalls = New-Object System.Collections.Generic.List[object]
$externalLocationPrefixes = @('Table.')

foreach ($file in $files) {
    $relative = $file
    if ($file.StartsWith($repoRootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $relative = $file.Substring($repoRootPrefix.Length)
    }
    $lines = [System.IO.File]::ReadAllLines($file)

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        $lineNumber = $i + 1
        $isComment = $line.TrimStart().StartsWith('!')

        if ($line -match '^\s*#\s*(\S+)\s*$') {
            $name = $Matches[1]
            if (-not $locations.ContainsKey($name)) {
                $locations[$name] = New-Object System.Collections.Generic.List[string]
            }
            $locations[$name].Add("${relative}:${lineNumber}")
        }

        if (-not $isComment) {
            foreach ($match in [regex]::Matches($line, $callPattern)) {
                $target = $match.Groups[1].Value
                if ($target -match '[<$"+]') {
                    continue
                }

                $afterCall = $line.Substring($match.Index + $match.Length).TrimStart()
                if ($afterCall.StartsWith('+')) {
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

                $literalCalls.Add([pscustomobject]@{
                    Target = $target
                    Source = "${relative}:${lineNumber}"
                })
            }

            foreach ($match in [regex]::Matches($line, $imagePattern)) {
                $imagePath = $match.Value
                $absoluteImagePath = Join-Path $repoRoot ($imagePath -replace '/', '\')
                if (-not (Test-Path $absoluteImagePath)) {
                    Add-Warning "Missing literal image reference: $imagePath at ${relative}:${lineNumber}"
                }
            }
        }
    }
}

foreach ($entry in $locations.GetEnumerator() | Sort-Object Name) {
    if ($entry.Value.Count -gt 1) {
        Add-Error "Duplicate location '$($entry.Name)': $($entry.Value -join ', ')"
    }
}

foreach ($call in $literalCalls) {
    if (-not $locations.ContainsKey($call.Target)) {
        Add-Warning "Missing literal location target '$($call.Target)' at $($call.Source)"
    }
}

Write-Host "Checked $($files.Count) source files."
Write-Host "Found $($locations.Count) locations."

if ($warnings.Count -gt 0 -and ($ShowWarnings -or $Strict)) {
    Write-Host ""
    Write-Host "Warnings:"
    foreach ($warning in $warnings) {
        Write-Host " - $warning"
    }
}
elseif ($warnings.Count -gt 0) {
    Write-Host "Warnings: $($warnings.Count). Re-run with -ShowWarnings to list them."
}

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "Errors:"
    foreach ($errorItem in $errors) {
        Write-Host " - $errorItem"
    }
    exit 1
}

if ($Strict -and $warnings.Count -gt 0) {
    exit 1
}

if ($Strict -and (Test-Path $locationIndexScript)) {
    & $locationIndexScript -Check
}

if ($Strict -and (Test-Path $locationAnalysisScript)) {
    & $locationAnalysisScript -Check
}

Write-Host "Project check passed."
