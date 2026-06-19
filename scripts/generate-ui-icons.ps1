# Generates colorful 48x48 PNG UI icons for classic QSP player.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$root = Join-Path $PSScriptRoot '..\images\common\ui'
$actRoot = Join-Path $root 'actions'
New-Item -ItemType Directory -Path $root -Force | Out-Null
New-Item -ItemType Directory -Path $actRoot -Force | Out-Null

function New-UiIcon {
    param(
        [string]$Path,
        [string]$BgHtml,
        [string]$AccentHtml,
        [string]$Shape
    )

    $bmp = New-Object System.Drawing.Bitmap 48, 48
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

    $bg = [System.Drawing.ColorTranslator]::FromHtml($BgHtml)
    $accent = [System.Drawing.ColorTranslator]::FromHtml($AccentHtml)
    $light = [System.Drawing.Color]::FromArgb(180, 255, 255, 255)

    $g.Clear($bg)
    $borderPen = New-Object System.Drawing.Pen $light, 2
    $g.DrawRectangle($borderPen, 2, 2, 43, 43)

    $brush = New-Object System.Drawing.SolidBrush $accent
    $pen = New-Object System.Drawing.Pen $accent, 3

    switch ($Shape) {
        'house' {
            $pts = @(
                (New-Object System.Drawing.Point 24, 10),
                (New-Object System.Drawing.Point 38, 22),
                (New-Object System.Drawing.Point 10, 22)
            )
            $g.FillPolygon($brush, $pts)
            $g.FillRectangle($brush, 16, 22, 16, 16)
        }
        'people' {
            $g.FillEllipse($brush, 16, 10, 16, 16)
            $g.FillEllipse($brush, 10, 28, 28, 14)
        }
        'gear' {
            $g.FillEllipse($brush, 14, 14, 20, 20)
            $hole = New-Object System.Drawing.SolidBrush $bg
            $g.FillEllipse($hole, 20, 20, 8, 8)
            for ($i = 0; $i -lt 8; $i++) {
                $g.FillRectangle($brush, 22, 6, 4, 8)
                $g.TranslateTransform(24, 24)
                $g.RotateTransform(45)
                $g.TranslateTransform(-24, -24)
            }
            $g.ResetTransform()
        }
        'clock' {
            $g.DrawEllipse($pen, 10, 10, 28, 28)
            $g.DrawLine($pen, 24, 24, 24, 14)
            $g.DrawLine($pen, 24, 24, 32, 28)
        }
        'hourglass' {
            $g.DrawLine($pen, 14, 10, 34, 10)
            $g.DrawLine($pen, 14, 38, 34, 38)
            $g.DrawLine($pen, 14, 10, 24, 24)
            $g.DrawLine($pen, 34, 10, 24, 24)
            $g.DrawLine($pen, 14, 38, 24, 24)
            $g.DrawLine($pen, 34, 38, 24, 24)
        }
        'eye' {
            $g.DrawEllipse($pen, 8, 18, 32, 14)
            $g.FillEllipse($brush, 20, 20, 8, 8)
        }
        'mug' {
            $g.FillRectangle($brush, 14, 14, 16, 22)
            $g.DrawArc($pen, 28, 18, 10, 12, 270, 180)
        }
        'arrow' {
            $g.DrawLine($pen, 12, 24, 34, 24)
            $g.DrawLine($pen, 28, 18, 34, 24)
            $g.DrawLine($pen, 28, 30, 34, 24)
        }
        'moon' {
            $g.FillEllipse($brush, 12, 12, 24, 24)
            $cut = New-Object System.Drawing.SolidBrush $bg
            $g.FillEllipse($cut, 18, 10, 20, 20)
        }
        'back' {
            $g.DrawLine($pen, 30, 24, 14, 24)
            $g.DrawLine($pen, 20, 18, 14, 24)
            $g.DrawLine($pen, 20, 30, 14, 24)
        }
        'stairs' {
            $g.DrawLine($pen, 12, 34, 12, 18)
            $g.DrawLine($pen, 12, 18, 22, 18)
            $g.DrawLine($pen, 22, 18, 22, 26)
            $g.DrawLine($pen, 22, 26, 32, 26)
            $g.DrawLine($pen, 32, 26, 32, 34)
        }
        'pot' {
            $g.FillEllipse($brush, 12, 24, 24, 10)
            $g.DrawArc($pen, 10, 12, 28, 18, 0, 180)
            $g.DrawLine($pen, 18, 12, 18, 8)
            $g.DrawLine($pen, 30, 12, 30, 8)
        }
        'bubble' {
            $g.DrawEllipse($pen, 10, 12, 24, 16)
            $g.FillEllipse($brush, 14, 16, 6, 6)
            $g.FillEllipse($brush, 24, 16, 6, 6)
            $g.DrawLine($pen, 18, 28, 14, 36)
            $g.DrawLine($pen, 14, 36, 20, 32)
        }
        'box' {
            $g.DrawRectangle($pen, 12, 14, 24, 20)
            $g.DrawLine($pen, 12, 20, 36, 20)
            $g.DrawLine($pen, 24, 14, 24, 34)
        }
        'heart' {
            $g.FillEllipse($brush, 12, 16, 12, 12)
            $g.FillEllipse($brush, 24, 16, 12, 12)
            $pts = @(
                (New-Object System.Drawing.Point 12, 24),
                (New-Object System.Drawing.Point 24, 38),
                (New-Object System.Drawing.Point 36, 24)
            )
            $g.FillPolygon($brush, $pts)
        }
        'kiss' {
            $g.DrawEllipse($pen, 10, 16, 28, 14)
            $g.DrawArc($pen, 16, 20, 8, 6, 200, 140)
            $g.DrawArc($pen, 24, 20, 8, 6, 200, 140)
        }
        'shop' {
            $g.DrawRectangle($pen, 10, 18, 28, 18)
            $g.DrawLine($pen, 10, 18, 24, 10)
            $g.DrawLine($pen, 24, 10, 38, 18)
            $g.FillRectangle($brush, 20, 26, 8, 10)
        }
        'dance' {
            $g.FillEllipse($brush, 20, 10, 8, 8)
            $g.DrawLine($pen, 24, 18, 24, 28)
            $g.DrawLine($pen, 24, 22, 16, 26)
            $g.DrawLine($pen, 24, 22, 32, 24)
            $g.DrawLine($pen, 24, 28, 18, 36)
            $g.DrawLine($pen, 24, 28, 30, 36)
        }
        'scroll' {
            $g.DrawRectangle($pen, 14, 10, 20, 28)
            $g.DrawLine($pen, 18, 16, 30, 16)
            $g.DrawLine($pen, 18, 22, 30, 22)
            $g.DrawLine($pen, 18, 28, 26, 28)
        }
        'cross' {
            $g.DrawLine($pen, 24, 10, 24, 38)
            $g.DrawLine($pen, 14, 18, 34, 18)
        }
        'anchor' {
            $g.DrawEllipse($pen, 18, 8, 12, 8)
            $g.DrawLine($pen, 24, 16, 24, 30)
            $g.DrawLine($pen, 14, 24, 34, 24)
            $g.DrawLine($pen, 16, 34, 32, 34)
            $g.DrawLine($pen, 18, 30, 14, 34)
            $g.DrawLine($pen, 30, 30, 34, 34)
        }
        'hammer' {
            $g.DrawLine($pen, 14, 34, 30, 18)
            $g.FillRectangle($brush, 26, 10, 12, 10)
        }
        'building' {
            $pts = @(
                (New-Object System.Drawing.Point 24, 8),
                (New-Object System.Drawing.Point 36, 18),
                (New-Object System.Drawing.Point 12, 18)
            )
            $g.FillPolygon($brush, $pts)
            $g.FillRectangle($brush, 16, 18, 6, 18)
            $g.FillRectangle($brush, 26, 18, 6, 18)
        }
        'stalls' {
            $g.DrawLine($pen, 8, 28, 8, 16)
            $g.DrawLine($pen, 8, 16, 18, 16)
            $g.DrawLine($pen, 18, 16, 18, 28)
            $g.DrawLine($pen, 22, 28, 22, 14)
            $g.DrawLine($pen, 22, 14, 34, 14)
            $g.DrawLine($pen, 34, 14, 34, 28)
        }
        'shield' {
            $g.DrawEllipse($pen, 12, 10, 24, 28)
            $g.DrawLine($pen, 24, 18, 24, 30)
            $g.DrawLine($pen, 18, 22, 30, 22)
        }
        default {
            $g.FillEllipse($brush, 12, 12, 24, 24)
        }
    }

    $bmp.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

$items = @(
    @{ File = 'family.png';    Bg = '#5c3d2e'; Accent = '#f0c080'; Shape = 'people' },
    @{ File = 'tavern.png';    Bg = '#2f4f2f'; Accent = '#9fd49f'; Shape = 'mug' },
    @{ File = 'staff.png';     Bg = '#3d4a5c'; Accent = '#a8c4f0'; Shape = 'people' },
    @{ File = 'time.png';      Bg = '#4a3d5c'; Accent = '#d8a8f0'; Shape = 'clock' },
    @{ File = 'wait.png';      Bg = '#5c4a2f'; Accent = '#f0d080'; Shape = 'hourglass' },
    @{ File = 'settings.png';  Bg = '#3d3d3d'; Accent = '#d0d0d0'; Shape = 'gear' },
    @{ File = 'debug.png';     Bg = '#5c2f2f'; Accent = '#f08080'; Shape = 'default' }
)

$actions = @(
    @{ File = 'look.png';      Bg = '#2f5f6b'; Accent = '#9fe0ff'; Shape = 'eye' },
    @{ File = 'work.png';      Bg = '#4a5c2f'; Accent = '#d0f080'; Shape = 'mug' },
    @{ File = 'travel.png';    Bg = '#3d4a6b'; Accent = '#a8c8ff'; Shape = 'arrow' },
    @{ File = 'sleep.png';     Bg = '#3d2f5c'; Accent = '#d0b0ff'; Shape = 'moon' },
    @{ File = 'return.png';    Bg = '#5c3d3d'; Accent = '#ffb0b0'; Shape = 'back' },
    @{ File = 'floor.png';     Bg = '#4a4a2f'; Accent = '#f0e080'; Shape = 'stairs' },
    @{ File = 'kitchen.png';   Bg = '#5c3d2f'; Accent = '#ffb070'; Shape = 'pot' },
    @{ File = 'talk.png';      Bg = '#2f4a5c'; Accent = '#90d0f0'; Shape = 'bubble' },
    @{ File = 'gift.png';     Bg = '#5c3d4a'; Accent = '#f0b0d0'; Shape = 'box' },
    @{ File = 'flirt.png';     Bg = '#5c2f4a'; Accent = '#f080b0'; Shape = 'heart' },
    @{ File = 'intim.png';     Bg = '#4a2f5c'; Accent = '#d090f0'; Shape = 'kiss' },
    @{ File = 'shop.png';      Bg = '#4a3d2f'; Accent = '#e8c090'; Shape = 'shop' },
    @{ File = 'dance.png';     Bg = '#3d2f5c'; Accent = '#c0a0f0'; Shape = 'dance' },
    @{ File = 'policy.png';    Bg = '#3d4a4a'; Accent = '#a0d0c0'; Shape = 'scroll' },
    @{ File = 'church.png';   Bg = '#4a3d2f'; Accent = '#e8d090'; Shape = 'cross' },
    @{ File = 'port.png';     Bg = '#2f4a5c'; Accent = '#90d0f0'; Shape = 'anchor' },
    @{ File = 'market.png';   Bg = '#5c4a2f'; Accent = '#f0c880'; Shape = 'stalls' },
    @{ File = 'mayor.png';    Bg = '#4a4a5c'; Accent = '#c0c0f0'; Shape = 'building' },
    @{ File = 'craftsmen.png'; Bg = '#5c3d2f'; Accent = '#d0a070'; Shape = 'hammer' },
    @{ File = 'guard.png';    Bg = '#3d4a5c'; Accent = '#a0b8e0'; Shape = 'shield' },
    @{ File = 'street.png';   Bg = '#4a5c3d'; Accent = '#c0e090'; Shape = 'house' }
)

foreach ($item in $items) {
    $path = Join-Path $root $item.File
    New-UiIcon -Path $path -BgHtml $item.Bg -AccentHtml $item.Accent -Shape $item.Shape
}

foreach ($item in $actions) {
    $path = Join-Path $actRoot $item.File
    New-UiIcon -Path $path -BgHtml $item.Bg -AccentHtml $item.Accent -Shape $item.Shape
}

$portraitThumbRoot = Join-Path $root 'portraits'
New-Item -ItemType Directory -Path $portraitThumbRoot -Force | Out-Null

function Export-PortraitThumb {
    param(
        [string]$SourcePath,
        [string]$DestPath,
        [int]$Size
    )

    if (-not (Test-Path $SourcePath)) {
        return
    }

    $src = [System.Drawing.Image]::FromFile($SourcePath)
    $bmp = New-Object System.Drawing.Bitmap $Size, $Size
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.DrawImage($src, 0, 0, $Size, $Size)
    $bmp.Save($DestPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    $src.Dispose()
}

$portraitSources = Join-Path $PSScriptRoot '..\images\portraits'
Get-ChildItem -Path $portraitSources -Filter '*.png' -File -ErrorAction SilentlyContinue | ForEach-Object {
    $girl = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    $menuThumb = Join-Path $portraitThumbRoot ($girl + '.png')
    $panelThumb = Join-Path $portraitThumbRoot ($girl + '_panel.png')
    Export-PortraitThumb -SourcePath $_.FullName -DestPath $menuThumb -Size 48
    Export-PortraitThumb -SourcePath $_.FullName -DestPath $panelThumb -Size 96
    Write-Host "Portrait thumbs: $girl"
}

Write-Host "UI icons written to $root"