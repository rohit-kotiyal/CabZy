from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class DriverStatus(str, enum.Enum):
    offline = "offline"
    active = "active"
    busy = "busy"


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    vehicle_number = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)

    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)

    status = Column(Enum(DriverStatus), default=DriverStatus.offline)

    user = relationship("User")

    