@echo off
if defined VIRTUAL_ENV (
    echo Python virtual environment is active.
    echo.
) else (
    echo No Python virtual environment is currently active.
)
call.venv\Scripts\activate
@REM call where python

call python .\etl\test.py
