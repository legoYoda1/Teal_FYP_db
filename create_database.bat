@echo off
setlocal

REM Check if virtual environment exists
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo.
    echo ⚠️  Virtual environment not found. Creating one using uv...
    
    REM Check if uv is installed
    where uv >nul 2>&1
    if errorlevel 1 (
        echo ❌ 'uv' is not installed. Please install it first using: pip install uv
        exit /b 1
    )

    REM Create virtual environment
    uv venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment.
        exit /b 1
    )

    REM Install dependencies
    uv pip install -r uv.lock
    if errorlevel 1 (
        echo ❌ Failed to install dependencies from uv.lock.
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Run ETL scripts
call python .\etl\create_database.py
if errorlevel 1 (
    echo ❌ Failed to create database.
    exit /b 1
)

call python .\etl\create_query_db.py
if errorlevel 1 (
    echo ❌ Failed to create query database.
    exit /b 1
)

echo ✅ All tasks completed successfully.
