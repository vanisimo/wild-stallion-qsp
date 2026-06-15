@echo off
setlocal

set "GAME=%~dp0game.qsp"
set "PLAYER=qspgui.exe"

where "%PLAYER%" >nul 2>nul
if errorlevel 1 (
    if exist "C:\Program Files\QSP\qsp590\qspgui.exe" (
        set "PLAYER=C:\Program Files\QSP\qsp590\qspgui.exe"
    ) else if exist "E:\Vano\QSP\qsp590\qspgui.exe" (
        set "PLAYER=E:\Vano\QSP\qsp590\qspgui.exe"
    ) else (
        echo QSP player not found. Install qspgui.exe or add it to PATH.
        pause
        exit /b 1
    )
)

if not exist "%GAME%" (
    echo game.qsp not found. Build the project first.
    pause
    exit /b 1
)

start "" "%PLAYER%" "%GAME%"
