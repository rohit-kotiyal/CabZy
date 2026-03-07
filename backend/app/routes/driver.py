from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.driver import Driver, DriverStatus
from app.models.ride import Ride, RideStatus
from app.core.security import get_current_user
from app.utils.calculations import validate_coordinates
from app.schemas.driver import (
    DriverProfileResponse,
    LocationUpdateRequest,
    LocationUpdateResponse,
    StatusUpdateRequest,
    StatusUpdateResponse,
    EarningsResponse,
    DriverRegistrationRequest
)


router = APIRouter(prefix="/driver", tags=["Drivers"])


# Function to verify driver role
def verify_driver_role(current_user: User):
    if current_user.role != UserRole.driver:
        raise HTTPException(status_code=403, detail="Access forbidden: Driver role required")


@router.post("/register", response_model=DriverProfileResponse)
def register_driver(
    driver_data: DriverRegistrationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_driver_role(current_user)
    
    # Check if driver already exists
    existing_driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if existing_driver:
        raise HTTPException(status_code=400, detail="Driver profile already exists")
    
    # Create new driver
    new_driver = Driver(
        user_id=current_user.id,
        vehicle_number=driver_data.vehicle_number,
        vehicle_type=driver_data.vehicle_type,
        is_verified=False,
        status=DriverStatus.offline,
        total_earnings=0.0,
        total_rides=0
    )
    
    try:
        db.add(new_driver)
        db.commit()
        db.refresh(new_driver)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    return {
        "driver_id": new_driver.id,
        "vehicle_number": new_driver.vehicle_number,
        "vehicle_type": new_driver.vehicle_type,
        "is_verified": new_driver.is_verified,
        "total_rides": new_driver.total_rides,
        "total_earnings": new_driver.total_earnings,
        "status": new_driver.status,
        "current_lat": new_driver.current_lat,
        "current_lng": new_driver.current_lng
    }


@router.get("/profile", response_model=DriverProfileResponse)
def get_driver_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_driver_role(current_user)
    
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    
    return {
        "driver_id": driver.id,
        "vehicle_number": driver.vehicle_number,
        "vehicle_type": driver.vehicle_type,
        "is_verified": driver.is_verified,
        "total_rides": driver.total_rides,
        "total_earnings": driver.total_earnings,
        "status": driver.status,
        "current_lat": driver.current_lat,
        "current_lng": driver.current_lng
    }


@router.put("/location", response_model=LocationUpdateResponse)
def update_driver_location(
    location_data: LocationUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_driver_role(current_user)
    
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    
    # Validate coordinates
    validate_coordinates(location_data.lat, location_data.lng)
    
    # Only allow location updates if driver is active or busy
    if driver.status == DriverStatus.offline:
        raise HTTPException(status_code=400, detail="Cannot update location while offline")
    
    driver.current_lat = location_data.lat
    driver.current_lng = location_data.lng

    try:
        db.commit()
        db.refresh(driver)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    return {
        "updated_lat": driver.current_lat,
        "updated_lng": driver.current_lng,
        "message": "Location updated successfully"
    }


@router.put("/status", response_model=StatusUpdateResponse)
def update_driver_status(
    status_data: StatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_driver_role(current_user)
    
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    
    # Validation: driver must be verified to go active
    if status_data.status == DriverStatus.active and not driver.is_verified:
        raise HTTPException(status_code=400, detail="Driver must be verified to go active")
    
    # Validation: check for active rides when changing status
    if status_data.status == DriverStatus.offline:
        active_ride = db.query(Ride).filter(
            Ride.driver_id == driver.id,
            Ride.status.in_([RideStatus.accepted, RideStatus.arrived, RideStatus.in_progress])
        ).first()
        
        if active_ride:
            raise HTTPException(status_code=400, detail="Cannot go offline with active rides")
        
        # Clear location when going offline
        driver.current_lat = None
        driver.current_lng = None
    
    driver.status = status_data.status

    try:
        db.commit()
        db.refresh(driver)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    return {
        "driver_id": driver.id,
        "status": driver.status,
        "vehicle_number": driver.vehicle_number,
        "vehicle_type": driver.vehicle_type,
        "is_verified": driver.is_verified,
        "total_rides": driver.total_rides,
        "total_earnings": driver.total_earnings
    }


@router.get("/earnings", response_model=EarningsResponse)
def get_driver_earnings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_driver_role(current_user)
    
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    
    return {
        "total_earnings": driver.total_earnings,
        "total_rides": driver.total_rides
    }