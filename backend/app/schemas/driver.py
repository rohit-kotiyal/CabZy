from pydantic import BaseModel, Field
from typing import Optional
from app.models.driver import DriverStatus



class LocationUpdateRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    lng: float = Field(..., ge=-180, le=180, description="Longitude coordinate")


class StatusUpdateRequest(BaseModel):
    status: DriverStatus


class DriverRegistrationRequest(BaseModel):
    vehicle_number: str = Field(..., min_length=1, max_length=50, description="Vehicle registration number")
    vehicle_type: str = Field(..., min_length=1, max_length=50, description="Type of vehicle (e.g., sedan, suv, hatchback)")


# Response Schemas
class DriverProfileResponse(BaseModel):
    driver_id: int
    vehicle_number: str
    vehicle_type: str
    is_verified: bool
    total_rides: int
    total_earnings: float
    status: DriverStatus
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None

    class Config:
        from_attributes = True


class LocationUpdateResponse(BaseModel):
    updated_lat: float
    updated_lng: float
    message: str = "Location updated successfully"


class StatusUpdateResponse(BaseModel):
    driver_id: int
    status: DriverStatus
    vehicle_number: str
    vehicle_type: str
    is_verified: bool
    total_rides: int
    total_earnings: float


class EarningsResponse(BaseModel):
    total_earnings: float
    total_rides: int