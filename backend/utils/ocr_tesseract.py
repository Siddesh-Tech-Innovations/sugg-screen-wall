"""
Production-ready OCR implementation using Tesseract OCR.
This is a free alternative that works well for handwritten text.
"""
import base64
import io
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from typing import Optional
import os

def extract_text_from_image(image_data: str) -> str:
    """
    Extract text from base64 encoded image data using Tesseract OCR.
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
        processed_image = preprocess_handwriting_image(image)
        
        # Try to extract text using Tesseract
        text = extract_with_tesseract(processed_image)
        
        if text and text.strip():
            return text.strip()
        else:
            return "Unable to extract clear text from the handwriting. Please try writing more clearly."
        
    except Exception as e:
        print(f"Error in text extraction: {str(e)}")
        return "Error processing the handwritten text. Please try again."

def preprocess_handwriting_image(image: Image.Image) -> Image.Image:
    """
    Advanced preprocessing specifically for handwritten text on dark background.
    """
    # Convert PIL image to OpenCV format
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Since your canvas has a dark background (#050e2eff) with white text,
    # we need to invert the image
    inverted = cv2.bitwise_not(gray)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(inverted, (3, 3), 0)
    
    # Apply threshold to get clean binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Apply morphological operations to clean up
    kernel = np.ones((2, 2), np.uint8)
    
    # Remove noise
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPENING, kernel, iterations=1)
    
    # Close gaps in letters
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # Dilate to make text slightly thicker (helps with OCR)
    dilated = cv2.dilate(closing, kernel, iterations=1)
    
    # Convert back to PIL Image
    result_image = Image.fromarray(dilated)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(result_image)
    result_image = enhancer.enhance(2.0)
    
    # Resize image if it's too small (OCR works better on larger images)
    width, height = result_image.size
    if width < 300 or height < 100:
        scale_factor = max(300/width, 100/height, 2)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        result_image = result_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return result_image

def extract_with_tesseract(image: Image.Image) -> str:
    """
    Extract text using Tesseract OCR with configuration optimized for handwriting.
    """
    try:
        import pytesseract
        
        # Configuration for handwritten text
        # --psm 6: Uniform block of text
        # --psm 8: Single text line
        # --psm 13: Raw line. Treat the image as a single text line
        custom_configs = [
            r'--oem 3 --psm 6',  # Uniform block of text
            r'--oem 3 --psm 8',  # Single text line
            r'--oem 3 --psm 13', # Raw line
        ]
        
        best_text = ""
        max_confidence = 0
        
        for config in custom_configs:
            try:
                # Get text with confidence
                data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
                
                # Calculate average confidence
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                if confidences:
                    avg_confidence = sum(confidences) / len(confidences)
                    
                    # Get text
                    text = pytesseract.image_to_string(image, config=config).strip()
                    
                    if text and avg_confidence > max_confidence:
                        max_confidence = avg_confidence
                        best_text = text
                        
            except Exception as e:
                print(f"Config {config} failed: {str(e)}")
                continue
        
        return best_text if best_text else pytesseract.image_to_string(image).strip()
        
    except ImportError:
        print("Tesseract not available. Install with: pip install pytesseract")
        print("Also install Tesseract binary on your system")
        return "OCR service not available. Please install Tesseract."
    except Exception as e:
        print(f"Tesseract OCR error: {str(e)}")
        return ""

def validate_extracted_text(text: str) -> tuple[bool, str]:
    """
    Validate if extracted text meets submission requirements.
    """
    if not text or not text.strip():
        return False, "No text could be extracted from the image. Please try writing more clearly."
    
    text = text.strip()
    
    # Check for common OCR artifacts that indicate poor recognition
    if len(text) < 3:
        return False, "Extracted text is too short. Please write more clearly or larger."
    
    # Check if text is mostly special characters (indicates poor OCR)
    special_char_ratio = sum(1 for c in text if not c.isalnum() and not c.isspace()) / len(text)
    if special_char_ratio > 0.5:
        return False, "Text recognition unclear. Please write more clearly."
    
    if len(text) > 1000:
        return False, "Extracted text is too long. Please keep it under 1000 characters."
    
    # Allow shorter text for handwriting (minimum 3 characters instead of 10)
    if len(text) < 3:
        return False, "Please write at least a few characters."
    
    return True, ""

# Fallback function for when Tesseract is not available
def extract_text_fallback(image_data: str) -> str:
    """
    Fallback method when OCR is not available.
    """
    return "OCR processing is not configured. Please contact administrator to set up text recognition."