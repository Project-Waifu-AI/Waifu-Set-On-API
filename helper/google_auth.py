from database.model import token_google
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
    
async def save_google_creds(email, token, exp, refersh:Optional[datetime]=None):
    data = await token_google.filter(email=email).first()
    if refersh is None:
        if data:
            data.access_token = token
            data.token_exp = exp
            await data.save()
        else:
            save = token_google(email=email, access_token=token, token_exp=exp)
            await save.save()
    else: 
        if data:
            data.access_token = token
            data.token_exp = exp
            data.refersh_token = refersh
            await data.save()
        else:
            save = token_google(email=email, access_token=token, token_exp=exp, refersh_token=refersh)
            await save.save()