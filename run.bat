@echo off
chcp 65001 >nul
title JWT Authentication Project

echo ========================================
echo     اجرای پروژه JWT Authentication
echo ========================================
echo.

REM راه‌اندازی Backend
echo [Backend] شروع اجرای Backend...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --reload  --port 8000"

REM صبر کردن 3 ثانیه
timeout /t 3 /nobreak >nul

REM راه‌اندازی Frontend
echo [Frontend] شروع اجرای Frontend...
start "Frontend - Angular" cmd /k "cd /d %~dp0frontend && ng serve  --port 4200 --open"

echo.
echo ========================================
echo سرویس‌ها در حال اجرا هستند:
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:4200
echo ========================================
echo.
echo برای خروج این پنجره را ببندید
echo.
pause
