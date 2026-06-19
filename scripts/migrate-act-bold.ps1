$ErrorActionPreference = 'Stop'
$root = Join-Path $PSScriptRoot '..\modules'
$files = Get-ChildItem -Path $root -Recurse -Filter '*.qsps' | Where-Object { $_.FullName -notmatch '\\archive\\' }
$count = 0

function Wrap-ActLabel([string]$label) {
    if ($label -match '<b>|<B>') { return $label }
    return '<b>' + $label + '</b>'
}

foreach ($file in $files) {
    $text = [System.IO.File]::ReadAllText($file.FullName)
    $new = $text

    $new = [regex]::Replace($new, "act\s+'([^']*)':", {
        param($m)
        $label = Wrap-ActLabel $m.Groups[1].Value
        $escaped = $label -replace "'", "''"
        "act '$escaped':"
    })

    $new = [regex]::Replace($new, 'act\s+"([^"]*)":', {
        param($m)
        $label = Wrap-ActLabel $m.Groups[1].Value
        'act "' + ($label -replace '"', '""') + '":'
    })

    $new = [regex]::Replace($new, "act\s+'([^']*)',\s*'([^']*)':", {
        param($m)
        $label = Wrap-ActLabel $m.Groups[1].Value
        $icon = $m.Groups[2].Value
        $escaped = $label -replace "'", "''"
        "act '$escaped', '$icon':"
    })

    $new = [regex]::Replace($new, 'act\s+"([^"]*)",\s*"([^"]*)":', {
        param($m)
        $label = Wrap-ActLabel $m.Groups[1].Value
        $icon = $m.Groups[2].Value
        'act "' + ($label -replace '"', '""') + '", "' + $icon + '":'
    })

    if ($new -ne $text) {
        [System.IO.File]::WriteAllText($file.FullName, $new, [System.Text.UTF8Encoding]::new($false))
        $count++
    }
}

Write-Host "Updated $count act files"