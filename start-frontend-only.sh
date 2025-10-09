#!/bin/bash

# Frontend-only Suggestion Screen Wall
# This starts only the React frontend (no backend needed)

echo "🚀 Starting Frontend-only Suggestion Screen Wall"
echo "Project root: $(pwd)"
echo ""

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: frontend/package.json not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Start frontend
echo "=== STARTING FRONTEND ONLY ==="
echo "Frontend starting on http://localhost:3000"
echo "No backend required - all functionality is in the frontend!"
echo ""

cd frontend && npm start