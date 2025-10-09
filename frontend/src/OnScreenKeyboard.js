import React from 'react';
import './OnScreenKeyboard.css';

const KEYS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
  ['Space']
];

function OnScreenKeyboard({ onKeyPress }) {
  return (
    <div className="keyboard-container">
      {KEYS.map((row, rowIndex) => (
        <div key={rowIndex} className="keyboard-row">
          {row.map((key) => (
            <button
              key={key}
              type="button"
              className="keyboard-key"
              onClick={() => onKeyPress(key === 'Space' ? ' ' : key)}
            >
              {key === 'Space' ? '␣' : key}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}

export default OnScreenKeyboard;
