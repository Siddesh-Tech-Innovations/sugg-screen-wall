"""
Google Cloud Storage service for uploading images and getting public URLs.
"""
import base64
import io
import uuid
from datetime import datetime
from google.cloud import storage
from PIL import Image
import os

class GCSImageUploader:
    def __init__(self, bucket_name: str, credentials_path: str = None):
        """
        Initialize GCS uploader
        
        Args:
            bucket_name: Name of the GCS bucket
            credentials_path: Path to service account JSON file (optional, can use env vars)
        """
        self.bucket_name = bucket_name
        
        # Initialize GCS client
        if credentials_path and os.path.exists(credentials_path):
            self.client = storage.Client.from_service_account_json(credentials_path)
        else:
            # Use default credentials (from env var GOOGLE_APPLICATION_CREDENTIALS)
            self.client = storage.Client()
        
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_base64_image(self, base64_data: str, folder: str = "suggestions") -> str:
        """
        Upload base64 image to GCS and return public URL
        
        Args:
            base64_data: Base64 encoded image data
            folder: Folder path in the bucket
            
        Returns:
            Public URL of the uploaded image
        """
        try:
            # Remove data URL prefix if present
            if base64_data.startswith('data:image'):
                base64_data = base64_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(base64_data)
            
            # Determine image format
            image = Image.open(io.BytesIO(image_bytes))
            image_format = image.format.lower() if image.format else 'png'
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{folder}/suggestion_{timestamp}_{unique_id}.{image_format}"
            
            # Upload to GCS
            blob = self.bucket.blob(filename)
            blob.upload_from_string(
                image_bytes,
                content_type=f'image/{image_format}'
            )
            
            # Make the blob publicly viewable
            blob.make_public()
            
            # Return public URL
            public_url = blob.public_url
            
            print(f"✅ Image uploaded to GCS: {filename}")
            print(f"🔗 Public URL: {public_url}")
            
            return public_url
            
        except Exception as e:
            print(f"❌ Failed to upload image to GCS: {e}")
            raise Exception(f"GCS upload failed: {str(e)}")
    
    def delete_image(self, image_url: str) -> bool:
        """
        Delete image from GCS using its public URL
        
        Args:
            image_url: Public URL of the image
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # Extract blob name from URL
            blob_name = image_url.split(f"{self.bucket_name}/")[-1]
            blob = self.bucket.blob(blob_name)
            blob.delete()
            
            print(f"✅ Image deleted from GCS: {blob_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete image from GCS: {e}")
            return False

# Singleton instance (will be configured with actual credentials)
_gcs_uploader = None

def get_gcs_uploader(bucket_name: str = None, credentials_path: str = None):
    """Get or create GCS uploader instance"""
    global _gcs_uploader
    
    if _gcs_uploader is None:
        if not bucket_name:
            # Use environment variable or default
            bucket_name = os.getenv('GCS_BUCKET_NAME', 'suggestion-screen-images')
        
        credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        
        try:
            _gcs_uploader = GCSImageUploader(bucket_name, credentials_path)
            print(f"✅ GCS uploader initialized for bucket: {bucket_name}")
        except Exception as e:
            print(f"❌ Failed to initialize GCS uploader: {e}")
            raise
    
    return _gcs_uploader

def upload_image_to_gcs(base64_data: str) -> str:
    """
    Convenience function to upload image and get URL
    
    Args:
        base64_data: Base64 encoded image data
        
    Returns:
        Public URL of uploaded image
    """
    uploader = get_gcs_uploader()
    return uploader.upload_base64_image(base64_data)