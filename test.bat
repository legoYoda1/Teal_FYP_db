@REM @echo off
@REM if defined VIRTUAL_ENV (
@REM     echo Python virtual environment is active.
@REM     echo.
@REM ) else (
@REM     echo No Python virtual environment is currently active.
@REM )
call .venv\Scripts\activate
@REM call where python

call python .\etl\test.py
