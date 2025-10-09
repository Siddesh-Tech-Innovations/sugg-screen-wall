# 🚀 Suggestion Screen Wall - Development Setup

This project consists of a **FastAPI backend** and a **React frontend**. Use the provided scripts to easily start both services for development.

## 📋 Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 14+** and **npm** (for frontend)
- **Git** (for version control)

## 🎯 Quick Start

### Option 1: Use the Development Script (Recommended)

```bash
# Run both backend and frontend
./start-dev.sh

# Or use the simpler version (better for VS Code)
./start-simple.sh
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment (if not exists)
python3 -m venv .

# Activate virtual environment
source bin/activate  # Linux/Mac
# OR
source Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies (if not installed)
npm install

# Start the development server
npm start
```

## 🔗 Access Points

Once both services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
sugg-screen-wall/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application entry
│   ├── requirements.txt
│   ├── routes/       # API routes
│   ├── utils/        # Utility functions
│   └── test/         # Backend tests
├── frontend/         # React frontend
│   ├── src/          # React source code
│   ├── public/       # Static files
│   └── package.json  # Node.js dependencies
├── docs/             # Documentation
├── start-dev.sh      # Full development startup script
└── start-simple.sh   # Simple startup script
```

## 🛠️ Development Scripts

### `start-dev.sh`
- Comprehensive script with environment detection
- Handles virtual environment setup
- Opens separate terminals for each service
- Includes port checking and error handling

### `start-simple.sh`
- Interactive script for VS Code and similar environments
- Choose to run backend only, frontend only, or both
- Better for integrated terminals

### Usage Examples

```bash
# Start both services interactively
./start-simple.sh

# Start only backend
./start-simple.sh backend

# Start only frontend  
./start-simple.sh frontend
```

## 🐛 Troubleshooting

### Port Already in Use
If you get port conflicts:
```bash
# Check what's using the ports
sudo lsof -i :3000  # Frontend
sudo lsof -i :8000  # Backend

# Kill processes if needed
sudo kill -9 <PID>
```

### Python Virtual Environment Issues
```bash
# Recreate virtual environment
cd backend
rm -rf bin/ lib/ include/ pyvenv.cfg  # Linux/Mac
# OR  
rm -rf Scripts/ Lib/ pyvenv.cfg       # Windows

python3 -m venv .
source bin/activate  # or Scripts/activate on Windows
pip install -r requirements.txt
```

### Node.js Dependency Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🔧 Environment Variables

Create a `.env` file in the backend directory for configuration:
```env
# Example .env file
DATABASE_URL=mongodb://localhost:27017/suggestion_screen
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 🚦 API Endpoints

Key backend endpoints:
- `GET /health` - Health check
- `POST /api/submissions` - Create submission
- `GET /api/submissions` - Get submissions
- `POST /api/auth/login` - User authentication
- `GET /api/admin/*` - Admin routes

See full API documentation at http://localhost:8000/docs when running.

## 🎉 Happy Coding!

Both services should now be running and communicating with each other. The React frontend will proxy API requests to the FastAPI backend automatically.