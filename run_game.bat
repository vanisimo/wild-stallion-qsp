@echo off
setlocal

set "GAME=%~dp0game.qsp"
set "PLAYER="

if exist "C:\Program Files\QSP\qsp590\qspgui.exe" (
    set "PLAYER=C:\Program Files\QSP\qsp590\qspgui.exe"
) else if exist "C:\Program Files\QSP\bin\qspgui.exe" (
    set "PLAYER=C:\Program Files\QSP\bin\qspgui.exe"
) else if exist "D:\QSP\qsp590\qspgui.exe" (
    set "PLAYER=D:\QSP\qsp590\qspgui.exe"
) else if exist "E:\Vano\QSP\qsp590\qspgui.exe" (
    set "PLAYER=E:\Vano\QSP\qsp590\qspgui.exe"
) else (
    where qspgui.exe >nul 2>nul
    if not errorlevel 1 (
        set "PLAYER=qspgui.exe"
    )
)

if "%PLAYER%"=="" (
    echo QSP player not found. Install QSP 5.90 or set path in run_game.bat.
    pause
    exit /b 1
)

if not exist "%GAME%" (
    echo game.qsp not found. Build the project first.
    pause
    exit /b 1
)

start "" "%PLAYER%" "%GAME%"
