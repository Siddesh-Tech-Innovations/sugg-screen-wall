#!/bin/bash

# Unified Startup Script for Suggestion Screen Wall
# This script starts both frontend and backend servers simultaneously

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting Suggestion Screen Wall Application"
echo "Project root: $PROJECT_ROOT"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo -e "${RED}❌ Virtual environment not found at $PROJECT_ROOT/.venv${NC}"
    echo "Please create a virtual environment first:"
    echo "python3 -m venv .venv"
    echo "source .venv/bin/activate"
    echo "pip install -r backend/requirements.txt"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo -e "${RED}❌ Node modules not found. Installing dependencies...${NC}"
    cd "$PROJECT_ROOT/frontend"
    npm install
    cd "$PROJECT_ROOT"
fi

# Function to run backend
run_backend() {
    echo -e "${BLUE}=== STARTING BACKEND ===${NC}"
    cd "$PROJECT_ROOT/backend"
    
    echo "Activating virtual environment..."
    source "$PROJECT_ROOT/.venv/bin/activate"
    
    echo "Backend starting on http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "Health Check: http://localhost:8000/health"
    echo ""
    
    export PYTHONPATH="$PROJECT_ROOT/backend:$PYTHONPATH"
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to run frontend
run_frontend() {
    echo -e "${GREEN}=== STARTING FRONTEND ===${NC}"
    cd "$PROJECT_ROOT/frontend"
    
    echo "Frontend starting on http://localhost:3000"
    echo "React Dev Server loading..."
    echo ""
    
    npm start
}

# Function to cleanup processes
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down servers...${NC}"
    
    # Kill background processes
    jobs -p | xargs -r kill 2>/dev/null || true
    
    # Kill any remaining uvicorn processes
    pkill -f "uvicorn.*main:app" 2>/dev/null || true
    
    # Kill any remaining npm processes for this project
    pkill -f "npm.*start" 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo -e "${YELLOW}Starting servers in parallel...${NC}"
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
run_backend &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
run_frontend &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID