#!/bin/bash

# Start Frontend with GCS Upload Server
# Frontend handles WhatsApp, simple backend handles GCS upload only

echo "🚀 Starting Suggestion Screen Wall (Frontend + GCS Upload Server)"
echo "Project root: $(pwd)"
echo ""

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Cleanup complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if we're in the right directory
if [ ! -f "simple-gcs-server.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Required files not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "Starting servers in parallel..."
echo "Press Ctrl+C to stop both servers"
echo ""

# Start simple GCS upload server
echo "=== STARTING GCS UPLOAD SERVER ==="
echo "GCS Upload Server starting on http://localhost:8001"
echo "Endpoint: POST http://localhost:8001/upload"
echo ""

cd /home/jacquewill/AI_Supremacy/sidd-tech-innv/sugg-screen-wall && source .venv/bin/activate && python simple-gcs-server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "=== STARTING FRONTEND ==="
echo "Frontend starting on http://localhost:3000"
echo "Frontend handles: Canvas drawing + WhatsApp API"
echo "Backend handles: GCS upload only"
echo ""

cd frontend && npm start &
FRONTEND_PID=$!

# Wait for both processes
wait
