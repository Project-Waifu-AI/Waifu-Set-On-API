from fastapi import APIRouter, Request, HTTPException, Cookie
from fastapi.responses import RedirectResponse
import google_auth_oauthlib.flow
import requests
import os
from configs import config
from database.model import userdata
from helper.access_token import create_access_token, decode_access_token, check_access_token_expired
from helper.cek_and_set import cek_namaku_ada, set_name_unik, cek_admin
from helper.google_auth import save_google_creds
from helper.drive_google import create_folder_gdrive

router = APIRouter(prefix='/auth/google', tags=['google-auth-WSO'])

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
@router.get("/callback-autentikasi", response_class=RedirectResponse)
async def auth2callback_register(request: Request, state: str) -> RedirectResponse:
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
        if await cek_namaku_ada(nama=nama) == False:
            namaYangDisimpan = await set_name_unik(nama=nama)
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
                    drive = create_folder_gdrive(access_token=access_token)
                    if drive['status'] is False:
                        raise HTTPException(detail=drive['keterangan'], status_code=500)
                    else:
                        drive_id = drive['keterangan']
                    user.driveID = drive_id
                
                await user.save()

            await save_google_creds(email=email, token=access_token, exp=exp_token, refersh=refresh_token)
            
            token = create_access_token(user=user)
            redirect_url = f'{config.redirect_root_google}?token={token}'
            response = RedirectResponse(redirect_url)
            response.set_cookie(key='token', value=token, httponly=True)
            return response
        
        else:
            
            drive = create_folder_gdrive(access_token=access_token)
            
            if drive['status'] is False:
                raise HTTPException(detail=drive['keterangan'], status_code=500)
            else:
                drive_id = drive['keterangan']
            
            if cek_admin(email=email) is False:
                save = userdata(nama=namaYangDisimpan, email=email, googleAuth=True, AtsumaruKanjo=100, driveID=drive_id)
            else:
                save = userdata(nama=namaYangDisimpan, email=email, googleAuth=True, AtsumaruKanjo=999999999, driveID=drive_id, admin=True)
            
            await save_google_creds(email=email, token=access_token, exp=exp_token, refersh=refresh_token)
            
            await save.save()
            
            user = await userdata.filter(email=email).first()
            
            token = create_access_token(user=user)
            
            redirect_url = f'{config.redirect_root_google}?token={token}'
            response = RedirectResponse(redirect_url)
            response.set_cookie(key='token', value=token, httponly=True)
            return response

    
    except ConnectionError as e:
        raise HTTPException(detail=str(e), status_code=500)
    
@router.get('/root')
async def submit(request: Request, token: str, access_token: str = Cookie(default=None)):
    target_url = config.redirect_uri_home
    response = requests.get(target_url, cookies={'access_token': access_token})

    if 'access_token' in response.cookies:
        response = RedirectResponse(target_url, status_code=302)
        response.delete_cookie(key='access_token', domain="waifu-set-on.wso", path='/')
    else:
        response = RedirectResponse(target_url, status_code=302)

    check = check_access_token_expired(access_token=token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=token)
        email = payloadJWT.get('sub')
    
    user = await userdata.filter(email=email).first()
    
    response.set_cookie(key='access_token', value=token, domain="waifu-set-on.wso", path='/')
    response.set_cookie(key='google_auth', value=user.googleAuth, domain="waifu-set-on.wso", path='/')
    response.set_cookie(key='smd_auth', value=user.smdAuth, domain="waifu-set-on.wso", path='/')
    response.set_cookie(key='wso_auth', value=user.akunwso, domain="waifu-set-on.wso", path='/')
    return response
