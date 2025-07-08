@echo off
if defined VIRTUAL_ENV (
    echo Python virtual environment is active.
    echo.
) else (
    echo No Python virtual environment is currently active.
    echo Activating the virtual environment...
)

:: Check if venv exists
if not exist .venv\Scripts\activate (
    echo Virtual environment not found. Running create_database.bat...
    call create_database.bat
)

:: Activate the virtual environment
call .venv\Scripts\activate

set FLASK_ENV=development
set FLASK_APP=main.py
set FLASK_DEBUG=1

REM call flask app
REM start cmd /k python .\app\main.py
start cmd /k flask run

timeout /t 1 >nul

REM auto-open dashboard on browser
start http://localhost:5000
