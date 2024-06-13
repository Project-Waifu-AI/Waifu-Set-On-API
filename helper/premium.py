from jose import jwt
from datetime import timedelta, datetime, timezone

from database.model import UserPremium

from configs import config

from helper.access_token import check_access_token_expired, decode_access_token

async def check_premium(user):
    user_premium = await UserPremium.get_or_none(user=user)
    
    if user_premium is None:
        if user.admin is False:
            return{
                'status': False,
                'penyebab': 'user has not registered as a premium user'
            }
        
    if check_access_token_expired(access_token=user_premium.token) is True:
        user_premium.token = None
        await user_premium.save()
        return{
            'status': False,
            'penyebab': 'akses premium user telah berakhir'
        }
    
    cek = decode_access_token(access_token=user_premium.token)
    planing = cek.get('plan')
    return {
        'status': True,
        'keterangan': planing
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
        await user.save()
        return {
            'status': True,
            'keterangan': f'{user.email} selamat telah menjadi premium plan {plan}'
            }
    except Exception as e:
        print (str(e))
        return {
                'status': False,
                'penyebab': str(e)
                }