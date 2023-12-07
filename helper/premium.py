from jose import jwt
from datetime import timedelta, datetime, timezone
from configs import config
from helper.access_token import check_access_token_expired, decode_access_token
from database.model import userdata

async def check_premium(email):
    try:
        user = await userdata.filter(email=email).first()
        if user.premium_token is None:
            if user.admin is True:
                return{
                    'status': True,
                    'keterangan': 'admin'
                }
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
            elif user.admin is True:
                return{
                    'status': True,
                    'keterangan': 'admin'
                }
            else:
                cek = decode_access_token(access_token=user.premium_token)
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

async def create_token_premium(email: str, plan: str):
    try:
        to_encode = {
            "sub": email,
            "plan": plan,
            "exp": datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=720),
        }
        encoded_token = jwt.encode(to_encode, config.secret_key, algorithm=config.algoritma)
        user = await userdata.filter(email=email).first()
        user.premium_token = str(encoded_token)
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