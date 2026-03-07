from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_db
from app.models.admin import Admin
from app.models.driver import Driver
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    get_current_admin
)
from app.schemas.admin import (
    AdminTokenResponse,
    AdminResponse,
    AdminCreateRequest,
    PendingDriverResponse,
    VerifyDriverResponse,
    DeleteDriverResponse
)
from typing import List


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/form-login", response_model=AdminTokenResponse)
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Admin login with form data - separate from user login
    """
    admin = db.query(Admin).filter(Admin.email == form_data.username).first()
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token with type='admin'
    token = create_access_token({
        "sub": str(admin.id),
        "type": "admin"
    })
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Get current logged-in admin information
    """
    return current_admin



@router.post("/create-admin", response_model=AdminResponse, status_code=201)
async def create_new_admin(
    admin_data: AdminCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new admin - No authentication required (for backend use only)
    """
    try:
        # Check if email already exists
        existing_admin = db.query(Admin).filter(Admin.email == admin_data.email).first()
        if existing_admin:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = hash_password(admin_data.password)
        
        # Create new admin
        new_admin = Admin(
            name=admin_data.name,
            email=admin_data.email,
            password=hashed_password
        )
        
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        
        return new_admin
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(e)}"
        )


@router.get("/list", response_model=List[AdminResponse])
async def get_all_admins(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Get list of all admins
    """
    admins = db.query(Admin).all()
    return admins


@router.delete("/{admin_id}")
async def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Delete an admin (cannot delete yourself)
    """
    if admin_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    try:
        db.delete(admin)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    return {"message": "Admin deleted successfully", "admin_id": admin_id}



@router.get("/drivers/pending", response_model=List[PendingDriverResponse])
async def get_pending_drivers(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Get all drivers pending verification
    """
    drivers = db.query(Driver).filter(Driver.is_verified == False).all()

    return [
        {
            "driver_id": driver.id,
            "user_id": driver.user_id,
            "vehicle_number": driver.vehicle_number,
            "vehicle_type": driver.vehicle_type,
            "is_verified": driver.is_verified,
            "status": driver.status,
            "total_rides": driver.total_rides,
            "total_earnings": driver.total_earnings
        }
        for driver in drivers
    ]


@router.put("/drivers/{driver_id}/verify", response_model=VerifyDriverResponse)
async def verify_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Verify a driver's account
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    if driver.is_verified:
        raise HTTPException(status_code=400, detail="Driver is already verified")
    
    driver.is_verified = True

    try:
        db.commit()
        db.refresh(driver)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
    return {
        "message": "Driver verified successfully",
        "driver_id": driver.id,
        "is_verified": driver.is_verified
    }


@router.delete("/drivers/{driver_id}", response_model=DeleteDriverResponse)
async def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Delete/reject a driver account
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    try:
        db.delete(driver)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

    return {
        "message": "Driver deleted successfully",
        "driver_id": driver_id
    }