import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [drawing, setDrawing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const canvasRef = useRef(null);
  const [dimensions, setDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  // Update canvas size on window resize for responsiveness
  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Canvas drawing handlers
  const startDrawing = (e) => {
    setDrawing(true);
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.beginPath();
    const { x, y } = getCursorPosition(e, canvas);
    ctx.moveTo(x, y);
  };

  const draw = (e) => {
    if (!drawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { x, y } = getCursorPosition(e, canvas);
    ctx.lineTo(x, y);
    ctx.strokeStyle = "#fff"; // Changed pen color to white
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";
    ctx.stroke();
  };

  const stopDrawing = () => {
    setDrawing(false);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  // Helper to get mouse/touch position
  const getCursorPosition = (e, canvas) => {
    const rect = canvas.getBoundingClientRect();
    let clientX, clientY;
    if (e.touches) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }
    return {
      x: clientX - rect.left,
      y: clientY - rect.top
    };
  };

  // Configuration from environment variables
  const GCS_BUCKET_NAME = process.env.REACT_APP_GCS_BUCKET_NAME || 'suggestion-screen-images';
  const WHATSAPP_API_URL = process.env.REACT_APP_WHATSAPP_API_URL || 'https://cloudapi.wbbox.in/api/v1.0/messages/send-template';
  const WHATSAPP_AUTH_TOKEN = process.env.REACT_APP_WHATSAPP_AUTH_TOKEN || 'UXdTWf5lhUy7vj6v05hLbw';
  const WHATSAPP_SENDER = process.env.REACT_APP_WHATSAPP_SENDER || '919168616243';
  const WHATSAPP_RECIPIENT = process.env.REACT_APP_WHATSAPP_RECIPIENT || '918623059461';
  const WHATSAPP_TEMPLATE = process.env.REACT_APP_WHATSAPP_TEMPLATE || 'auto_message6';

  // Function to upload image to Google Cloud Storage via simple backend
  const uploadToGCS = async (base64Data) => {
    try {
      const response = await fetch('http://localhost:8001/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_data: base64Data
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('✅ Image uploaded to GCS:', result.url);
        return result.url;
      } else {
        const error = await response.text();
        throw new Error(`GCS upload failed: ${response.status} ${error}`);
      }
    } catch (error) {
      console.error('❌ GCS upload error:', error);
      throw error;
    }
  };

  // Function to send WhatsApp message via backend
  const sendWhatsAppMessage = async (imageUrl) => {
    try {
      const response = await fetch('http://localhost:8001/send-whatsapp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_url: imageUrl
        })
      });

      const result = await response.json();
      
      if (response.ok) {
        console.log('✅ WhatsApp message sent successfully:', result);
        return result;
      } else {
        console.error('❌ WhatsApp API error:', result);
        return { success: false, error: `Backend error: ${response.status}` };
      }
    } catch (error) {
      console.error('❌ WhatsApp service error:', error);
      return { success: false, error: `Network error: ${error.message}` };
    }
  };

  // Function to capture canvas with background color
  const captureCanvasWithBackground = (canvas) => {
    // Create a new canvas with the same dimensions
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    
    // Fill with background color first
    tempCtx.fillStyle = '#050e2eff'; // Same as CSS background
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // Draw the original canvas on top
    tempCtx.drawImage(canvas, 0, 0);
    
    // Return the image with background
    return tempCanvas.toDataURL('image/png');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (isSubmitting) return; // Prevent double submission
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Check if canvas has any content
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const hasContent = imageData.data.some(pixel => pixel !== 0);
    
    if (!hasContent) {
      alert('Please write something on the canvas before submitting!');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // Step 1: Convert canvas to base64 image with background
      const imageDataUrl = captureCanvasWithBackground(canvas);
      console.log('📸 Canvas image captured with background');
      
      // Step 2: Upload to Google Cloud Storage
      console.log('📤 Uploading to Google Cloud Storage...');
      const imageUrl = await uploadToGCS(imageDataUrl);
      
      // Step 3: Send WhatsApp message with image link
      console.log('📱 Sending WhatsApp message...');
      const whatsappResult = await sendWhatsAppMessage(imageUrl);
      
      // Step 4: Show result to user
      if (whatsappResult.success) {
        const successMsg = `✅ Success! Your suggestion has been uploaded and sent via WhatsApp!

Image URL: ${imageUrl}

WhatsApp Results:
• Total Recipients: ${whatsappResult.total_recipients}
• Successful Sends: ${whatsappResult.successful_sends}
• Failed Sends: ${whatsappResult.failed_sends}`;
        
        alert(successMsg);
        clearCanvas();
      } else {
        alert(`⚠️ Partial Success: Image uploaded to ${imageUrl}\nBut WhatsApp sending failed: ${whatsappResult.error}`);
      }
      
    } catch (error) {
      console.error('❌ Error in submission process:', error);
      alert(`❌ Error: ${error.message || 'Failed to process suggestion'}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="App"
      style={{
        minHeight: '100vh',
        height: '100vh',
        width: '100vw',
        overflow: 'hidden',
        background: 'linear-gradient(135deg, #f0f4fd 0%, #d9e7fa 100%)',
        position: 'relative'
      }}
    >
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          border: 'none',
          background: '#050e2eff',
          touchAction: 'none',
          zIndex: 1
        }}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        onTouchStart={startDrawing}
        onTouchMove={draw}
        onTouchEnd={stopDrawing}
      />
      
      {/* Control Buttons */}
      <div style={{
        position: 'absolute',
        bottom: 40,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 2,
        display: 'flex',
        gap: '20px'
      }}>
        <button
          type="button"
          onClick={clearCanvas}
          disabled={isSubmitting}
          style={{
            padding: '15px 30px',
            fontSize: '1.2rem',
            background: '#ff6b6b',
            color: 'white',
            border: 'none',
            borderRadius: 8,
            cursor: isSubmitting ? 'not-allowed' : 'pointer',
            fontWeight: 600,
            opacity: isSubmitting ? 0.6 : 1
          }}
        >
          Clear
        </button>
        
        <button
          type="button"
          onClick={handleSubmit}
          disabled={isSubmitting}
          style={{
            padding: '20px 60px',
            fontSize: '1.5rem',
            background: isSubmitting ? '#ccc' : '#fff',
            color: '#2D5F9A',
            border: 'none',
            borderRadius: 12,
            cursor: isSubmitting ? 'not-allowed' : 'pointer',
            fontWeight: 700,
            letterSpacing: 1,
            boxShadow: '0 4px 16px rgba(45,95,154,0.12)'
          }}
        >
          {isSubmitting ? 'Processing...' : 'Send'}
        </button>
      </div>
      
      <h2
        style={{
          position: 'absolute',
          top: 30,
          left: '50%',
          transform: 'translateX(-50%)',
          color: '#2D5F9A',
          background: '#fafdff',
          padding: '12px 32px',
          borderRadius: 10,
          letterSpacing: 1,
          boxShadow: '0 2px 8px rgba(45,95,154,0.10)',
          zIndex: 2,
          fontSize: '2rem',
          fontWeight: 700,
          margin: 0
        }}
      >
        Suggestion Window
      </h2>
      
      {/* Instructions */}
      <div style={{
        position: 'absolute',
        top: 120,
        left: '50%',
        transform: 'translateX(-50%)',
        color: '#666',
        background: 'rgba(255,255,255,0.9)',
        padding: '8px 20px',
        borderRadius: 8,
        fontSize: '1rem',
        zIndex: 2
      }}>
        Write your suggestion with white text on the canvas
      </div>
    </div>
  );
}

export default App;