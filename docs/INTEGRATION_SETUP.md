# Frontend-Backend Integration Setup Guide

## Quick Start

### 1. Backend Setup

1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

2. Environment Setup
Create a `.env` file in the backend directory:
```env
MONGODB_URI=mongodb://localhost:27017/suggestion_app
PORT=8000
ENVIRONMENT=development
```

3. Start Backend Server
```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

1. Install Dependencies
```bash
cd frontend
npm install
```

2. Start Frontend Server
```bash
npm start
```

The frontend will run on `http://localhost:3000` and automatically connect to the backend at `http://localhost:8000`.

## How It Works

### Frontend Changes
- Canvas Drawing: Users draw on a full-screen canvas
- Image Capture: When "Send" is clicked, the canvas is converted to a base64 PNG image
- API Request: The image data is sent to `/api/submissions` endpoint
- Error Handling: Displays success/error messages to the user

### Backend Changes
- New Model: `SubmissionCreate` now accepts `image_data` instead of `content`
- OCR Processing: Images are processed to extract text (currently using placeholder)
- Validation: Extracted text is validated before saving
- Response: Returns the extracted text along with submission confirmation

## OCR Implementation Options

### Option 1: Simple Placeholder (Current)
- Located in `utils/ocr_simple.py`
- Returns a placeholder message for now
- Good for testing the integration

### Option 2: Tesseract OCR (Free)
1. Install Tesseract:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt install tesseract-ocr`

2. Install Python package:
```bash
pip install pytesseract
```

3. Update `utils/ocr_simple.py` to use the full OCR implementation in `utils/ocr.py`

### Option 3: Google Cloud Vision API (Recommended)
1. Set up Google Cloud project and enable Vision API
2. Download service account key
3. Install package:
```bash
pip install google-cloud-vision
```
4. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

### Option 4: OpenAI Vision API
1. Get OpenAI API key
2. Install package:
```bash
pip install openai
```
3. Add to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Testing the Integration

1. Start both servers (backend on :8000, frontend on :3000)
2. Open browser to `http://localhost:3000`
3. Draw something on the canvas
4. Click "Send" button
5. Check response - should see success message
6. Verify in database - check if submission was saved

## API Endpoint Details

### POST /api/submissions

Request Body:
```json
{
  "image_data": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

Success Response (201):
```json
{
  "success": true,
  "message": "Submission received successfully",
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "created_at": "2023-10-07T10:30:00.000Z",
    "extracted_text": "This is the extracted text from the image"
  }
}
```

Error Response (400):
```json
{
  "detail": "No text could be extracted from the image. Please try writing more clearly."
}
```

## Next Steps

1. Choose OCR Method: Decide between Tesseract, Google Vision, or OpenAI
2. Implement Real OCR: Replace the placeholder in `ocr_simple.py`
3. Test Handwriting: Test with various handwriting samples
4. Improve Accuracy: Fine-tune image preprocessing for better OCR results
5. Add Admin Panel: Connect the existing admin routes to a frontend

## Troubleshooting

### Common Issues

1. CORS Errors: Make sure backend CORS is configured for frontend URL
2. Canvas Empty: Check if canvas has content before submitting
3. OCR Errors: Ensure OCR service is properly configured
4. Database Connection: Verify MongoDB is running and connection string is correct

### Frontend Debugging
```javascript
// Add to handleSubmit for debugging
console.log('Canvas content:', hasContent);
console.log('Image data length:', imageDataUrl.length);
```

### Backend Debugging
```python
# Add to submissions.py for debugging
print(f"Received image data length: {len(submission.image_data)}")
print(f"Extracted text: {extracted_text}")
```

## Architecture Overview

```
┌─────────────────┐    HTTP POST     ┌─────────────────┐
│                 │   image_data     │                 │
│   React App     │ ──────────────►  │   FastAPI       │
│   (Canvas UI)   │                  │   Backend       │
│                 │ ◄────────────────│                 │
└─────────────────┘   JSON Response  └─────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │   OCR Service   │
                                     │  (Extract Text) │
                                     └─────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │    MongoDB      │
                                     │   (Store Data)  │
                                     └─────────────────┘
```

This setup gives you a solid foundation for connecting your handwriting canvas to the backend with OCR processing.