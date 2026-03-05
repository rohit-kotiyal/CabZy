from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.ride import Ride, RideStatus
from app.schemas.ride import RideRequest, RideResponse
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.utils.calculations import validate_coordinates, calculate_distance, estimate_duration, calculate_fare
from typing import List


router = APIRouter(prefix="/rides", tags=["Rides"])


@router.post("/request", response_model=RideResponse)
async def request_ride(
    ride_data: RideRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    # Check Role
    if current_user.role != UserRole.rider:
        raise HTTPException(status_code=403, detail="Only riders can request rides")
    
    # Validate Coordinates
    validate_coordinates(ride_data.pickup_lat, ride_data.pickup_lng)
    validate_coordinates(ride_data.drop_lat, ride_data.drop_lng)

    # Check for active rides
    active_ride = db.query(Ride).filter(
        Ride.rider_id == current_user.id,
        Ride.status.in_([RideStatus.accepted, RideStatus.requested, RideStatus.started])
    ).first()

    if active_ride:
        raise HTTPException(status_code=400, detail="You already have an active ride")

    # Calculate distance, duration & fare
    distance = calculate_distance(ride_data.pickup_lat, ride_data.pickup_lng, ride_data.drop_lat, ride_data.drop_lng)
    duration = estimate_duration(distance)
    fare = calculate_fare(distance, duration)


    ride = Ride(
        rider_id = current_user.id,
        pickup_lat = ride_data.pickup_lat,
        pickup_lng = ride_data.pickup_lng,
        drop_lat = ride_data.drop_lat,
        drop_lng = ride_data.drop_lng,
        distance_meters = distance,
        duration_seconds = duration,
        fare_estimate = fare,
        status = RideStatus.requested
    )

    try:
        db.add(ride)
        db.commit()
        db.refresh(ride)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ride


@router.post("/{ride_id}/accept", response_model=RideResponse)
async def accept_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    """Driver accepts a ride request"""
    # Verify user is a driver
    if current_user.role != UserRole.driver:
        raise HTTPException(status_code=403, detail="Only drivers can accept rides")
    
    # Check if driver has active ride
    active_ride = db.query(Ride).filter(
        Ride.driver_id == current_user.id,
        Ride.status.in_([RideStatus.accepted, RideStatus.started])
    ).first()

    if active_ride:
        raise HTTPException(status_code=400, detail="You already have an active ride")
    

    # Get the requested ride
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    if ride.status != RideStatus.requested:
        raise HTTPException(status_code=400, detail="Ride is not available")
    

    # Accept the ride
    ride.driver_id = current_user.id
    ride.status = RideStatus.accepted


    try:
        db.commit()
        db.refresh(ride)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to accept ride")
    
    return ride



@router.post("/{ride_id}/start", response_model=RideResponse)
def start_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Driver start the ride"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    if ride.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if ride.status != RideStatus.accepted:
        raise HTTPException(status_code=400, detail="Ride must be accepted first")
    
    ride.status = RideStatus.started

    try:
        db.commit()
        db.refresh(ride)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ride



@router.post("/{ride_id}/complete", response_model=RideResponse)
async def complete_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    """Driver completes the ride"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    if ride.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if ride.status != RideStatus.started:
        raise HTTPException(status_code=400, detail="Ride must be started first")
    
    
    ride.status = RideStatus.completed

    try:
        db.commit()
        db.refresh(ride)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ride


@router.post("/{ride_id}/cancel", response_model=RideResponse)
async def cancel_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    """Cancel a ride"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    # Check authorization (either rider or assigned driver)
    if ride.rider_id != current_user.id and ride.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    # Can't cancel completed ride
    if ride.status == RideStatus.completed:
        raise HTTPException(status_code=400, detail="Cannot cancel completed ride")
    
    ride.status = RideStatus.cancelled

    try:
        db.commit()
        db.refresh(ride)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ride


@router.get("/available", response_model=List[RideResponse])
async def get_available_rides(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available rides for the drivers to accept"""
    if current_user.role != UserRole.driver:
        raise HTTPException(status_code=403, detail="Only drivers can see available rides")
    
    rides = db.query(Ride).filter(
        Ride.status == RideStatus.requested
    ).order_by(Ride.created_at.desc()).offset(skip).limit(limit).all()

    return rides



@router.get("/current/active", response_model=RideResponse)
async def get_current_ride(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get's user current active ride"""
    active_ride = db.query(Ride).filter(
        or_(
            Ride.rider_id == current_user.id,
            Ride.driver_id == current_user.id
        ),
        Ride.status.in_([RideStatus.requested, RideStatus.accepted, RideStatus.started])
    ).first()

    if not active_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    return active_ride



@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific ride detail"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    # Check Authorization
    if ride.rider_id != current_user.id and ride.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    return ride




@router.get("/history/all", response_model=List[RideResponse])
async def get_ride_history(
    status: RideStatus = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get ride history with optional status filter.
    Example: /rides/history/all?status=completed
    """
    query = db.query(Ride).filter(
    or_(
        Ride.rider_id == current_user.id,
        Ride.driver_id == current_user.id
        )
    )
    
    if status:
        query = query.filter(Ride.status == status)
    
    rides = query.order_by(Ride.created_at.desc()).offset(skip).limit(limit).all()
    
    return rides