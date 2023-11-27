from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
import os
from configs import config
from database.model import userdata, token_google
from helping.auth_helper import create_access_token, apakahNamakuAda, buatNamaUnik, cek_admin

router = APIRouter(prefix='/google-auth', tags=['google-auth-WSO'])

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# endpoint pemanggilan
@router.get("/autentikasi")
async def daftar():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['email', 'profile']  
    )
    flow.redirect_uri = config.redirect_uri_autentikasi_google
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

#endpoint callback
@router.get("/callback-autentikasi")
async def auth2callback_register(request: Request, state: str):
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['email', 'profile'],  
            state=state
        )
        flow.redirect_uri = config.redirect_uri_autentikasi_google
        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        access_token = credentials.token
        exp_token = credentials.expiry
        refresh_token = credentials.refresh_token

        userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
        user_info_response = requests.get(userinfo_endpoint, headers={'Authorization': f'Bearer {access_token}'})
        user_info = user_info_response.json()
        nama = user_info.get("name")
        email = user_info.get('email')

        user = await userdata.filter(email=email).first()
        
        global namaYangDisimpan
        if await apakahNamakuAda(nama=nama) == False:
            namaYangDisimpan = await buatNamaUnik(nama=nama)
        else:
            namaYangDisimpan = nama
        
        if user:
            
            if user.googleAuth is False:
                user.googleAuth = True
                user.AtsumaruKanjo += 100
            else:
                token = create_access_token(user=user)
                return JSONResponse (content={'access_token': str(token)})
            
            if user.nama is None:
                user.nama = namaYangDisimpan  
            
            await user.save()
            
            await token_google.create(email=email, access_token=access_token, token_exp=exp_token, refersh_token=refresh_token)

            token = create_access_token(user=user)
            return JSONResponse (content={'access_token': str(token)})
        else:
            save = userdata(nama=namaYangDisimpan, email=email, googleAuth=True, AtsumaruKanjo=100)
            await save.save()
            user = await userdata.filter(email=email).first()
            token = create_access_token(user=user)
            return JSONResponse({'access_token': token})
    
    except ConnectionError as e:
        print(f"Kesalahan koneksi: {e}")
        return JSONResponse({"error": "Request Timed Out"}, status_code=500)