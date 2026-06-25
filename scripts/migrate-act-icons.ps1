$ErrorActionPreference = 'Stop'
$python = Join-Path $PSScriptRoot 'migrate-act-icons.py'
python $python @args