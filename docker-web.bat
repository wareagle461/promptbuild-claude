@echo off
REM Quick script to run the web UI in Docker

echo ============================================================
echo Prompt Generator - Web UI
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
docker-compose build prompt-generator-web

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Starting web UI...
echo.
echo Web UI will be available at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

docker-compose --profile web up prompt-generator-web

REM If user stopped with Ctrl+C, clean up
docker-compose --profile web down
