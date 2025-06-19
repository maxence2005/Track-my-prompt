@echo off

setlocal enabledelayedexpansion
set "showConsole=false"
for %%A in (%*) do (
    if /I "%%A"=="/V" set "showConsole=true"
)

if "%showConsole%"=="true" (
    python.exe -m track_my_prompt %*
) else (
    start "" pythonw.exe -m track_my_prompt %*
)