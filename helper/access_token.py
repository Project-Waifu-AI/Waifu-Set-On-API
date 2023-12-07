from typing import Optional
from datetime import datetime, timezone, timedelta
from jose import jwt
from configs import config

def create_access_token(user, permintaan: Optional[str]= None):
    if user.admin is False:
        level = 'user'
    elif user.admin is True:
        level = 'admin'
    to_encode = {
        "sub": str(user.email),
        "level": level,
        "exp": datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=8),
    }
    if permintaan is not None:
        to_encode.update({'permintaan':permintaan})
    
    encoded_token = jwt.encode(to_encode, config.secret_key, algorithm=config.algoritma)
    return encoded_token

def check_access_token_expired(access_token: str):
    try:
        payload = jwt.decode(access_token, config.secret_key, algorithms=[config.algoritma])
        expiration = payload.get("exp")
        if expiration:
            expiration_utc = datetime.utcfromtimestamp(expiration).replace(tzinfo=timezone.utc)
            return expiration_utc < datetime.now(timezone.utc)
        else:
            return False
    except jwt.ExpiredSignatureError:
        return True  # Token sudah kadaluarsa

def decode_access_token(access_token: str):
    try:
        payload = jwt.decode(access_token, config.secret_key, algorithms=[config.algoritma])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token sudah kadaluarsa
    except jwt.InvalidTokenError:
        return None  # Token tidak valid