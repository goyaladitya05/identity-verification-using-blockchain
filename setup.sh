#!/bin/bash

# Setup script for macOS and Linux

echo ""
echo "========================================"
echo "Decentralized Identity Verification Setup"
echo "========================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3.10+ is not installed"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js 16+ is not installed"
    exit 1
fi

echo "[1/5] Creating Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "[2/5] Installing Python dependencies..."
pip install -r requirements.txt

echo "[3/5] Copying .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - please update with your configuration"
fi

cd ..

echo "[4/5] Installing Node.js dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Start MongoDB: docker run -d -p 27017:27017 --name mongodb mongo"
echo "3. Start Ganache: ganache-cli (in another terminal)"
echo "4. Start backend: cd backend && source venv/bin/activate && python run.py"
echo "5. Start frontend: cd frontend && npm start"
echo ""
echo "For more details, see QUICKSTART.md"
echo ""
