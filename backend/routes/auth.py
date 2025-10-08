from fastapi import APIRouter, HTTPException, Depends, Header
from models import AdminLogin, AdminUser, SessionToken
from database import db
from utils.auth import verify_password, create_session_token, get_expiry, get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/login", response_model=SessionToken)
async def login(payload: AdminLogin):
    admin = await db.admin_users.find_one({"username": payload.username})
    if not admin or not verify_password(payload.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_token = create_session_token()
    expires_at = get_expiry()

    await db.admin_sessions.insert_one({
        "admin_id": admin["_id"],
        "session_token": session_token,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "is_active": True
    })

    await db.admin_users.update_one(
        {"_id": admin["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    return SessionToken(
        session_token=session_token,
        user=AdminUser(**admin),
        expires_at=expires_at
    )

@router.post("/logout")
async def logout(authorization: str = Header(...), current_user: AdminUser = Depends(get_current_user)):
    token = authorization.split(" ")[1]
    result = await db.admin_sessions.update_one(
        {"session_token": token},
        {"$set": {"is_active": False}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Invalid session token")

    return {"success": True, "message": "Logged out successfully"}

