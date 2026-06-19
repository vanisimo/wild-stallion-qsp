$ErrorActionPreference = 'Stop'
$root = Join-Path $PSScriptRoot '..\modules'
$files = Get-ChildItem -Path $root -Recurse -Filter '*.qsps' | Where-Object { $_.FullName -notmatch '\\archive\\' }
$count = 0

foreach ($file in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $new = $text

    if ($new -notmatch "gs 'Menu\.Add'") {
        continue
    }

    $new = $new.Replace("gs 'Menu.Add',", "gs 'MenuUiAdd',")

    [System.IO.File]::WriteAllText($file.FullName, $new, [System.Text.UTF8Encoding]::new($false))
    $count++
}

Write-Host "Updated $count menu files"