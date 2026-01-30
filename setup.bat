@echo off
REM DesignAudit AI - Complete Setup Script (Windows)
REM This script sets up the entire development environment

setlocal enabledelayedexpansion

echo.
echo DesignAudit AI - Development Setup
echo ===================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo ^✓ .env created
    echo WARNING: Please update .env with your API keys
    echo.
)

REM Setup Backend
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -q -r requirements.txt
echo ^✓ Backend dependencies installed

cd ..

REM Setup Frontend
echo.
echo Setting up Frontend...
cd frontend

echo Installing frontend dependencies...
npm install --silent
echo ^✓ Frontend dependencies installed

cd ..

echo.
echo ^✓ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your API keys:
echo    - OPENAI_API_KEY
echo    - DATABASE_URL (if using PostgreSQL)
echo    - AWS credentials (if using S3)
echo.
echo 2. Start the services:
echo    Option A - With Docker Compose:
echo      docker-compose up -d
echo.
echo    Option B - Manually:
echo      Terminal 1 - Backend:
echo        cd backend
echo        venv\Scripts\activate.bat
echo        python main.py
echo.
echo      Terminal 2 - Frontend:
echo        cd frontend
echo        npm run dev
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo Documentation:
echo - README.md - Project overview
echo - QUICK_START.md - Quick reference
echo - BLUEPRINT.md - Feature specifications
echo - docs/ - Detailed documentation
