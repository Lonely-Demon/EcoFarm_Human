from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = "en"

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    supabase_id: str
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None

    class Config:
        orm_mode = True
