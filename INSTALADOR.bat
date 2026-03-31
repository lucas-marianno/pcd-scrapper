@echo off
echo ==========================================
echo Starting Project Setup...
echo ==========================================

:: 1. Install Scoop (Requires bypassing execution policy temporarily)
echo [1/5] Installing Scoop...
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

:: 2. Install uv using Scoop
echo [2/5] Installing uv...
call scoop install uv

:: 3. Install dependencies from pyproject.toml
:: 'uv sync' automatically creates the .venv and installs everything
echo [3/5] Syncing dependencies with uv...
call uv sync

:: 4. Activate the virtual environment (Windows equivalent of source .venv/bin/activate)
echo [4/5] Activating virtual environment...
call .venv\Scripts\activate.bat

:: 5. Install Playwright browsers
echo [5/5] Installing Playwright browsers...
call playwright install

echo ==========================================
echo Setup Complete! 
echo ==========================================
pause
