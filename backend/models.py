from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Any, Optional, List
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema
from pydantic.json_schema import GetJsonSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        return {"type": "string"}

# ========== SUBMISSION ==========

class SubmissionCreate(BaseModel):
    content: str = Field(..., min_length=10, max_length=1000)

class SubmissionSuccessData(BaseModel):
    id: str
    created_at: datetime

class SubmissionSuccessResponse(BaseModel):
    success: bool = True
    message: str = "Submission received successfully"
    data: SubmissionSuccessData


class SubmissionInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    content: str
    category: str
    sentiment: Optional[str]
    viewed: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

# ========== ADMIN ==========

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUser(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    role: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

# ========== SESSION ==========

class SessionToken(BaseModel):
    session_token: str
    user: AdminUser
    expires_at: datetime

# ========== BULK VIEW ==========
class BulkViewUpdate(BaseModel):
    submission_ids: List[str]
