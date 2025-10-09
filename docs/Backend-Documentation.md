# Backend Documentation - Anonymous Suggestion Screen App

## Project Overview

The Anonymous Suggestion Screen App is a web-based platform that allows users to submit anonymous suggestions, inquiries, requests, or feedback. The backend automatically categorizes submissions and provides an admin interface for viewing and managing entries.

## Tech Stack

### Backend Technology Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async MongoDB driver) or PyMongo
- **Authentication**: Simple session-based authentication with bcrypt password hashing
- **Text Classification**: NLTK, spaCy, or scikit-learn
- **Validation**: Pydantic (built-in with FastAPI)
- **Security**: FastAPI security utilities, CORS middleware, rate limiting
- **Environment Management**: python-decouple or python-dotenv
- **Logging**: Python logging or loguru

## Database Schema

### Submissions Collection

```python
{
  "_id": ObjectId,
  "content": str (required, max: 1000 characters),
  "category": str (enum: ['Suggestion', 'Inquiry', 'Request', 'Feedback']),
  "viewed": bool (default: False),
  "created_at": datetime (default: datetime.utcnow),
  "updated_at": datetime,
  "ip_address": str (hashed for privacy),
  "user_agent": str (for analytics, optional),
  "sentiment": str (enum: ['positive', 'neutral', 'negative'], optional)
}
```

### Admin Users Collection (if implementing authentication)

```python
{
  "_id": ObjectId,
  "username": str (required, unique),
  "email": str (required, unique),
  "password_hash": str (required),
  "role": str (enum: ['admin', 'super_admin'], default: 'admin'),
  "last_login": datetime,
  "created_at": datetime (default: datetime.utcnow),
  "is_active": bool (default: True)
}
```

### Admin Sessions Collection (for simple session management)

```python
{
  "_id": ObjectId,
  "admin_id": ObjectId (reference to admin user),
  "session_token": str (unique, random generated),
  "created_at": datetime (default: datetime.utcnow),
  "expires_at": datetime,
  "is_active": bool (default: True)
}
```

## API Endpoints

### Base URL
- `http://localhost:8000/api`

### 1. Submit Suggestion

**Endpoint**: `POST /submissions`

**Description**: Submit a new anonymous suggestion/feedback

**Request Body**:
```json
{
  "content": "This is my suggestion for improving the cafeteria food quality."
}
```

**Validation Rules**:
- `content`: Required, string, min 10 characters, max 1000 characters
- Rate limiting: 5 submissions per IP per hour

**Response** (Success - 201):
```json
{
  "success": true,
  "message": "Submission received successfully",
  "data": {
    "id": "64a7b8c9d1e2f3a4b5c6d7e8",
    "created_at": "2023-10-07T10:30:00.000Z"
  }
}
```

**Response** (Error - 400):
```json
{
  "success": false,
  "message": "Validation error",
  "errors": [
    {
      "field": "content",
      "message": "Content must be between 10 and 1000 characters"
    }
  ]
}
```

### 2. Admin Authentication

**Endpoint**: `POST /auth/login`

**Description**: Admin login to access dashboard

**Request Body**:
```json
{
  "username": "admin",
  "password": "securePassword123"
}
```

**Response** (Success - 200):
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "session_token": "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz",
    "user": {
      "id": "64a7b8c9d1e2f3a4b5c6d7e8",
      "username": "admin",
      "role": "admin"
    },
    "expires_at": "2023-10-08T10:30:00.000Z"
  }
}
```

### 3. Get All Submissions (Admin Only)

**Endpoint**: `GET /admin/submissions`

**Description**: Retrieve all submissions with filtering and pagination

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Query Parameters**:
- `page`: int (default: 1)
- `limit`: int (default: 20, max: 100)
- `category`: str (optional: 'Suggestion', 'Inquiry', 'Request', 'Feedback')
- `viewed`: bool (optional: true/false)
- `sort_by`: str (default: 'created_at', options: 'created_at', 'category')
- `sort_order`: str (default: 'desc', options: 'asc', 'desc')
- `search`: str (optional: search in content)

**Example Request**:
```
GET /admin/submissions?page=1&limit=10&viewed=false&category=Suggestion
```

**Response** (Success - 200):
```json
{
  "success": true,
  "data": {
    "submissions": [
      {
        "id": "64a7b8c9d1e2f3a4b5c6d7e8",
        "content": "This is a suggestion for improvement...",
        "category": "Suggestion",
        "viewed": false,
        "created_at": "2023-10-07T10:30:00.000Z",
        "sentiment": "positive"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 87,
      "itemsPerPage": 10,
      "hasNextPage": true,
      "hasPreviousPage": false
    },
    "stats": {
      "totalUnviewed": 23,
      "categoryCounts": {
        "Suggestion": 45,
        "Inquiry": 20,
        "Request": 15,
        "Feedback": 7
      }
    }
  }
}
```

### 4. Get Single Submission (Admin Only)

**Endpoint**: `GET /admin/submissions/:id`

**Description**: Retrieve a specific submission by ID

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Response** (Success - 200):
```json
{
  "success": true,
  "data": {
    "id": "64a7b8c9d1e2f3a4b5c6d7e8",
    "content": "This is a detailed suggestion...",
    "category": "Suggestion",
    "viewed": false,
    "created_at": "2023-10-07T10:30:00.000Z",
    "updated_at": "2023-10-07T10:30:00.000Z",
    "sentiment": "positive"
  }
}
```

### 5. Mark Submission as Viewed (Admin Only)

**Endpoint**: `PATCH /admin/submissions/:id/view`

**Description**: Mark a submission as viewed

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Response** (Success - 200):
```json
{
  "success": true,
  "message": "Submission marked as viewed",
  "data": {
    "id": "64a7b8c9d1e2f3a4b5c6d7e8",
    "viewed": true,
    "updated_at": "2023-10-07T11:00:00.000Z"
  }
}
```

### 6. Bulk Mark as Viewed (Admin Only)

**Endpoint**: `PATCH /admin/submissions/bulk-view`

**Description**: Mark multiple submissions as viewed

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Request Body**:
```json
{
  "submission_ids": [
    "64a7b8c9d1e2f3a4b5c6d7e8",
    "64a7b8c9d1e2f3a4b5c6d7e9"
  ]
}
```

**Response** (Success - 200):
```json
{
  "success": true,
  "message": "2 submissions marked as viewed",
  "data": {
    "updated_count": 2
  }
}
```

### 7. Delete Submission (Admin Only)

**Endpoint**: `DELETE /admin/submissions/:id`

**Description**: Delete a specific submission

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Response** (Success - 200):
```json
{
  "success": true,
  "message": "Submission deleted successfully"
}
```

### 8. Dashboard Statistics (Admin Only)

**Endpoint**: `GET /admin/dashboard/stats`

**Description**: Get overview statistics for admin dashboard

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Response** (Success - 200):
```json
{
  "success": true,
  "data": {
    "total_submissions": 150,
    "unviewed_count": 25,
    "today_count": 8,
    "week_count": 42,
    "category_breakdown": {
      "Suggestion": 75,
      "Inquiry": 35,
      "Request": 25,
      "Feedback": 15
    },
    "sentiment_breakdown": {
      "positive": 80,
      "neutral": 50,
      "negative": 20
    },
    "recent_activity": [
      {
        "date": "2023-10-07",
        "count": 8
      },
      {
        "date": "2023-10-06",
        "count": 12
      }
    ]
  }
}
```

### 9. Admin Logout

**Endpoint**: `POST /auth/logout`

**Description**: Logout admin and invalidate session

**Authentication**: Required (Session Token in Header: `Authorization: Bearer <session_token>`)

**Response** (Success - 200):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Authentication Flow

### Simple Session-Based Authentication

Instead of JWT tokens, this system uses a simple session-based authentication that's easier to implement:

1. **Login Process**:
   - Admin enters username/password
   - Server verifies password using bcrypt
   - Server generates a random session token (using `secrets.token_urlsafe()`)
   - Session token is stored in database with expiration time
   - Session token is returned to client

2. **Authentication Check**:
   - Client sends session token in Authorization header: `Authorization: Bearer <session_token>`
   - Server looks up session token in database
   - Checks if session is valid and not expired
   - If valid, allows access to protected endpoint

3. **Logout Process**:
   - Client sends session token in logout request
   - Server marks session as inactive in database
   - Session becomes invalid immediately

4. **Session Management**:
   - Sessions expire after 24 hours (configurable)
   - Only one active session per admin user (optional - can be multiple)
   - Expired sessions are automatically cleaned up

### Implementation Example:

```python
import bcrypt
import secrets
from datetime import datetime, timedelta

# Login function
def login_admin(username: str, password: str):
    admin = find_admin_by_username(username)
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin.password_hash):
        # Generate session token
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Store session in database
        create_session(admin.id, session_token, expires_at)
        
        return {
            "session_token": session_token,
            "user": admin,
            "expires_at": expires_at
        }
    return None

# Authentication check
def verify_session(session_token: str):
    session = find_active_session(session_token)
    if session and session.expires_at > datetime.utcnow():
        return session.admin
    return None
```

## Text Classification Logic

### Category Classification Algorithm

The backend should implement intelligent text classification to categorize submissions:

**Keywords and Patterns**:

1. **Suggestion**:
   - Keywords: "suggest", "recommend", "should", "could", "improvement", "better", "enhance"
   - Pattern: Future-oriented language, constructive tone

2. **Inquiry**:
   - Keywords: "question", "ask", "why", "how", "what", "when", "where", "explain"
   - Pattern: Question marks, interrogative words

3. **Request**:
   - Keywords: "need", "want", "please", "request", "require", "can you", "would you"
   - Pattern: Action-oriented language, direct asks

4. **Feedback**:
   - Keywords: "think", "feel", "experience", "opinion", "good", "bad", "excellent", "terrible"
   - Pattern: Past tense, evaluative language

### Implementation Options

1. **Rule-based Classification** (Simple):
```python
def classify_submission(content):
    text = content.lower()
    
    suggestion_score = count_keywords(text, suggestion_keywords)
    inquiry_score = count_keywords(text, inquiry_keywords)
    request_score = count_keywords(text, request_keywords)
    feedback_score = count_keywords(text, feedback_keywords)
    
    max_score = max(suggestion_score, inquiry_score, request_score, feedback_score)
    
    if max_score == 0:
        return 'Feedback'  # default
    if max_score == suggestion_score:
        return 'Suggestion'
    if max_score == inquiry_score:
        return 'Inquiry'
    if max_score == request_score:
        return 'Request'
    return 'Feedback'
```

2. **ML-based Classification** (Advanced):
   - Use OpenAI API for text classification
   - Train a custom model using scikit-learn
   - Use pre-trained models like BERT with transformers library

## Security Considerations

### Rate Limiting
- Implement rate limiting to prevent spam
- 5 submissions per IP per hour
- 100 requests per IP per 15 minutes for API calls

### Data Privacy
- Hash IP addresses before storing
- Don't store any personally identifiable information
- Implement GDPR compliance measures

### Input Validation
- Sanitize all user inputs
- Validate content length and format
- Prevent XSS and injection attacks

### Authentication Security
- Use bcrypt for password hashing
- Implement simple session-based authentication with random session tokens
- Session tokens expire after 24 hours (configurable)
- Store sessions in database for easy management and logout functionality

## Environment Variables

```env
# Server Configuration
PORT=8000
ENVIRONMENT=development

# Database
MONGODB_URI=mongodb://localhost:27017/suggestion_app

# Authentication
SESSION_SECRET=your-super-secret-session-key-here
SESSION_EXPIRES_HOURS=24

# OpenAI (if using for classification)
OPENAI_API_KEY=your-openai-api-key

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_WINDOW_SECONDS=3600
RATE_LIMIT_MAX_REQUESTS=5

# CORS
ALLOWED_ORIGINS=http://localhost:3000
```

## Error Handling

### Standard Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "errors": [
    {
      "field": "fieldName",
      "message": "Specific error message"
    }
  ],
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests (rate limiting)
- 500: Internal Server Error

## Testing Strategy

### Unit Tests
- Test classification algorithm accuracy
- Test validation functions
- Test utility functions

### Integration Tests
- Test API endpoints
- Test database operations
- Test authentication flow

### Load Testing
- Test submission endpoint under load
- Verify rate limiting works correctly
- Test database performance

## Deployment Considerations

### Production Setup
1. Use process manager (PM2)
2. Set up reverse proxy (Nginx)
3. Configure SSL certificates
4. Set up monitoring (Prometheus/Grafana)
5. Implement logging aggregation
6. Set up automated backups

### Scaling Considerations
- Implement caching (Redis) for frequently accessed data
- Consider database indexing for performance
- Implement horizontal scaling if needed
- Use CDN for static assets

## API Documentation
- Use Swagger/OpenAPI for interactive API documentation
- Include Postman collection for testing
- Provide code examples for integration

This documentation provides a comprehensive foundation for implementing the backend of your anonymous suggestion screen app. The system is designed to be scalable, secure, and maintainable while providing all the functionality you specified.