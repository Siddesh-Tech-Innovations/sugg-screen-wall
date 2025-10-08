import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [drawing, setDrawing] = useState(false);
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

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Handwritten suggestion submitted!');
    clearCanvas();
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
      <button
        type="button"
        onClick={handleSubmit}
        style={{
          position: 'absolute',
          bottom: 40,
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 2,
          padding: '20px 60px',
          fontSize: '1.5rem',
          background: '#fff',
          color: '#2D5F9A',
          border: 'none',
          borderRadius: 12,
          cursor: 'pointer',
          fontWeight: 700,
          letterSpacing: 1,
          boxShadow: '0 4px 16px rgba(45,95,154,0.12)'
        }}
      >
        Send
      </button>
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
    </div>
  );
}

export default App;