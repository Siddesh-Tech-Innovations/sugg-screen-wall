"""
Simple GCS Upload + WhatsApp Server
Two endpoints: upload images to GCS and send WhatsApp messages
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import uuid
from datetime import datetime
import os
import requests

app = FastAPI()

# Simple CORS for localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ImageUpload(BaseModel):
    image_data: str

class WhatsAppMessage(BaseModel):
    image_url: str

# WhatsApp Configuration - Multiple Recipients
WHATSAPP_API_URL = "https://cloudapi.wbbox.in/api/v1.0/messages/send-template"
WHATSAPP_AUTH_TOKEN = "UXdTWf5lhUy7vj6v05hLbw"
WHATSAPP_SENDER = "919168616243"
WHATSAPP_RECIPIENTS = [
    "918623059461",  # Original recipient
    # "919145288018",  # Additional recipient 1
    # "919876543210"   # Additional recipient 2 (replace with actual number)
]
WHATSAPP_TEMPLATE = "auto_message6"

@app.post("/upload")
async def upload_image(upload: ImageUpload):
    try:
        from google.cloud import storage
        
        # Initialize client
        client = storage.Client.from_service_account_json(
            '/home/jacquewill/AI_Supremacy/sidd-tech-innv/suggestion-screen-service-account.json'
        )
        
        # Remove data URL prefix
        base64_data = upload.image_data.split(',')[1] if upload.image_data.startswith('data:') else upload.image_data
        
        # Decode image
        image_bytes = base64.b64decode(base64_data)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"suggestions/canvas_{timestamp}_{unique_id}.png"
        
        # Upload to GCS
        bucket = client.bucket('suggestion-screen-images')
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type='image/png')
        
        # Return public URL
        public_url = f"https://storage.googleapis.com/suggestion-screen-images/{filename}"
        
        return {"success": True, "url": public_url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-whatsapp")
async def send_whatsapp_message(message: WhatsAppMessage):
    try:
        url = f"{WHATSAPP_API_URL}/{WHATSAPP_SENDER}"
        results = []
        
        # Send to all recipients
        for recipient in WHATSAPP_RECIPIENTS:
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient,
                "type": "template",
                "template": {
                    "name": WHATSAPP_TEMPLATE,
                    "language": {"code": "en"},
                    "components": [{
                        "type": "header",
                        "parameters": [{
                            "type": "image",
                            "image": {"link": message.image_url}
                        }]
                    }]
                }
            }

            response = requests.post(
                url, 
                json=payload, 
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {WHATSAPP_AUTH_TOKEN}'
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                results.append({
                    "recipient": recipient,
                    "success": True, 
                    "response": result
                })
            else:
                results.append({
                    "recipient": recipient,
                    "success": False, 
                    "error": f"WhatsApp API error: {response.status_code}"
                })
        
        # Check if all successful
        successful_count = sum(1 for r in results if r["success"])
        total_count = len(results)
        
        return {
            "success": successful_count > 0,
            "total_recipients": total_count,
            "successful_sends": successful_count,
            "failed_sends": total_count - successful_count,
            "results": results
        }
            
    except Exception as e:
        return {"success": False, "error": f"WhatsApp service error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)