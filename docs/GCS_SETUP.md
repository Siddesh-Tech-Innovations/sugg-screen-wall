# Google Cloud Storage Setup Guide

## Prerequisites

1. **Google Cloud Account**: Ensure you have a Google Cloud Platform account
2. **Google Cloud SDK**: Install the `gcloud` CLI tool

## Setup Steps

### 1. Create a Google Cloud Project

```bash
# Create a new project (replace PROJECT_ID with your preferred ID)
gcloud projects create suggestion-screen-wall --name="Suggestion Screen Wall"

# Set the project as active
gcloud config set project suggestion-screen-wall
```

### 2. Enable Required APIs

```bash
# Enable Cloud Storage API
gcloud services enable storage.googleapis.com

# Enable Cloud Storage JSON API (if needed)
gcloud services enable storage-api.googleapis.com
```

### 3. Create a Service Account

```bash
# Create service account
gcloud iam service-accounts create suggestion-screen-sa \
    --display-name="Suggestion Screen Service Account" \
    --description="Service account for uploading canvas images"

# Grant necessary permissions
gcloud projects add-iam-policy-binding suggestion-screen-wall \
    --member="serviceAccount:suggestion-screen-sa@suggestion-screen-wall.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
```

### 4. Create and Download Service Account Key

```bash
# Create and download service account key
gcloud iam service-accounts keys create ./gcs-credentials.json \
    --iam-account=suggestion-screen-sa@suggestion-screen-wall.iam.gserviceaccount.com
```

### 5. Create Storage Bucket

```bash
# Create bucket (replace BUCKET_NAME with your preferred name)
gsutil mb -p suggestion-screen-wall gs://suggestion-screen-images

# Set bucket to publicly accessible for uploaded objects
gsutil iam ch allUsers:objectViewer gs://suggestion-screen-images
```

### 6. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
# Google Cloud Storage Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcs-credentials.json
GCS_BUCKET_NAME=suggestion-screen-images

# WhatsApp Configuration
WHATSAPP_API_URL=https://cloudapi.wbbox.in/api/v1.0/messages/send-template
WHATSAPP_AUTH_TOKEN=UXdTWf5lhUy7vj6v05hLbw
WHATSAPP_SENDER=919168616243
WHATSAPP_RECIPIENT=919921059461
WHATSAPP_TEMPLATE=auto_message6
```

## Testing the Setup

### 1. Test GCS Authentication

```bash
# Test authentication
gsutil ls

# Test bucket access
gsutil ls gs://suggestion-screen-images
```

### 2. Test Python GCS Integration

```python
from google.cloud import storage

# Initialize client
client = storage.Client.from_service_account_json('path/to/gcs-credentials.json')

# List buckets
for bucket in client.list_buckets():
    print(bucket.name)
```

## Alternative Setup Methods

### Method 1: Using Default Credentials (Recommended for Development)

```bash
# Authenticate with your user account
gcloud auth application-default login

# Set the project
gcloud config set project suggestion-screen-wall
```

Then in your code, simply use:
```python
from google.cloud import storage
client = storage.Client()  # Will use default credentials
```

### Method 2: Using Environment Variable

```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/gcs-credentials.json"
```

## Troubleshooting

### Common Issues:

1. **Permission Denied**: Ensure service account has `roles/storage.admin` or `roles/storage.objectAdmin`
2. **Bucket Not Found**: Verify bucket name and project settings
3. **Authentication Failed**: Check credentials file path and content

### Verification Commands:

```bash
# Check current project
gcloud config get-value project

# Check authentication
gcloud auth list

# Test bucket access
gsutil ls gs://suggestion-screen-images

# Upload test file
echo "test" > test.txt
gsutil cp test.txt gs://suggestion-screen-images/
gsutil rm gs://suggestion-screen-images/test.txt
```

## Security Notes

- Keep your service account key file secure and never commit it to version control
- Consider using workload identity or other more secure authentication methods in production
- Set appropriate IAM policies to limit access scope
- Use bucket lifecycle policies to manage storage costs

## Cost Optimization

- Set up lifecycle policies to delete old images after a certain period
- Use nearline or coldline storage for archival purposes
- Monitor usage with Cloud Monitoring