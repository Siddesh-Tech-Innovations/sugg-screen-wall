# Suggestion Screen Wall - Windows Setup

A simple web application for capturing handwritten suggestions and sending them via WhatsApp.

## 🚀 Quick Start (Windows)

### Prerequisites
1. **Python 3.8+** - Download from [python.org](https://python.org)
2. **Node.js** - Download from [nodejs.org](https://nodejs.org)
3. **Google Cloud Service Account** - Place `suggestion-screen-service-account.json` in the parent directory

### Installation & Running

#### Option 1: Batch Script (Recommended)
1. Extract the project zip file
2. Place your `suggestion-screen-service-account.json` file in the parent directory
3. Double-click `run-windows.bat`
4. Follow the on-screen instructions

#### Option 2: PowerShell Script
1. Extract the project zip file
2. Place your `suggestion-screen-service-account.json` file in the parent directory
3. Right-click on `run-windows.ps1` → "Run with PowerShell"
4. If you get execution policy errors, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### What the Scripts Do

✅ **Automatic Setup:**
- Check for Python and Node.js installation
- Create Python virtual environment
- Install all required dependencies (Python & Node.js)
- Verify service account file location

✅ **Automatic Launch:**
- Start backend server (localhost:8001)
- Start frontend server (localhost:3000)
- Open both in separate windows

✅ **Automatic Cleanup:**
- Stop servers when you close the script
- Clean shutdown on Ctrl+C

## 📁 Directory Structure

```
parent-directory/
├── suggestion-screen-service-account.json  ← Your GCS credentials
└── sugg-screen-wall/                       ← Project folder
    ├── run-windows.bat                     ← Windows batch script
    ├── run-windows.ps1                     ← PowerShell script
    ├── simple-gcs-server.py               ← Backend server
    ├── frontend/                           ← React app
    └── ...
```

## 🎨 Usage

1. Open your browser to `http://localhost:3000`
2. Draw your suggestion on the canvas
3. Click "Submit Suggestion"
4. Your drawing will be:
   - Uploaded to Google Cloud Storage
   - Sent via WhatsApp to configured recipients

## ⚙️ Configuration

Edit `simple-gcs-server.py` to modify:
- WhatsApp recipients
- WhatsApp template
- GCS bucket name

```python
WHATSAPP_RECIPIENTS = [
    "918623059461",  # Recipient 1
    "919921059461",  # Recipient 2
    "YOUR_NUMBER"    # Add more recipients
]
```

## 🔧 Troubleshooting

### Common Issues:

**"Python not found"**
- Install Python from python.org
- Make sure "Add to PATH" is checked during installation

**"Node.js not found"**
- Install Node.js from nodejs.org
- Restart your computer after installation

**"Service account file not found"**
- Make sure `suggestion-screen-service-account.json` is in the parent directory
- Check the file name spelling

**"Port already in use"**
- Close any existing servers
- Restart your computer if needed

### Manual Installation:

If the automated scripts don't work, you can install manually:

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.venv\Scripts\activate.bat

# 3. Install Python dependencies
pip install fastapi uvicorn google-cloud-storage requests

# 4. Install Node.js dependencies
cd frontend
npm install
cd ..

# 5. Start backend (in one terminal)
python simple-gcs-server.py

# 6. Start frontend (in another terminal)
cd frontend
npm start
```

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Ensure all prerequisites are installed
3. Verify the service account file is in the correct location
4. Make sure ports 3000 and 8001 are not in use

## 🎉 Features

- **Canvas Drawing**: Touch and mouse support
- **Background Preservation**: Dark blue background maintained in saved images
- **Multiple Recipients**: Send to multiple WhatsApp numbers
- **Automatic Upload**: Direct integration with Google Cloud Storage
- **Real-time Feedback**: Status updates during processing