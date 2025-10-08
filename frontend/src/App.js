import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [drawing, setDrawing] = useState(false);
  const canvasRef = useRef(null);

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
    ctx.strokeStyle = "#2D5F9A"; // Changed to a blue shade
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
        overflow: 'hidden',
        background: 'linear-gradient(135deg, #f0f4fd 0%, #d9e7fa 100%)',
        display: 'flex',                // Add flex
        justifyContent: 'center',       // Center horizontally
        alignItems: 'center'            // Center vertically
      }}
    >
      <header className="App-header" style={{ width: '100%' }}>
        <h2
          style={{
            color: '#2D5F9A',
            background: '#fafdff',
            padding: '12px 0',
            borderRadius: 10,
            marginBottom: 32,
            letterSpacing: 1,
            boxShadow: '0 2px 8px rgba(45,95,154,0.10)'
          }}
        >
          Suggestion Window
        </h2>
        <div
          style={{
            width: 600,
            background: '#fafdff',
            borderRadius: 18,
            boxShadow: '0 6px 32px rgba(45,95,154,0.10)',
            padding: 36,
            margin: '0 auto'
          }}
        >
          <form onSubmit={handleSubmit}>
            <div
              style={{
                marginBottom: 24,
                display: 'flex',
                justifyContent: 'center', // Center horizontally
                alignItems: 'center',     // Center vertically (if needed)
                flexDirection: 'column'
              }}
            >
              <canvas
                ref={canvasRef}
                width={540}
                height={300}
                style={{
                  border: '2px solid #a3bde3',
                  borderRadius: 14,
                  background: '#eaf2fb',
                  touchAction: 'none',
                  boxShadow: '0 2px 8px rgba(45,95,154,0.06)'
                }}
                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={stopDrawing}
                onMouseLeave={stopDrawing}
                onTouchStart={startDrawing}
                onTouchMove={draw}
                onTouchEnd={stopDrawing}
              />
              <div style={{ marginTop: 12, textAlign: 'right', width: '100%' }}>
                <button
                  type="button"
                  onClick={clearCanvas}
                  style={{
                    fontSize: 16,
                    padding: '6px 18px',
                    background: '#a3bde3',
                    color: '#2D5F9A',
                    border: 'none',
                    borderRadius: 6,
                    cursor: 'pointer',
                    fontWeight: 500,
                    transition: 'background 0.2s'
                  }}
                >
                  Clear
                </button>
              </div>
            </div>
            <button
              type="submit"
              style={{
                width: '100%',
                padding: '16px 0',
                fontSize: '1.2rem',
                background: 'linear-gradient(90deg, #2D5F9A 60%, #6CA0DC 100%)',
                color: '#fff',
                border: 'none',
                borderRadius: 8,
                cursor: 'pointer',
                fontWeight: 600,
                letterSpacing: 1,
                boxShadow: '0 2px 8px rgba(45,95,154,0.08)'
              }}
            >
              Send
            </button>
          </form>
        </div>
      </header>
    </div>
  );
}

export default App;