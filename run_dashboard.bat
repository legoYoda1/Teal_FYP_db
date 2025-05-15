@echo off
if defined VIRTUAL_ENV (
    echo Python virtual environment is active.
    echo.
) else (
    echo No Python virtual environment is currently active.
)
call.venv\Scripts\activate

REM call flask app
start cmd /k python .\app\main.py

timeout /t 1 >nul

REM auto-open dashboard on browser
start http://localhost:5000
