import base64
import io
from PIL import Image
import cv2
import numpy as np
from typing import Optional
import os

# For this implementation, I'll provide multiple OCR options
# You can choose one based on your needs and available resources

def extract_text_from_image(image_data: str) -> str:
    """
    Extract text from base64 encoded image data using OCR.
    
    Args:
        image_data: Base64 encoded image data (with or without data URL prefix)
    
    Returns:
        Extracted text string
    """
    try:
        # Remove data URL prefix if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess image for better OCR results
        processed_image = preprocess_image(image)
        
        # Try different OCR methods in order of preference
        text = ""
        
        # Method 1: Try Google Cloud Vision API (recommended for production)
        text = extract_with_google_vision(processed_image)
        if text.strip():
            return text.strip()
        
        # Method 2: Try Tesseract OCR (free alternative)
        text = extract_with_tesseract(processed_image)
        if text.strip():
            return text.strip()
        
        # Method 3: Try OpenAI Vision API (if available)
        text = extract_with_openai_vision(processed_image)
        if text.strip():
            return text.strip()
        
        return "Unable to extract text from the image. Please try writing more clearly."
        
    except Exception as e:
        print(f"Error in text extraction: {str(e)}")
        return "Error processing the handwritten text. Please try again."

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image to improve OCR accuracy.
    """
    # Convert PIL image to OpenCV format
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Invert if background is dark (which seems to be your case)
    # Check if image is mostly dark
    if np.mean(thresh) < 127:
        thresh = cv2.bitwise_not(thresh)
    
    # Apply morphological operations to clean up the image
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Convert back to PIL Image
    return Image.fromarray(cleaned)

def extract_with_google_vision(image: Image.Image) -> str:
    """
    Extract text using Google Cloud Vision API.
    Requires: pip install google-cloud-vision
    """
    try:
        from google.cloud import vision
        
        # Initialize the client
        client = vision.ImageAnnotatorClient()
        
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create Vision API image object
        vision_image = vision.Image(content=img_byte_arr)
        
        # Perform text detection
        response = client.text_detection(image=vision_image)
        texts = response.text_annotations
        
        if texts:
            return texts[0].description
        
        return ""
        
    except ImportError:
        print("Google Cloud Vision not available. Install with: pip install google-cloud-vision")
        return ""
    except Exception as e:
        print(f"Google Vision API error: {str(e)}")
        return ""

def extract_with_tesseract(image: Image.Image) -> str:
    """
    Extract text using Tesseract OCR.
    Requires: pip install pytesseract
    And Tesseract binary installed on system
    """
    try:
        import pytesseract
        
        # Configure Tesseract for handwriting
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?:;\'\" '
        
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
        
    except ImportError:
        print("Tesseract not available. Install with: pip install pytesseract")
        return ""
    except Exception as e:
        print(f"Tesseract OCR error: {str(e)}")
        return ""

def extract_with_openai_vision(image: Image.Image) -> str:
    """
    Extract text using OpenAI Vision API.
    Requires: pip install openai
    """
    try:
        import openai
        
        # Convert image to base64
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        image_b64 = base64.b64encode(img_byte_arr).decode()
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract and return only the handwritten text from this image. If no clear text is visible, return an empty string."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        print("OpenAI not available. Install with: pip install openai")
        return ""
    except Exception as e:
        print(f"OpenAI Vision API error: {str(e)}")
        return ""

def validate_extracted_text(text: str) -> tuple[bool, str]:
    """
    Validate if extracted text meets submission requirements.
    
    Returns:
        (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "No text could be extracted from the image. Please try writing more clearly."
    
    text = text.strip()
    
    if len(text) < 10:
        return False, "Extracted text is too short. Please write at least 10 characters."
    
    if len(text) > 1000:
        return False, "Extracted text is too long. Please keep it under 1000 characters."
    
    return True, ""