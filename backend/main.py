"""
Suggestion Screen Wall - Main Backend Application
Handles image submissions, uploads to Google Cloud Storage, and sends via WhatsApp
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
import os
import base64
import logging

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("✅ Environment variables loaded from .env file")
except ImportError:
    logging.warning("⚠️ python-dotenv not installed, using system environment variables")
except Exception as e:
    logging.warning(f"⚠️ Failed to load .env file: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Suggestion Screen Wall API",
    description="API for receiving canvas drawings and sending them via WhatsApp",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment configuration
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://cloudapi.wbbox.in/api/v1.0/messages/send-template")
WHATSAPP_AUTH_TOKEN = os.getenv("WHATSAPP_AUTH_TOKEN", "UXdTWf5lhUy7vj6v05hLbw")
WHATSAPP_SENDER = os.getenv("WHATSAPP_SENDER", "919168616243")
WHATSAPP_RECIPIENT = os.getenv("WHATSAPP_RECIPIENT", "919921059461")
WHATSAPP_TEMPLATE = os.getenv("WHATSAPP_TEMPLATE", "auto_message6")

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "suggestion-screen-images")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Request/Response Models
class SubmissionRequest(BaseModel):
    image_data: str  # Base64 encoded image from canvas
    metadata: Optional[dict] = {}

class SubmissionResponse(BaseModel):
    id: str
    status: str
    message: str
    data: dict

# Services
class GoogleCloudStorageService:
    """Service for uploading images to Google Cloud Storage"""
    
    def __init__(self):
        self.bucket_name = GCS_BUCKET_NAME
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            try:
                from google.cloud import storage
                if GOOGLE_APPLICATION_CREDENTIALS:
                    self._client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
                else:
                    self._client = storage.Client()
                logger.info(f"✅ GCS client initialized for bucket: {self.bucket_name}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize GCS client: {e}")
                raise HTTPException(status_code=500, detail="Cloud storage not available")
        return self._client
    
    def upload_image(self, base64_data: str) -> str:
        """Upload base64 image to GCS and return public URL"""
        try:
            # Remove data URL prefix if present
            if base64_data.startswith('data:image'):
                base64_data = base64_data.split(',')[1]
            
            # Decode image
            image_bytes = base64.b64decode(base64_data)
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"suggestions/canvas_{timestamp}_{unique_id}.png"
            
            # Upload to GCS
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.upload_from_string(image_bytes, content_type='image/png')
            
            # For uniform bucket-level access, we don't use make_public()
            # Instead, the bucket should be configured with public access
            url = f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
            
            logger.info(f"✅ Image uploaded to GCS: {filename}")
            logger.info(f"✅ Public URL: {url}")
            return url
            
        except Exception as e:
            logger.error(f"❌ GCS upload failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

class WhatsAppService:
    """Service for sending messages via WhatsApp API"""
    
    def __init__(self):
        self.api_url = WHATSAPP_API_URL
        self.auth_token = WHATSAPP_AUTH_TOKEN
        self.sender = WHATSAPP_SENDER
        self.template = WHATSAPP_TEMPLATE
    
    def send_image_message(self, recipient: str, image_url: str) -> dict:
        """Send WhatsApp message with image"""
        try:
            import requests
            
            url = f"{self.api_url}/{self.sender}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.auth_token}'
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient,
                "type": "template",
                "template": {
                    "name": self.template,
                    "language": {"code": "en"},
                    "components": [{
                        "type": "header",
                        "parameters": [{
                            "type": "image",
                            "image": {"link": image_url}
                        }]
                    }]
                }
            }
            
            logger.info(f"📱 Sending WhatsApp message to {recipient}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ WhatsApp message sent successfully: {result}")
                return {"success": True, "response": result}
            else:
                error = f"WhatsApp API error: {response.status_code} - {response.text}"
                logger.error(f"❌ {error}")
                return {"success": False, "error": error}
                
        except Exception as e:
            error = f"WhatsApp service error: {str(e)}"
            logger.error(f"❌ {error}")
            return {"success": False, "error": error}

# Initialize services
gcs_service = GoogleCloudStorageService()
whatsapp_service = WhatsAppService()

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Suggestion Screen Wall API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "submit": "/api/submissions"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "gcs_bucket": GCS_BUCKET_NAME,
            "whatsapp_recipient": WHATSAPP_RECIPIENT
        }
    }

@app.post("/api/submissions", response_model=SubmissionResponse)
async def submit_suggestion(submission: SubmissionRequest):
    """
    Main endpoint: Receive canvas drawing, upload to GCS, send via WhatsApp
    """
    submission_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    logger.info(f"📝 New submission received: {submission_id}")
    
    try:
        # Validate image data
        if not submission.image_data or not submission.image_data.strip():
            raise HTTPException(status_code=400, detail="No image data provided")
        
        # Step 1: Upload image to Google Cloud Storage
        logger.info("📤 Uploading image to Google Cloud Storage...")
        image_url = gcs_service.upload_image(submission.image_data)
        
        # Step 2: Send WhatsApp message with image link
        logger.info(f"📱 Sending WhatsApp message to {WHATSAPP_RECIPIENT}...")
        whatsapp_result = whatsapp_service.send_image_message(WHATSAPP_RECIPIENT, image_url)
        
        # Step 3: Prepare response
        if whatsapp_result["success"]:
            response_data = {
                "submission_id": submission_id,
                "image_url": image_url,
                "whatsapp_status": "sent",
                "whatsapp_response": whatsapp_result["response"],
                "recipient": WHATSAPP_RECIPIENT,
                "timestamp": timestamp
            }
            
            logger.info(f"✅ Submission {submission_id} processed successfully")
            
            return SubmissionResponse(
                id=submission_id,
                status="success",
                message="Image uploaded and WhatsApp message sent successfully",
                data=response_data
            )
        else:
            # WhatsApp failed, but image was uploaded
            response_data = {
                "submission_id": submission_id,
                "image_url": image_url,
                "whatsapp_status": "failed",
                "whatsapp_error": whatsapp_result["error"],
                "timestamp": timestamp
            }
            
            return SubmissionResponse(
                id=submission_id,
                status="partial_success",
                message="Image uploaded but WhatsApp sending failed",
                data=response_data
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error processing submission {submission_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/config")
async def get_config():
    """Get current configuration (for debugging)"""
    return {
        "whatsapp": {
            "sender": WHATSAPP_SENDER,
            "recipient": WHATSAPP_RECIPIENT,
            "template": WHATSAPP_TEMPLATE
        },
        "gcs": {
            "bucket": GCS_BUCKET_NAME,
            "credentials_configured": bool(GOOGLE_APPLICATION_CREDENTIALS)
        },
        "environment": "development"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)