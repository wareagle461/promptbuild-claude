@echo off
REM Quick script to run the prompt generator in Docker

echo ============================================================
echo Prompt Generator - Docker CLI
echo ============================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running!
    echo Please start Docker Desktop
    pause
    exit /b 1
)

echo Building Docker image...
docker-compose build prompt-generator-cli

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Starting interactive prompt generator...
echo.
echo Connecting to Ollama at: http://localhost:11434
echo.

docker-compose run --rm prompt-generator-cli

pause
