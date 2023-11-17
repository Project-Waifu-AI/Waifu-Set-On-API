from database.model import userdata, premium
from configs import config
from datetime import datetime, timedelta, timezone
from database.model import logaudio
from ast import pattern
from jose import jwt
from typing import Optional
import random
import bcrypt
import secrets
import pytz
import re
def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

def check_password(password: str, user):
    bytes = password.encode('utf-8')
    password_data = user.password
    result = bcrypt.checkpw(bytes, password_data)
    return result

def set_password(password: str):
    salt = bcrypt.gensalt()
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    return hash

def create_access_token(user, permintaan: str | None):
    if user.admin is False:
        level = 'user'
    elif user.admin is True:
        level = 'admin'
    to_encode = {
        "sub": str(user.user_id),
        "level": level,
        "exp": datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=8),
    }
    if permintaan is not None:
        to_encode.update({'permintaan':permintaan})
        encoded_token = jwt.encode(to_encode, config.secret_key, algorithm=config.algoritma)
        return encoded_token
    else:
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
        
async def check_premium_becomewaifu(user_id:str):
    user = await premium.filter(user_id=user_id).first()
    if user is None:
        user_audio_count = await logaudio.filter(user_id=user_id).count()
        if user_audio_count >= 10:
            return ("logaudio data anda telah mencapai limit. Upgrade ke plan premium atau hapus logaudio.")
    else:
        current_time = datetime.now()
        if user.waktu_basi and user.waktu_basi <= current_time:
            user.premium = False
            await user.save()
            return ("Masa premium telah habis. Kembali ke versi gratis.")

async def check_premium_AI_U(user):
    data = await premium.filter(user_id=user.user_id).first()
    if data.premium is False:
        return False
    elif data.premium is True:
        current_time = datetime.now()
        if data.waktu_basi and data.waktu_basi <= current_time:
            data.premium = False
            await data.save()
            return False
        else:
            return True

def validation_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False
    
async def apakahNamakuAda(nama:str):
    user = await userdata.filter(nama=nama).first()
    if user:
        return False
    else:
        return True
    
async def buatNamaUnik(nama:str):
    while True:
        random_suffix = random.randint(1, 9999)
        new_name = f"{nama}#{random_suffix}"
        user = await userdata.filter(nama=new_name).first()
        if user is None:
            return new_name
        
async def userIni(namaORemail: str):
    nama = await userdata.filter(nama=namaORemail).first()
    if nama:
        return nama
    else:
        email = await userdata.filter(email=namaORemail).first()
        if email:
            return email
        else:
            return False

def valid_password(password: str):
    if len(password) < 8:
        return False
    
    if not (re.search("[a-z]", password) and
            re.search("[A-Z]", password) and
            re.search("[0-9]", password)):
            return False
    
    return True