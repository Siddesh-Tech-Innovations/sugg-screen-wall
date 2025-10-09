import bcrypt
import secrets
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Header
from database import db
from models import AdminUser

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_session_token() -> str:
    return secrets.token_urlsafe(32)

def get_expiry(hours: int = 24):
    return datetime.utcnow() + timedelta(hours=hours)

async def get_current_user(authorization: str = Header(...)) -> AdminUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    token = authorization.split(" ")[1]
    session = await db.admin_sessions.find_one({"session_token": token, "is_active": True})
    
    if not session or session["expires_at"] <= datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session token")
    
    user = await db.admin_users.find_one({"_id": session["admin_id"]})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return AdminUser(**user)
