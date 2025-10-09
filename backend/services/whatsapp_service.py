"""
WhatsApp API service for sending template messages with images.
"""
import requests
import os
from typing import Optional

class WhatsAppService:
    def __init__(self, base_url: str, auth_token: str, sender_number: str):
        """
        Initialize WhatsApp service
        
        Args:
            base_url: Base URL for WhatsApp API (e.g., 'https://cloudapi.wbbox.in/api/v1.0/messages/send-template')
            auth_token: Bearer token for authentication
            sender_number: Sender WhatsApp number (e.g., '919168616243')
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.sender_number = sender_number
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }
    
    def send_image_template(self, recipient_number: str, image_url: str, template_name: str = "auto_message6") -> dict:
        """
        Send WhatsApp template message with image
        
        Args:
            recipient_number: Recipient's WhatsApp number (e.g., '919921059461')
            image_url: Public URL of the image to send
            template_name: Template name to use
            
        Returns:
            API response dict
        """
        try:
            # Construct full API URL
            url = f"{self.base_url}/{self.sender_number}"
            
            # Prepare message payload
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": "en"
                    },
                    "components": [
                        {
                            "type": "header",
                            "parameters": [
                                {
                                    "type": "image",
                                    "image": {
                                        "link": image_url
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
            
            print(f"📱 Sending WhatsApp message to {recipient_number}")
            print(f"🖼️ Image URL: {image_url}")
            print(f"📝 Template: {template_name}")
            
            # Send POST request
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                print(f"✅ WhatsApp message sent successfully!")
                print(f"📋 Response: {result}")
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response": result
                }
            else:
                error_msg = f"WhatsApp API error: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": error_msg,
                    "response": response.text
                }
                
        except requests.exceptions.Timeout:
            error_msg = "WhatsApp API request timed out"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"WhatsApp API request failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
        
        except Exception as e:
            error_msg = f"Unexpected error sending WhatsApp message: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

# Singleton instance
_whatsapp_service = None

def get_whatsapp_service() -> WhatsAppService:
    """Get or create WhatsApp service instance"""
    global _whatsapp_service
    
    if _whatsapp_service is None:
        # Get configuration from environment variables
        base_url = os.getenv('WHATSAPP_API_URL', 'https://cloudapi.wbbox.in/api/v1.0/messages/send-template')
        auth_token = os.getenv('WHATSAPP_AUTH_TOKEN', 'UXdTWf5lhUy7vj6v05hLbw')
        sender_number = os.getenv('WHATSAPP_SENDER_NUMBER', '919168616243')
        
        _whatsapp_service = WhatsAppService(base_url, auth_token, sender_number)
        print(f"✅ WhatsApp service initialized for sender: {sender_number}")
    
    return _whatsapp_service

def send_suggestion_image(recipient_number: str, image_url: str) -> dict:
    """
    Convenience function to send suggestion image via WhatsApp
    
    Args:
        recipient_number: Recipient's WhatsApp number
        image_url: Public URL of the suggestion image
        
    Returns:
        Result dict with success status and details
    """
    service = get_whatsapp_service()
    return service.send_image_template(recipient_number, image_url)