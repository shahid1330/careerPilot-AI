@echo off
echo ========================================
echo   STARTING CAREERPILOT AI SERVERS
echo ========================================
echo.

:: Kill existing processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Start Backend
echo [1/2] Starting Backend Server...
start "CareerPilot Backend" cmd /k "cd /d E:\Christ University\Trimester 6\Project\backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

:: Wait for backend to start
timeout /t 5 /nobreak >nul

:: Start Frontend
echo [2/2] Starting Frontend Server...
start "CareerPilot Frontend" cmd /k "cd /d E:\Christ University\Trimester 6\Project\frontend && npm run dev"

echo.
echo ========================================
echo   SERVERS STARTING IN NEW WINDOWS
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
