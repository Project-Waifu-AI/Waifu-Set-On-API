from database.model import userdata, access_token_data
from datetime import datetime, timedelta
from database.model import logaudio
from ast import pattern
import bcrypt
import secrets
import pytz
import io
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

async def create_access_token(user_id: str):
    token = secrets.token_hex(16)
    waktu_basi = datetime.now(pytz.utc) + timedelta(hours=1)
    save = access_token_data(access_token=token, waktu_basi=waktu_basi, user_id=user_id)
    await save.save()

async def check_access_token_expired(access_token: str):
    current_time = datetime.now(pytz.utc)
    data = await access_token_data.filter(access_token=access_token).first()
    
    if data:
        if data.waktu_basi <= current_time:
            await data.delete()
            return True
        else:
            return data.user_id
    else:
        return False

async def check_premium_becomewaifu(user_id:str):
    user = await userdata.filter(user_id=user_id).first()
    if not user.premium:
        user_audio_count = await logaudio.filter(user_id=user_id).count()
        if user_audio_count >= 10:
            return ("logaudio data anda telah mencapai limit. Upgrade ke plan premium atau hapus logaudio.")
    else:
        current_time = datetime.now()
        if user.waktu_basi_premium and user.waktu_basi_premium <= current_time:
            user.premium = False
            await user.save()
            return ("Masa premium telah habis. Kembali ke versi gratis.")

async def check_premium_AI_U(user):
    if user.premium is False:
        return False
    elif user.premium is True:
        current_time = datetime.now()
        if user.waktu_basi_premium and user.waktu_basi_premium <= current_time:
            user.premium = False
            await user.save()
            return ("masa premium telah habis")
        else:
            return True

def validation_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False