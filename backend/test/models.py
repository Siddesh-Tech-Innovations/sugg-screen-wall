from pydantic import BaseModel, Field, conlist
from datetime import datetime
from typing import List, Optional, Any
from bson import ObjectId

# Request Body Models
class SubmissionCreate(BaseModel):
    content: str = Field(..., min_length=10, max_length=1000, description="Content must be between 10 and 1000 characters")

class BulkViewUpdate(BaseModel):
    submission_ids: conlist(str, min_length=1)

# Database Models
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class SubmissionInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    content: str
    category: str
    viewed: bool
    created_at: datetime
    updated_at: datetime
    ip_address: str
    user_agent: str
    sentiment: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AdminUser(BaseModel):
    username: str
    disabled: Optional[bool] = None