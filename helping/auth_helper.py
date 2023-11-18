from database.model import userdata
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

def create_access_token(user, permintaan: Optional[str]= None):
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
        
async def check_premium(user_id):
    try:
        user = await userdata.filter(user_id=user_id).first()
        if user.premium_token is None:
            return{
                'status': False,
                'keterangan': 'silahkan pilih plan premium'
            }
        else:
            if check_access_token_expired(access_token=user.premium_token) is True:
                user.premium_token = None
                user.save()
                return{
                    'status': False,
                    'keterangan': 'akses premium user telah berakhir'
                }
            else:
                cek = decode_access_token(access_token=user.premium)
                planing = cek.get('plan')
                return {
                    'status': True,
                    'keterangan': planing
                }
    except Exception as e:
        return{
            'status':False,
            'keterangan': str(e)
        }

async def create_token_premium(user_id: str, plan: str):
    try:
        to_encode = {
            "sub": user_id,
            "plan": plan,
            "exp": datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=720),
        }
        encoded_token = jwt.encode(to_encode, config.secret_key, algorithm=config.algoritma)
        user = await userdata.filter(user_id=user_id).first()
        user.premium = str(encoded_token)
        user.save
        return {
            'status': True,
            'keterangan': f'{user.email} selamat telah menjadi premium plan {plan}'
            }
    except Exception as e:
        print (str(e))
        return {
                'status': False,
                'keterangan': str(e)
                }
    
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