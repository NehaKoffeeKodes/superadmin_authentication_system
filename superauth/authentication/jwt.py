import datetime,jwt
from django.conf import settings

def create_jwt(user, expire_minutes: int = 15) -> str:
    """
    Creates a JWT token for the given user.
    Default expiry: 15 minutes (use longer for final access token).
    Used after successful login or OTP verification.
    """
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes),
        "iat": datetime.datetime.utcnow(),  
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


