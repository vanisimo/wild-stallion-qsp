param(
    [ValidateSet('dev', 'release')]
    [string]$Profile = 'dev'
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$buildScript = Join-Path $PSScriptRoot 'build.ps1'
$runScript = Join-Path $repoRoot 'run_game.bat'

& $buildScript -Profile $Profile
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& $runScript
exit $LASTEXITCODE