import random
from app.core.redis import redis_client


OTP_EXPIRE_SECONDS = 300

def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(email: str, otp:str):
    key = f"otp:{email}"
    redis_client.setex(key, OTP_EXPIRE_SECONDS, otp)


def verify_otp(email: str, otp: str):
    stored_otp = redis_client.get(f"otp:{email}")   
    if stored_otp and stored_otp == otp:
        redis_client.delete(f"otp: {email}")
        return True
    return False
