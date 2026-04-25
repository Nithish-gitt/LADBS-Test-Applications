@echo off
echo ==========================================
echo Starting Salesforce Permit Management App
echo ==========================================
echo.
echo Starting Backend API on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Starting Frontend on http://localhost:8080
echo.

:: Start Backend API in a new window
start "Backend API" cmd /k "cd /d %~dp0 && python -m uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend Server in a new window
start "Frontend Server" cmd /k "cd /d %~dp0\frontend && python -m http.server 8080"

:: Wait for frontend to start
timeout /t 2 /nobreak >nul

:: Open browser
start http://localhost:8080

echo.
echo ==========================================
echo Application started!
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:8080
echo ==========================================
echo.
echo Press any key to stop all servers...
pause >nul

:: Kill the servers
taskkill /FI "WINDOWTITLE eq Backend API*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend Server*" /F >nul 2>&1
