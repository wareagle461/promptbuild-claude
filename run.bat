@echo off
chcp 65001 >nul
REM Windows batch script to run the prompt generator

echo Starting Uncensored Prompt Generator...
echo.

REM Check if Python is installed (try py first, then python)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)

python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)

echo Error: Python is not installed or not in PATH
echo Please install Python 3.7+ from python.org
pause
exit /b 1

:python_found
echo Found Python: %PYTHON_CMD%
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Warning: Ollama doesn't seem to be running
    echo Please start Ollama or run: ollama serve
    echo.
    pause
)

REM Run the prompt generator
%PYTHON_CMD% prompt_generator.py %*

pause
