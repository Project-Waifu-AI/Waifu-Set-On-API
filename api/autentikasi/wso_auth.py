from fastapi import APIRouter, HTTPException, Request, Cookie
from fastapi.responses import JSONResponse, RedirectResponse

from typing import Optional
import random
import requests


from database.model import UserData, UserAuth

from helper.access_token import create_access_token, check_access_token_expired, decode_access_token
from helper.cek_and_set import cek_password, cek_valid_email, set_password, cek_admin, cek_data_user, cek_valid_password

from handler.response.basic import success_response, error_response
from handler.request.auth import LoginWSO, SimpanUserWSO

from send.email import send_verify_token

from configs import config

router = APIRouter(prefix='/auth/wso', tags=['Waifu-Set-On-autentikasi'])

@router.post('/login')
async def login_wso(meta: LoginWSO):
    user = await cek_data_user(namaORemail=meta.emailORname)
    
    if user is False:
        raise HTTPException(detail=error_response(pesan='name or email is still not registered', penyebab='user is not found', action='login-wso'), status_code=404)

    if user.auth.wso is False:
        return RedirectResponse(config.redirect_uri_page_masuk, status_code=300)
        
    if not cek_password(password=meta.password, user=user):
        raise HTTPException(status_code=403, detail=error_response(pesan="the name or email or password you entered is incorrect", penyebab='The password you entered is incorrect', action='login-wso', kepada=user.email))

    token = create_access_token(user=user)     
    redirect_url = f'{config.redirect_root_wso}?token={token}'
    return JSONResponse(content={'url': redirect_url}, status_code=201)
        
@router.post('/register/{email}')
async def register(email: str):
    token_konfirmasi = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    user = await UserData.get_or_none(email=email)
    validasi_email = cek_valid_email(email=email)
    
    adminkah = cek_admin(email=email)

    if validasi_email is False:
        raise HTTPException(status_code=403, detail=error_response(pesan="The email you entered is invalid", penyebab='your email is not valid', action='register-wso'))
    
    if user:
        
        if user.banned:
            raise HTTPException(status_code=403, detail=error_response(pesan="Your account has been banned", kepada=email, action='register-wso', penyebab='your email is banned stupid'))
        
        if user.auth.wso is False:
            sendEmail01=send_verify_token(target_email=email, token=token_konfirmasi)
            if sendEmail01 is True:
                
                try:
                    user.token = token_konfirmasi
                    user.admin = adminkah
                    await user.save()
                    response = success_response(kepada=email, action='register-wso', pesan=f'confirmation token has been sent')
                    return JSONResponse(response, status_code=201)
                
                except Exception as e:
                    raise HTTPException(detail=error_response(pesan='something gone wrong', kepada=email, penyebab=str(e), action='register-wso'), status_code=500)
            
            else:
                raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=str(sendEmail01), kepada=email, action='register-wso'), status_code=500)
        
        else:
            raise HTTPException(detail=error_response(pesan='Your email has been registered on a WSO account and cannot be created again', penyebab='This email has been registered to the WSO application using WSO authentication', kepada=email, action='register-wso'), status_code=405)
    
    else:
        sendEmail02 = send_verify_token(target_email=email, token=token_konfirmasi)
        if sendEmail02 is True:
            
            try:
                await UserData.create(email=email, token=token_konfirmasi, status='register-wso', admin=adminkah)
                
                response = success_response(kepada=email, action='register-wso', pesan=f'confirmation token has been sent')
                
                return JSONResponse(response, status_code=201)
            
            except Exception as e:
                raise HTTPException(detail=error_response(pesan='something gone wrong', kepada=email, penyebab=str(e), action='register-wso'), status_code=500)
        
        else:
            raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=str(sendEmail02), kepada=email, action='register-wso'), status_code=500)
    
@router.post('/simpan-user')
async def simpan_user(meta: SimpanUserWSO):
    user = await UserData.get_or_none(email=meta.email)
    user_auth = await UserAuth.get_or_none(user=user)
    
    if user is None:
        raise HTTPException(detail=error_response(pesan='user not found', penyebab='user is not found', action='simpan-user-wso'), status_code=404)

    if meta.password != meta.konfirmasi_password:
        raise HTTPException(detail=error_response(pesan='The password and confirmation password you entered are not the same, please try again', penyebab='The password and confirmation password you entered are not the same', action='simpan-user-wso', kepada=user.email), status_code=403)
        
    if cek_valid_password(meta.password) is False:
        raise HTTPException(detail=error_response(pesan='The password must consist of 8 characters, a combination of lowercase and uppercase letters and numbers added as well', kepada=user.email, penyebab='password is not valid', action='simpan-user-wso'), status_code=403) 
    
    if user.token and user.token == meta.token:
        # Token cocok dengan pengguna
        if user_auth is None:
            
            try:
                await UserAuth.create(password=set_password(password=meta.password), wso=True, user=user)
                
                token = create_access_token(user=user)
                redirect_url = f'{config.redirect_root_wso}?token={token}&tujuan=register'
                response = JSONResponse(content={'url': redirect_url}, status_code=201)
                return response
            
            except Exception as e:
                raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=str(e), kepada=user.email, action='simpan-user-wso'), status_code=500)
        else:
            try:
                user_auth.password = set_password(password=meta.password)  # Setel kata sandi baru
                user_auth.wso = True  # Setel akunwso menjadi Aktif
                user.token = None  # Hapus token
                
                await user.save()
                await user_auth.save()

                token = create_access_token(user=user)
                redirect_url = f'{config.redirect_root_wso}?token={token}&tujuan=register'
                response = JSONResponse(content={'url': redirect_url}, status_code=201)
                return response
            
            except Exception as e:
                raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=str(e), kepada=user.email, action='simpan-user-wso'), status_code=500)
    else:
        # Token tidak cocok dengan pengguna
        if user_auth:
            # Akun pengguna google auth aktif, hapus token
            user.token = None  # Hapus token
            await user.save()
            raise HTTPException(detail=error_response(pesan='The confirmation token you entered is incorrect, please regenerate a new confirmation token in the register section', penyebab='The confirmation token you entered is incorrect', kepada=user.email, action='simpan-user-wso'), status_code=404)
        
        else:
            # gak terhubung dengan auth lain , hapus data pengguna
            await user.delete()  # Hapus data pengguna
            raise HTTPException(detail=error_response(pesan='The confirmation token you entered is incorrect, please regenerate a new confirmation token in the register section', penyebab='The confirmation token you entered is incorrect', kepada=user.email, action='simpan-user-wso'), status_code=404)

@router.get('/root')
async def submit(request: Request, token: str, tujuan: Optional[str] = None, access_token: str = Cookie(default=None)):
    if tujuan == 'register':
        target_url = config.redirect_uri_update
    else:
        target_url = config.redirect_uri_home
    response = requests.get(target_url, cookies={'access_token': access_token})

    if 'access_token' in response.cookies:
        response = RedirectResponse(target_url, status_code=300)
        response.delete_cookie(key='access_token', domain="waifu-set-on.wso", path='/')
    else:
        response = RedirectResponse(target_url, status_code=300)

    check = check_access_token_expired(access_token=token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=token)
        email = payloadJWT.get('sub')
    
    user = cek_data_user(namaORemail=email)
    
    response.set_cookie(key='access_token', value=token, domain="waifu-set-on.wso", path='/')
    response.set_cookie(key='google_auth', value=user.auth.google, domain="waifu-set-on.wso", path='/')
    response.set_cookie(key='smd_auth', value=user.auth.smd, domain="waifu-set-on.wso", path='/')
    response.set_cookie(key='wso_auth', value=user.auth.wso, domain="waifu-set-on.wso", path='/')
    return response