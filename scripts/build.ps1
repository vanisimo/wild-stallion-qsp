param(
    [switch]$NoCopy
)

$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$buildDir = Join-Path $repoRoot '.build\qsp-cli'
$outDir = Join-Path $buildDir 'out'
$combined = Join-Path $buildDir 'game.qsps'
$targetGame = Join-Path $repoRoot 'game.qsp'

$nodeDir = 'C:\Program Files\nodejs'
$npmDir = Join-Path $env:APPDATA 'npm'
$env:PATH = "$nodeDir;$npmDir;$env:PATH"

$qspCli = Get-Command qsp-cli.cmd -ErrorAction SilentlyContinue
if (-not $qspCli) {
    throw 'qsp-cli.cmd was not found. Install @qsp/cli or add it to PATH.'
}

$projectPath = Join-Path $repoRoot 'qsp-project.json'
$project = Get-Content -Raw $projectPath | ConvertFrom-Json
$module = $project.project[0]

New-Item -ItemType Directory -Force $buildDir, $outDir | Out-Null

$files = New-Object System.Collections.Generic.List[string]
foreach ($file in $module.files) {
    $files.Add((Join-Path $repoRoot $file.path))
}

foreach ($folder in $module.folders) {
    Get-ChildItem -Path (Join-Path $repoRoot $folder.path) -Recurse -File -Filter *.qsps |
        Sort-Object FullName |
        ForEach-Object { $files.Add($_.FullName) }
}

$sb = New-Object System.Text.StringBuilder
foreach ($file in $files) {
    [void]$sb.AppendLine([System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8))
    [void]$sb.AppendLine()
}

[System.IO.File]::WriteAllText($combined, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))

Push-Location $buildDir
try {
    & $qspCli.Source 'game.qsps' --directory 'out'
}
finally {
    Pop-Location
}

$builtGame = Join-Path $outDir 'game.qsp'
if (-not (Test-Path $builtGame)) {
    throw "Build did not produce $builtGame"
}

if (-not $NoCopy) {
    Copy-Item $builtGame $targetGame -Force
}

Write-Host "Built $($files.Count) source files."
Write-Host "Output: $builtGame"
if (-not $NoCopy) {
    Write-Host "Copied: $targetGame"
}
