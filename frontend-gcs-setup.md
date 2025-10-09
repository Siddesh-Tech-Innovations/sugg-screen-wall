# Configure GCS Bucket for Frontend Uploads

Since we're now uploading directly from the frontend, we need to configure the GCS bucket to allow public uploads. Here are the steps:

## Option 1: Using gsutil (Recommended)

```bash
# Make the bucket publicly writable (for uploads)
gsutil iam ch allUsers:objectCreator gs://suggestion-screen-images

# Make the bucket publicly readable (for viewing images)
gsutil iam ch allUsers:objectViewer gs://suggestion-screen-images

# Enable CORS for the bucket to allow browser uploads
gsutil cors set cors-config.json gs://suggestion-screen-images
```

Create `cors-config.json`:
```json
[
  {
    "origin": ["http://localhost:3000", "https://your-domain.com"],
    "method": ["GET", "POST", "PUT", "OPTIONS"],
    "responseHeader": ["Content-Type", "Access-Control-Allow-Origin"],
    "maxAgeSeconds": 3600
  }
]
```

## Option 2: Using Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to Cloud Storage → Buckets
3. Select your bucket: `suggestion-screen-images`
4. Go to **Permissions** tab
5. Click **+ GRANT ACCESS**
6. Add these permissions:
   - Principal: `allUsers`
   - Role: `Storage Object Creator` (for uploads)
   - Role: `Storage Object Viewer` (for public access)

7. Go to **Configuration** tab
8. Scroll to **CORS** section
9. Click **EDIT CORS CONFIGURATION**
10. Add this configuration:
```json
[
  {
    "origin": ["http://localhost:3000"],
    "method": ["GET", "POST", "PUT", "OPTIONS"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
```

## Security Note

⚠️ **Warning**: Making a bucket publicly writable can be a security risk. In production, consider:
- Using signed URLs for uploads
- Implementing proper authentication
- Setting up Cloud Functions for server-side uploads
- Using Firebase Storage instead

## Testing the Configuration

After configuring, test with:
```bash
# Test public upload
curl -X POST \
  "https://storage.googleapis.com/upload/storage/v1/b/suggestion-screen-images/o?uploadType=media&name=test.txt" \
  -H "Content-Type: text/plain" \
  -d "test content"

# Test public read
curl "https://storage.googleapis.com/suggestion-screen-images/test.txt"
```