$ErrorActionPreference = 'Stop'
$root = Join-Path $PSScriptRoot '..\modules'
$files = Get-ChildItem -Path $root -Recurse -Filter '*.qsps'
$count = 0

foreach ($file in $files) {
    $text = [System.IO.File]::ReadAllText($file.FullName)
    $new = $text

    $new = [regex]::Replace($new, "\*pl '<font color=""#606080""><i>(.*?)</i></font>'", {
        param($m)
        $inner = $m.Groups[1].Value -replace "'", "''"
        "gs 'PrintThoughtLine', '$inner'"
    })

    $new = [regex]::Replace($new, "\*p '<font color=""#606080""><i>(.*?)</i></font>'", {
        param($m)
        $inner = $m.Groups[1].Value -replace "'", "''"
        "gs 'PrintThoughtLine', '$inner'"
    })

    if ($new -ne $text) {
        [System.IO.File]::WriteAllText($file.FullName, $new, [System.Text.UTF8Encoding]::new($false))
        $count++
    }
}

Write-Host "Updated $count files"