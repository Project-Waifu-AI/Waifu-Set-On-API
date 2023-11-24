from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
import os
from configs import config
from database.model import userdata
from helping.auth_helper import create_access_token, credentials_to_dict, apakahNamakuAda, buatNamaUnik, cek_admin

router = APIRouter(prefix='/google-auth', tags=['google-auth-WSO'])

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# endpoint pemanggilan
@router.get("/register")
async def daftar():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['email', 'profile']  
    )
    flow.redirect_uri = config.redirect_uri_register_google
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

@router.get("/login")
async def daftar():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['email', 'profile']  
    )
    flow.redirect_uri = config.redirect_uri_login_google
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

#endpoint callback
@router.get("/auth2callbackRegister")
async def auth2callback_register(request: Request, state: str):
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['email', 'profile'],  
            state=state
        )
        flow.redirect_uri = config.redirect_uri_register_google
        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        creds = credentials_to_dict(credentials)
        access_token = credentials.token

        userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
        user_info_response = requests.get(userinfo_endpoint, headers={'Authorization': f'Bearer {access_token}'})
        user_info = user_info_response.json()
        email = user_info.get("email")
        nama = user_info.get("name")

        user = await userdata.filter(email=email).first()

        if user:

            if await apakahNamakuAda(nama=nama) == False:
                namaYangDisimpan = await buatNamaUnik(nama=nama)
            else:
                namaYangDisimpan = nama

            if user.googleAuth is False:
                
                if user.akunwso is True and user.email != email:
                    raise HTTPException (detail='gmail yang anda daftarkan dengan akun wso berbeda dengan gmail yang anda coba hubungkan pada google auth')
                adminkah = cek_admin(email=email)
                if adminkah is True:
                    user.googleAuth = True
                    user.email = email
                    user.AtsumaruKanjo += 99999999
                    user.admin = True
                else:
                    user.googleAuth = True
                    user.email = email
                    user.AtsumaruKanjo += 100
                if user.nama is None:
                    user.nama = namaYangDisimpan
                    
                await user.save()
                token = create_access_token(user=user)
                return JSONResponse({'access_token': token}, status_code=201)
            
            else:
                raise HTTPException (detail='email anda sudah terhubung dengan google autentikasi', status_code=403)
        
        else:
            save = userdata(nama=namaYangDisimpan, email=email, googleAuth=True, AtsumaruKanjo=100)
            await save.save()
            user = await userdata.filter(email=email).first()
            token = create_access_token(user=user)
            return JSONResponse({'access_token': token}, status_code=201) 
    
    except ConnectionError as e:
        print(f"Kesalahan koneksi: {e}")
        return JSONResponse({"error": "Request Timed Out"}, status_code=500)

    
@router.get("/auth2callbackLogin")
async def auth2callback(request: Request, state: str):
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['email', 'profile'],  
            state=state
        )
        flow.redirect_uri = config.redirect_uri_login_google
        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        creds = credentials_to_dict(credentials)
        access_token = credentials.token

        userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
        user_info_response = requests.get(userinfo_endpoint, headers={'Authorization': f'Bearer {access_token}'})
        user_info = user_info_response.json()
        email = user_info.get("email")

        user = await userdata.filter(email=email).first()
        if user:
            
            if user.googleAuth is False:
                raise HTTPException(detail='email anda masih belum terhubung dengan google autentikasi', status_code=405)
            else:
                user = await userdata.filter(email=email).first()
                token = create_access_token(user=user)
                return JSONResponse({'access_token': token}, status_code=200)
        else:
            raise HTTPException (detail='gmail ini masih belum terdafatar dengan autentikasi apapun di WSO', status_code=405)
    except ConnectionError as e:
        print(f"Kesalahan koneksi: {e}")
        return JSONResponse({"error": "Request Timed Out"}, status_code=500)