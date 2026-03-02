from sqlalchemy import Column, String, Integer, Enum, DateTime
from app.core.database import Base
from datetime import datetime, timezone
import enum


class UserRole(str, enum.Enum):
    rider = "rider"
    driver = "driver"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.rider)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    