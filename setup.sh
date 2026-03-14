#!/bin/bash

echo ""
echo "======================================================================"
echo "STUDY TRACKER - COMPLETE SETUP GUIDE"
echo "======================================================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[!] Node.js not installed!"
    echo "Please download from: https://nodejs.org/"
    echo ""
    exit 1
fi

echo "[✓] Node.js found:"
node -v
echo ""

# Install frontend dependencies
echo "[*] Installing React frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "[!] Failed to install npm packages"
    exit 1
fi
cd ..
echo "[✓] Frontend dependencies installed"
echo ""

# Show instructions
echo "======================================================================"
echo "SETUP COMPLETE! Follow these steps:"
echo "======================================================================"
echo ""
echo "STEP 1: Start MySQL Database"
echo "   - Ensure MySQL service is running"
echo ""
echo "STEP 2: Start API Backend (Terminal 1)"
echo "   python api_server.py"
echo ""
echo "STEP 3: Start React Frontend (Terminal 2)"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "The app will open at: http://localhost:3000"
echo "API runs on: http://localhost:5000/api"
echo ""
echo "======================================================================"
echo ""
