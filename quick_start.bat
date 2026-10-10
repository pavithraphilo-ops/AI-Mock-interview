@echo off
REM Quick Start Script for AI Mock Interview System (Windows)
REM This script sets up the development environment

echo ==========================================
echo AI Mock Interview System - Quick Start
echo ==========================================
echo.

REM Check Python version
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    pause
    exit /b 1
)
echo ^✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% equ 0 (
    echo ^✓ Virtual environment created
) else (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% equ 0 (
    echo ^✓ Virtual environment activated
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo ^✓ Dependencies installed successfully
) else (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Create .env file
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo ^✓ .env file created from template
    echo.
    echo ⚠️  IMPORTANT: Update .env with your Gemini API key
    echo    1. Visit: https://makersuite.google.com/app/apikeys
    echo    2. Get your API key
    echo    3. Edit .env and add: GEMINI_API_KEY=your_key_here
    echo.
) else (
    echo ^✓ .env file already exists
)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env and add your Gemini API key
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
echo For more information, see README.md
echo.
pause
