# schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., example="Alice")
    email: EmailStr = Field(..., example="alice@example.com")
    password: str = Field(..., min_length=6, example="strongpassword123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="alice@example.com")
    password: str = Field(..., example="strongpassword123")

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., example="bearer")
    expires_in: int = Field(..., example=3600)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True