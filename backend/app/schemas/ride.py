from pydantic import BaseModel
from app.models.ride import RideStatus


class RideRequest(BaseModel):
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float



class RideResponse(BaseModel):
    id: int
    status: RideStatus

    class Config:
        from_attributes = True