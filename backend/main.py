from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os

from routes import submissions, admin, auth as auth_router
from exceptions import CustomException, custom_exception_handler
from limiter import limiter

app = FastAPI(title="Suggestion Screen App")

app.state.limiter = limiter

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(submissions.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api/auth")
app.include_router(admin.router, prefix="/api/admin")

app.add_exception_handler(CustomException, custom_exception_handler)

@app.get("/health")
async def health_check():
    return {"status": "ok"}