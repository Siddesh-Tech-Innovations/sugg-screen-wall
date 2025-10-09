from fastapi import APIRouter, Request, HTTPException, status
from models import SubmissionCreate, SubmissionSuccessResponse, SubmissionSuccessData
from database import db
from datetime import datetime
from utils.classify import classify_submission, hash_ip
from utils.ocr_simple import extract_text_from_image, validate_extracted_text
from user_agents import parse as parse_user_agent
from limiter import limiter

router = APIRouter()

@router.post("/submissions", status_code=status.HTTP_201_CREATED, response_model=SubmissionSuccessResponse)
@limiter.limit("5/hour")
async def submit_suggestion(request: Request, submission: SubmissionCreate):
    ip = request.client.host
    ip_hashed = hash_ip(ip)
    ua = request.headers.get("user-agent", "")
    user_agent = parse_user_agent(ua).ua_string[:255]

    try:
        # Extract text from the image
        extracted_text = extract_text_from_image(submission.image_data)
        
        # Validate extracted text
        is_valid, error_message = validate_extracted_text(extracted_text)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        content = extracted_text.strip()
        category = classify_submission(content)
        sentiment = "neutral"  # Placeholder

        doc = {
            "content": content,
            "category": category,
            "viewed": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "ip_address": ip_hashed,
            "user_agent": user_agent,
            "sentiment": sentiment
        }

        result = await db.submissions.insert_one(doc)

        return SubmissionSuccessResponse(
            data=SubmissionSuccessData(
                id=str(result.inserted_id),
                created_at=doc["created_at"],
                extracted_text=content
            ))
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing submission: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing handwritten text. Please try again."
        )
