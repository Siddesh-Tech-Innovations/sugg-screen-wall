#!/usr/bin/env node

/**
 * Configure GCS Bucket for Frontend Uploads
 * This script sets up the bucket with proper permissions and CORS
 */

const { Storage } = require('@google-cloud/storage');
const path = require('path');

// Configuration
const BUCKET_NAME = 'suggestion-screen-images';
const SERVICE_ACCOUNT_PATH = '/home/jacquewill/AI_Supremacy/sidd-tech-innv/suggestion-screen-service-account.json';

async function configureBucket() {
  try {
    console.log('🔧 Configuring GCS bucket for frontend uploads...');
    
    // Initialize GCS client
    const storage = new Storage({
      keyFilename: SERVICE_ACCOUNT_PATH,
    });
    
    const bucket = storage.bucket(BUCKET_NAME);
    
    // Check if bucket exists
    const [exists] = await bucket.exists();
    if (!exists) {
      console.log(`❌ Bucket ${BUCKET_NAME} does not exist`);
      return;
    }
    
    // Configure CORS
    console.log('📋 Setting CORS configuration...');
    await bucket.setCorsConfiguration([
      {
        origin: ['http://localhost:3000', 'https://your-domain.com', '*'],
        method: ['GET', 'POST', 'PUT', 'OPTIONS', 'HEAD'],
        responseHeader: ['Content-Type', 'Access-Control-Allow-Origin', 'Access-Control-Allow-Headers'],
        maxAgeSeconds: 3600,
      },
    ]);
    
    // Set bucket to public read
    console.log('🔓 Making bucket publicly readable...');
    await bucket.makePublic();
    
    // Set uniform bucket-level access
    console.log('⚙️ Enabling uniform bucket-level access...');
    await bucket.setMetadata({
      iamConfiguration: {
        uniformBucketLevelAccess: {
          enabled: true,
        },
      },
    });
    
    // Add public write permissions (for uploads)
    console.log('✍️ Adding public upload permissions...');
    await bucket.iam.setPolicy({
      bindings: [
        {
          role: 'roles/storage.objectCreator',
          members: ['allUsers'],
        },
        {
          role: 'roles/storage.objectViewer',
          members: ['allUsers'],
        },
      ],
    });
    
    console.log('✅ Bucket configuration complete!');
    console.log(`📦 Bucket: ${BUCKET_NAME}`);
    console.log('🌐 Public read/write access enabled');
    console.log('🔗 CORS configured for localhost:3000');
    
  } catch (error) {
    console.error('❌ Error configuring bucket:', error.message);
    process.exit(1);
  }
}

// Run the configuration
configureBucket();