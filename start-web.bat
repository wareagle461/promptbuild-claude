@echo off
chcp 65001 >nul
echo ============================================================
echo Starting Prompt Generator Web UI
echo ============================================================
echo.

docker-compose up -d prompt-generator-web

if errorlevel 1 (
    echo.
    echo Failed to start web UI!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Web UI Started Successfully!
echo ============================================================
echo.
echo Open your browser to: http://localhost:8080
echo.
echo To stop: docker-compose down
echo To view logs: docker-compose logs -f prompt-generator-web
echo.
pause
