/**
 * Minimal Backend for Signed URL Generation
 * This small server only generates signed URLs for GCS uploads
 */

const express = require('express');
const { Storage } = require('@google-cloud/storage');
const cors = require('cors');

const app = express();
const port = 8001; // Different port to avoid conflicts

// Middleware
app.use(cors({
  origin: ['http://localhost:3000'],
  credentials: true
}));
app.use(express.json());

// Initialize GCS
const storage = new Storage({
  keyFilename: '/home/jacquewill/AI_Supremacy/sidd-tech-innv/suggestion-screen-service-account.json',
});

const bucket = storage.bucket('suggestion-screen-images');

// Generate signed URL for upload
app.post('/api/generate-upload-url', async (req, res) => {
  try {
    const { filename, contentType } = req.body;
    
    const options = {
      version: 'v4',
      action: 'write',
      expires: Date.now() + 15 * 60 * 1000, // 15 minutes
      contentType: contentType || 'image/png',
    };

    const [url] = await bucket.file(filename).getSignedUrl(options);
    
    res.json({
      uploadUrl: url,
      publicUrl: `https://storage.googleapis.com/suggestion-screen-images/${filename}`
    });
  } catch (error) {
    console.error('Error generating signed URL:', error);
    res.status(500).json({ error: 'Failed to generate upload URL' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'signed-url-generator' });
});

app.listen(port, () => {
  console.log(`🔗 Signed URL service running on http://localhost:${port}`);
  console.log(`📋 Health check: http://localhost:${port}/health`);
});