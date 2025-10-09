# Suggestion Screen Wall

A complete web application that allows users to draw suggestions on a canvas and automatically sends them via WhatsApp through Google Cloud Storage integration.

## 🚀 Features

- **Canvas Drawing Interface**: Responsive touch/mouse drawing on full-screen canvas
- **Google Cloud Storage Integration**: Automatic image upload with public URL generation
- **WhatsApp API Integration**: Direct image sharing via WhatsApp Business API
- **Unified Startup**: Single command to start both frontend and backend servers
- **Clean Architecture**: Modular services for easy maintenance and scalability

## 🏗️ Architecture

```
Frontend (React) → Backend (FastAPI) → Google Cloud Storage → WhatsApp API
```

### Data Flow
1. User draws on canvas interface
2. Canvas image is captured as base64
3. Backend receives image and uploads to Google Cloud Storage
4. Public image URL is generated
5. WhatsApp message with image is sent via Business API
6. User receives confirmation of successful submission

## 📁 Project Structure

```
sugg-screen-wall/
├── frontend/                 # React application
│   ├── src/
│   │   ├── App.js           # Main canvas component
│   │   ├── App.css          # Styling
│   │   └── index.js         # React entry point
│   └── package.json         # Frontend dependencies
├── backend/                  # FastAPI application
│   ├── main.py              # Main API server
│   ├── services/            # Service modules
│   │   ├── gcs_service.py   # Google Cloud Storage
│   │   └── whatsapp_service.py # WhatsApp API
│   ├── requirements.txt     # Python dependencies
│   └── .env.template        # Environment config template
├── docs/                    # Documentation
│   ├── GCS_SETUP.md        # Google Cloud Storage setup guide
│   └── README.md           # This file
├── tests/                   # Test files
└── start.sh                # Unified startup script
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- Google Cloud Platform account
- WhatsApp Business API access

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd sugg-screen-wall

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install backend dependencies
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 2. Configure Google Cloud Storage

Follow the detailed setup guide in [`docs/GCS_SETUP.md`](docs/GCS_SETUP.md):

1. Create Google Cloud project
2. Enable Cloud Storage API
3. Create service account and download credentials
4. Create storage bucket with public access
5. Set environment variables

### 3. Configure Environment Variables

```bash
# Copy template and edit with your values
cp backend/.env.template backend/.env
```

Edit `backend/.env` with your configuration:
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcs-credentials.json
GCS_BUCKET_NAME=your-bucket-name
WHATSAPP_AUTH_TOKEN=your-whatsapp-token
WHATSAPP_RECIPIENT=recipient-phone-number
```

### 4. Start the Application

```bash
# Make startup script executable
chmod +x start.sh

# Start both frontend and backend servers
./start.sh
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📱 Usage

1. **Draw**: Use mouse or touch to draw your suggestion on the black canvas
2. **Submit**: Click the "Submit Suggestion" button
3. **Confirmation**: Receive confirmation that your image was uploaded and sent via WhatsApp

## 🔧 API Endpoints

### Main Endpoints
- `POST /api/submissions` - Submit canvas drawing for processing
- `GET /health` - Health check endpoint
- `GET /api/config` - View current configuration
- `GET /docs` - Interactive API documentation

### Request Format
```json
{
  "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "metadata": {
    "timestamp": "2024-01-01T00:00:00.000Z",
    "dimensions": {"width": 1920, "height": 1080}
  }
}
```

### Response Format
```json
{
  "id": "uuid-string",
  "status": "success",
  "message": "Image uploaded and WhatsApp message sent successfully",
  "data": {
    "submission_id": "uuid-string",
    "image_url": "https://storage.googleapis.com/bucket/image.png",
    "whatsapp_status": "sent",
    "recipient": "919921059461",
    "timestamp": "2024-01-01T00:00:00.000Z"
  }
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Manual Testing
1. Start the application with `./start.sh`
2. Open http://localhost:3000
3. Draw something on the canvas
4. Submit and verify WhatsApp message is received

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test config endpoint
curl http://localhost:8000/api/config
```

## 🔒 Security Considerations

- **Environment Variables**: Never commit `.env` files or credentials to version control
- **Service Account**: Use minimal required permissions for GCS service account
- **CORS**: Configure appropriate origins for production deployment
- **WhatsApp Token**: Secure your WhatsApp API authentication token

## 🚀 Deployment

### Production Configuration

1. **Environment Setup**:
   ```env
   ENVIRONMENT=production
   WHATSAPP_RECIPIENT=production-phone-number
   GCS_BUCKET_NAME=production-bucket-name
   ```

2. **Security Hardening**:
   - Use environment-specific service accounts
   - Implement rate limiting
   - Add input validation
   - Enable HTTPS

3. **Monitoring**:
   - Set up Google Cloud Monitoring
   - Add application logging
   - Monitor WhatsApp API usage

## 🐛 Troubleshooting

### Common Issues

1. **"Cloud storage not available"**:
   - Check Google Cloud credentials configuration
   - Verify service account permissions
   - Ensure bucket exists and is accessible

2. **"WhatsApp sending failed"**:
   - Verify WhatsApp API token validity
   - Check recipient phone number format
   - Ensure template name is correct

3. **"CORS errors"**:
   - Verify backend is running on port 8000
   - Check CORS configuration in `main.py`

4. **Canvas drawing not working**:
   - Ensure JavaScript is enabled
   - Check browser compatibility
   - Verify touch event handling

### Debug Mode

```bash
# Start with debug logging
cd backend
LOG_LEVEL=DEBUG python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing documentation in `docs/`
- Review API documentation at `/docs` endpoint