from app.core.database import Base
import enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum, DateTime


class RideStatus(str, enum.Enum):
    requested = "requested"
    accepted = "accepted"
    started = "started"
    completed = "completed"
    cancelled = "cancelled"


class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    drop_lat = Column(Float, nullable=False)
    drop_lng = Column(Float, nullable=False)

    fare_estimate = Column(Float, nullable=True)
    fare_actual = Column(Float, nullable=True)
    distance_meters = Column(Float, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    status = Column(Enum(RideStatus), default=RideStatus.requested)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    rider = relationship("User", foreign_keys=[rider_id])
    driver = relationship("User", foreign_keys=[driver_id])
