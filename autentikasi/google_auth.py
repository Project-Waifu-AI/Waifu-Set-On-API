from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import google_auth_oauthlib.flow
import requests
import os
from configs import config
from database.model import userdata
from helping.auth_helper import create_access_token, apakahNamakuAda, buatNamaUnik, cek_admin, save_google_creds
from helping.drive_google_helper import create_folder_gdrive

router = APIRouter(prefix='/google-auth', tags=['google-auth-WSO'])

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# endpoint pemanggilan
@router.get("/autentikasi")
async def daftar():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['email', 'profile', 'https://www.googleapis.com/auth/drive.file']  
    )
    flow.redirect_uri = config.redirect_uri_autentikasi_google
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
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
                
                if cek_admin is True:
                    user.admin = True
                    user.AtsumaruKanjo += 999999999
                    user.NegaiGoto += 999999999
                else:
                    user.AtsumaruKanjo += 100

                if user.nama is None:
                    user.nama = namaYangDisimpan
                
                if user.driveID is None:
                    drive = create_folder_gdrive
                    user.driveID = str(drive)
                await user.save()

            await save_google_creds(email=email, token=access_token, exp=exp_token, refersh=refresh_token)
            
            token = create_access_token(user=user)
            return JSONResponse(content={
                'access_token': token,
                'google_auth': str(user.googleAuth),
                'akunWSO': str(user.akunwso)
            }, status_code=200)
        
        else:
            
            drive = create_folder_gdrive(access_token=access_token, email=email)
            
            if cek_admin(email=email) is False:
                save = userdata(nama=namaYangDisimpan, email=email, googleAuth=True, AtsumaruKanjo=100, driveID=str(drive))
            else:
                save = userdata(nama=namaYangDisimpan, email=email, googleAuth=True, AtsumaruKanjo=999999999, driveID=str(drive), admin=True)
            
            await save_google_creds(email=email, token=access_token, exp=exp_token, refersh=refresh_token)
            
            await save.save()
            
            user = await userdata.filter(email=email).first()
            
            token = create_access_token(user=user)
            
            return JSONResponse(content={
                'access_token': token,
                'google_auth': str(save.googleAuth),
                'akunWSO': str(save.akunwso)
            })
    
    except ConnectionError as e:
        raise HTTPException(detail=str(e), status_code=500)