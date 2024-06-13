from database.model import UserGoogleAuth
from typing import Optional
from datetime import datetime

def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    
async def save_google_creds(user, drive_id,token, exp, refersh:Optional[datetime]=None):
    data = await UserGoogleAuth.get_or_none()
    
    if data:
        data.access_token = token
        data.token_exp = exp
        data.refresh_token = refersh
        data.drive_id = drive_id
        await data.save()
        return True
    
    await UserGoogleAuth.create(access_token = token, user=user, token_exp = exp, refresh_token = refersh)
    return True