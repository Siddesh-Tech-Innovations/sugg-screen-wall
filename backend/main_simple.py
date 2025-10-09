from fastapi import FastAPI, HTTPExceptionfrom fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddlewarefrom fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModelfrom pydantic import BaseModel

from typing import Optionalfrom typing import Optional

import uuidimport uuid

from datetime import datetimefrom datetime import datetime

import osimport os



# Import our services# Import our services

from services.gcs_service import upload_image_to_gcsfrom services.gcs_service import upload_image_to_gcs

from services.whatsapp_service import send_suggestion_imagefrom services.whatsapp_service import send_suggestion_image



app = FastAPI(title="Suggestion Screen App - WhatsApp Integration")app = FastAPI(title="Suggestion Screen App - WhatsApp Integration")



# Add CORS middleware# Add CORS middleware

app.add_middleware(app.add_middleware(

    CORSMiddleware,    CORSMiddleware,

    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app

    allow_credentials=True,    allow_credentials=True,

    allow_methods=["*"],    allow_methods=["*"],

    allow_headers=["*"],    allow_headers=["*"],

))



# Configuration from environment variables# Configuration from environment variables

WHATSAPP_RECIPIENT = os.getenv('WHATSAPP_RECIPIENT_NUMBER', '919921059461')  # Default recipientWHATSAPP_RECIPIENT = os.getenv('WHATSAPP_RECIPIENT_NUMBER', '919921059461')  # Default recipient



# Pydantic models for request/responsetry:

class SubmissionCreate(BaseModel):

    image_data: Optional[str] = ""  # Base64 encoded image# Add CORS middleware    from utils.ocr_huggingface import extract_text_with_huggingface as extract_text_from_image, validate_extracted_text

    content: Optional[str] = ""  # Optional text content

    category: Optional[str] = "general"app.add_middleware(    print("✅ Using enhanced Hugging Face OCR system")



class SubmissionResponse(BaseModel):    CORSMiddleware,except ImportError as e:

    id: str

    status: str    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app    print(f"⚠️ Hugging Face OCR unavailable: {e}")

    message: str

    data: dict    allow_credentials=True,    from utils.ocr_simple import extract_text_from_image, validate_extracted_text



@app.get("/")    allow_methods=["*"],    print("🔄 Falling back to simple OCR system")

async def root():

    return {"message": "Suggestion Screen Wall API - WhatsApp Integration"}    allow_headers=["*"],



@app.get("/health"))app = FastAPI(title="Suggestion Screen App")

async def health_check():

    return {"status": "healthy", "timestamp": datetime.now().isoformat()}



@app.post("/api/submissions", response_model=SubmissionResponse)# Pydantic models for request/response# Pydantic models for request/response

async def create_submission(submission: SubmissionCreate):

    """class SubmissionCreate(BaseModel):class SubmissionCreate(BaseModel):

    Receive image submission, upload to Google Cloud Storage, and send via WhatsApp

    """    image_data: Optional[str] = ""  # Base64 encoded image    image_data: Optional[str] = ""  # Base64 encoded image (optional)

    try:

        submission_id = str(uuid.uuid4())    content: Optional[str] = ""  # Optional text content    content: Optional[str] = ""  # Optional text content

        timestamp = datetime.now().isoformat()

            category: Optional[str] = "general"    category: Optional[str] = "general"

        print(f"📝 Received new submission: {submission_id}")

        

        # Check if image data is provided

        image_received = bool(submission.image_data and submission.image_data.strip())class SubmissionResponse(BaseModel):class SubmissionResponse(BaseModel):

        

        if not image_received:    id: str    id: str

            response_data = {

                "submission_id": submission_id,    status: str    status: str

                "image_received": False,

                "error": "No image data provided",    message: str    message: str

                "timestamp": timestamp

            }    data: dict    data: dict  # Contains the response data

            print(f"⚠️ No image data in submission {submission_id}")

            

            return SubmissionResponse(

                id=submission_id,@app.get("/")# Add CORS middleware

                status="error",

                message="No image data provided",async def root():app.add_middleware(

                data=response_data

            )    return {"message": "Suggestion Screen Wall API - WhatsApp Integration"}    CORSMiddleware,

        

        print(f"🖼️ Processing image for submission {submission_id}")    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app

        

        # Upload image to Google Cloud Storage@app.get("/health")    allow_credentials=True,

        try:

            print("📤 Uploading image to Google Cloud Storage...")async def health_check():    allow_methods=["*"],

            image_url = upload_image_to_gcs(submission.image_data)

            print(f"✅ Image uploaded successfully: {image_url}")    return {"status": "healthy", "timestamp": datetime.now().isoformat()}    allow_headers=["*"],

            

        except Exception as gcs_error:)

            print(f"❌ GCS upload failed: {gcs_error}")

            response_data = {@app.post("/api/submissions", response_model=SubmissionResponse)

                "submission_id": submission_id,

                "image_received": True,async def create_submission(submission: SubmissionCreate):@app.get("/")

                "gcs_upload": "failed",

                "gcs_error": str(gcs_error),    """async def root():

                "timestamp": timestamp

            }    Receive image submission, upload to Google Cloud Storage, and send via WhatsApp    return {"message": "Suggestion Screen Wall API"}

            

            return SubmissionResponse(    """

                id=submission_id,

                status="error",    try:@app.get("/health")

                message="Failed to upload image to cloud storage",

                data=response_data        submission_id = str(uuid.uuid4())async def health_check():

            )

                timestamp = datetime.now().isoformat()    return {"status": "ok", "message": "Backend is running!"}

        # Send WhatsApp message with the image

        try:        

            print(f"📱 Sending WhatsApp message to {WHATSAPP_RECIPIENT}...")

            whatsapp_result = send_suggestion_image(WHATSAPP_RECIPIENT, image_url)        print(f"📝 Received new submission: {submission_id}")@app.get("/api/test")

            

            if whatsapp_result["success"]:        async def test_endpoint():

                print("✅ WhatsApp message sent successfully!")

                response_data = {        # Check if image data is provided    return {"message": "API is working!", "frontend_url": "http://localhost:3000"}

                    "submission_id": submission_id,

                    "image_received": True,        image_received = bool(submission.image_data and submission.image_data.strip())

                    "gcs_upload": "success",

                    "image_url": image_url,        @app.post("/api/submissions", response_model=SubmissionResponse)

                    "whatsapp_sent": "success",

                    "whatsapp_response": whatsapp_result.get("response"),        if image_received:async def create_submission(submission: SubmissionCreate):

                    "recipient": WHATSAPP_RECIPIENT,

                    "timestamp": timestamp            print(f"🖼️ Image data received, processing for WhatsApp...")    """Handle suggestion submissions from the frontend"""

                }

                                try:

                return SubmissionResponse(

                    id=submission_id,            # TODO: Upload image to Google Cloud Storage        # Generate a unique ID and timestamp

                    status="success",

                    message="Image uploaded and WhatsApp message sent successfully",            # image_url = upload_to_gcs(submission.image_data)        submission_id = str(uuid.uuid4())

                    data=response_data

                )                    timestamp = datetime.now().isoformat()

            else:

                print(f"❌ WhatsApp sending failed: {whatsapp_result.get('error')}")            # TODO: Send WhatsApp message with image        

                response_data = {

                    "submission_id": submission_id,            # whatsapp_result = send_whatsapp_message(image_url)        # Check if image data is provided

                    "image_received": True,

                    "gcs_upload": "success",                    image_received = bool(submission.image_data and len(submission.image_data) > 0)

                    "image_url": image_url,

                    "whatsapp_sent": "failed",            # For now, simulate the process        

                    "whatsapp_error": whatsapp_result.get("error"),

                    "timestamp": timestamp            response_data = {        # Extract text using OCR if image is provided

                }

                                "submission_id": submission_id,        extracted_text = ""

                return SubmissionResponse(

                    id=submission_id,                "image_received": True,        if image_received:

                    status="partial_success",

                    message="Image uploaded but WhatsApp sending failed",                "gcs_upload": "pending",            print(f"🔍 Starting OCR processing for submission {submission_id}")

                    data=response_data

                )                "whatsapp_sent": "pending",            extracted_text = extract_text_from_image(submission.image_data)

                

        except Exception as whatsapp_error:                "timestamp": timestamp            

            print(f"❌ WhatsApp service error: {whatsapp_error}")

            response_data = {            }            # Validate the extracted text

                "submission_id": submission_id,

                "image_received": True,                        is_valid, validation_message = validate_extracted_text(extracted_text)

                "gcs_upload": "success",

                "image_url": image_url,            print(f"✅ Submission {submission_id} processed successfully")            if not is_valid:

                "whatsapp_sent": "error",

                "whatsapp_error": str(whatsapp_error),                            print(f"⚠️ OCR validation failed: {validation_message}")

                "timestamp": timestamp

            }        else:                extracted_text = f"OCR processed but validation failed: {validation_message}"

            

            return SubmissionResponse(            response_data = {        

                id=submission_id,

                status="partial_success",                "submission_id": submission_id,        # Use provided content or OCR result

                message="Image uploaded but WhatsApp service encountered an error",

                data=response_data                "image_received": False,        if submission.content and submission.content.strip():

            )

                        "error": "No image data provided",            content_description = submission.content.strip()

    except Exception as e:

        print(f"❌ Error processing submission: {e}")                "timestamp": timestamp        elif extracted_text:

        raise HTTPException(status_code=500, detail=f"Failed to process submission: {str(e)}")

            }            content_description = extracted_text

@app.get("/api/submissions")

async def get_submissions():            print(f"⚠️ No image data in submission {submission_id}")        else:

    """Get all submissions (placeholder for now)"""

    return {                    content_description = "No content provided"

        "submissions": [],

        "total": 0,        return SubmissionResponse(        

        "message": "WhatsApp integration - submissions not stored locally"

    }            id=submission_id,        # For now, just return success response



@app.get("/api/config")            status="success",        # In a real app, you'd save this to a database and process the image

async def get_config():

    """Get current configuration (for debugging)"""            message="Submission received successfully",        response = SubmissionResponse(

    return {

        "whatsapp_recipient": WHATSAPP_RECIPIENT,            data=response_data            id=submission_id,

        "gcs_bucket": os.getenv('GCS_BUCKET_NAME', 'suggestion-screen-images'),

        "whatsapp_sender": os.getenv('WHATSAPP_SENDER_NUMBER', '919168616243'),        )            status="success",

        "environment": "development"

    }                    message="Suggestion received successfully",



if __name__ == "__main__":    except Exception as e:            data={

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)        print(f"❌ Error processing submission: {e}")                "extracted_text": content_description,

        raise HTTPException(status_code=500, detail="Failed to process submission")                "image_received": image_received,

                "ocr_processed": image_received,

@app.get("/api/submissions")                "category": submission.category,

async def get_submissions():                "timestamp": timestamp,

    """Get all submissions (placeholder for now)"""                "submission_id": submission_id

    return {            }

        "submissions": [],        )

        "total": 0,        

        "message": "WhatsApp integration - submissions not stored locally"        print(f"📝 New suggestion received:")

    }        print(f"   ID: {submission_id}")

        print(f"   Category: {submission.category}")

if __name__ == "__main__":        print(f"   Image received: {image_received}")

    import uvicorn        if image_received:

    uvicorn.run(app, host="0.0.0.0", port=8000)            print(f"   OCR processed: ✅")
            print(f"   Extracted text: '{content_description}'")
        else:
            print(f"   Text content: '{content_description}'")
        print(f"   Timestamp: {timestamp}")
        print("=" * 60)
        
        return response
        
    except Exception as e:
        print(f"❌ Error processing submission: {e}")
        raise HTTPException(status_code=500, detail="Failed to process submission")

@app.get("/api/submissions")
async def get_submissions():
    """Get all submissions (placeholder for now)"""
    return {
        "submissions": [],
        "total": 0,
        "message": "No submissions yet - this is a demo endpoint"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)