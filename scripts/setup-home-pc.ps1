# One-time setup for a fresh TraKtir workspace (build tools + game.qsp)
param(
    [switch]$SkipNodeInstall
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

function Ensure-Node {
    $node = Get-Command node -ErrorAction SilentlyContinue
    if ($node) {
        Write-Host "Node.js: $($node.Source)"
        return
    }

    if ($SkipNodeInstall) {
        throw 'Node.js is not installed. Install Node.js LTS or rerun without -SkipNodeInstall.'
    }

    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw 'Node.js is missing and winget is unavailable. Install Node.js LTS manually from https://nodejs.org/'
    }

    Write-Host 'Installing Node.js LTS via winget...'
    & winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    $env:PATH = "C:\Program Files\nodejs;$env:APPDATA\npm;$env:PATH"
}

function Ensure-QspCli {
    $env:PATH = "C:\Program Files\nodejs;$env:APPDATA\npm;$env:PATH"
    $qspCli = Get-Command qsp-cli.cmd -ErrorAction SilentlyContinue
    if ($qspCli) {
        Write-Host "qsp-cli: $($qspCli.Source)"
        return
    }

    Write-Host 'Installing @qsp/cli globally...'
    & npm install -g @qsp/cli
}

function Ensure-QspPlayer {
    $candidates = @(
        'C:\Program Files\QSP\qsp590\qspgui.exe',
        'C:\Program Files\QSP\bin\qspgui.exe',
        'D:\QSP\qsp590\qspgui.exe',
        'E:\Vano\QSP\qsp590\qspgui.exe'
    )

    foreach ($path in $candidates) {
        if (Test-Path $path) {
            Write-Host "QSP player: $path"
            return
        }
    }

    Write-Warning 'QSP player (qspgui.exe) not found. Install QSP 5.90 and rerun run_game.bat.'
}

Write-Host "TraKtir setup: $repoRoot"
Ensure-Node
Ensure-QspCli
Ensure-QspPlayer

$qqspIni = Join-Path $repoRoot 'qqsp.ini'
if (Test-Path $qqspIni) {
    $gamePath = (Join-Path $repoRoot 'game.qsp') -replace '\\', '/'
    $content = Get-Content -Raw $qqspIni
    $content = [regex]::Replace($content, 'lastGame=.*', "lastGame=$gamePath")
    Set-Content -Path $qqspIni -Value $content -Encoding UTF8
    Write-Host "qqsp.ini lastGame -> $gamePath"
}

& (Join-Path $PSScriptRoot 'build.ps1')

Write-Host ''
Write-Host 'Done. Launch with:'
Write-Host "  $repoRoot\run_game.bat"
Write-Host 'Or open game.qsp in QSP player from this folder.'