import json
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserRegister, UserLogin, TokenResponse, VerifyOtp
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.otp import generate_otp, save_otp, verify_otp
from app.core.config import MAIL_USERNAME, MAIL_FROM, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME
from app.core.redis import redis_client
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Add email configuration
conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = MAIL_PORT,
    MAIL_SERVER = MAIL_SERVER,
    MAIL_FROM_NAME = MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


fm = FastMail(conf)


# Send OTP
@router.post("/register")
async def send_otp(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email Already Registered")
    
    otp = generate_otp()
    save_otp(user_data.email, otp)

    # Save user data temporarily
    redis_client.setex(
        f"register:{user_data.email}",
        300,
        json.dumps(user_data.model_dump())
    ) 


    # Send Email
    message = MessageSchema(
        subject="Your CabZy OTP Code",
        recipients=[user_data.email],
        body=f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #2c3e50;">Welcome to CabZy!</h2>
                <p>Your OTP code is:</p>
                <h1 style="color: #3498db; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
                <p>This code will expire in <strong>5 minutes</strong>.</p>
                <p style="color: #7f8c8d; font-size: 12px;">If you didn't request this code, please ignore this email.</p>
            </body>
        </html>
        """,
        subtype="html"
    )


    try:
        await fm.send_message(message)
        return {"message": "OTP was sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP email: {str(e)}")

# Register User
@router.post("/verify-otp", response_model=TokenResponse)
async def confirm_registration(data: VerifyOtp, db: Session = Depends(get_db)):
    
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="Invalid or Expired OTP")
    
    # Fetch temp user data
    temp_data = redis_client.get(f"register:{data.email}")
    if not temp_data:
        raise HTTPException(status_code=400, detail="Registration Failed")
    
    user_data = json.loads(temp_data)

    try:
        # Create user object
        new_user = User(
            name=user_data["name"],
            email=user_data["email"],
            phone=user_data["phone"],
            password=hash_password(user_data["password"]),
            role=UserRole(user_data["role"])
        )

        db.add(new_user)
        db.flush() 
        
        # Generate token (if this fails, nothing is committed)
        token = create_access_token({"sub": str(new_user.id)})
        
        # Only commit if everything succeeded
        db.commit()
        db.refresh(new_user)
        
        # Clean up Redis
        redis_client.delete(f"register:{data.email}")
        redis_client.delete(f"otp:{data.email}")
        
        return {"access_token": token}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )



@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin, 
    db: Session = Depends(get_db),
    ):
    
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/form-login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db),
    ):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Authorize
@router.get("/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role.value
    }