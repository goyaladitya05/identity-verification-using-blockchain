@echo off
REM Setup script for Windows

echo.
echo ========================================
echo Decentralized Identity Verification Setup
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3.10+ is not installed or not in PATH
    exit /b 1
)

REM Check for Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js 16+ is not installed or not in PATH
    exit /b 1
)

echo [1/5] Creating Python virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate

echo [2/5] Installing Python dependencies...
pip install -r requirements.txt

echo [3/5] Copying .env file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please update with your configuration
)

cd ..

echo [4/5] Installing Node.js dependencies...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update backend\.env with your configuration
echo 2. Start MongoDB: docker run -d -p 27017:27017 --name mongodb mongo
echo 3. Start Ganache: ganache-cli (in another terminal)
echo 4. Start backend: cd backend ^& venv\Scripts\activate ^& python run.py
echo 5. Start frontend: cd frontend ^& npm start
echo.
echo For more details, see QUICKSTART.md
echo.
