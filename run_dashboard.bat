@echo off
if defined VIRTUAL_ENV (
    echo Python virtual environment is active.
    echo.
) else (
    echo No Python virtual environment is currently active.
)
call.venv\Scripts\activate

REM auto-open dashboard on browser
start http://localhost:5000

REM call flask app
call python .\app\main.py