from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class VerifyOtp(BaseModel):
    email: EmailStr
    otp: str
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"