from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.models.driver import DriverStatus


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


class AdminCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


# Driver Management Schemas
class PendingDriverResponse(BaseModel):
    driver_id: int
    user_id: int
    vehicle_number: str
    vehicle_type: str
    is_verified: bool
    status: DriverStatus
    total_rides: int
    total_earnings: float

    class Config:
        from_attributes = True


class VerifyDriverResponse(BaseModel):
    message: str
    driver_id: int
    is_verified: bool


class DeleteDriverResponse(BaseModel):
    message: str
    driver_id: int