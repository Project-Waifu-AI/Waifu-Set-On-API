from fastapi import APIRouter, HTTPException, Request, Cookie
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Optional
import random
import requests
from body_request.auth_body_request import LoginWSO, SimpanUserWSO
from database.model import userdata
from helper.access_token import create_access_token, check_access_token_expired, decode_access_token
from helper.cek_and_set import cek_password, cek_valid_email, set_password, cek_admin, cek_data_user, cek_valid_password
from helper.response import pesan_response
from webhook.send_email import send_verify_token
from configs import config

router = APIRouter(prefix='/auth/wso', tags=['Waifu-Set-On-autentikasi'])

@router.post('/login')
async def login_wso(meta: LoginWSO, access_token: str = Cookie(default=None)):
    user = await cek_data_user(namaORemail=meta.emailORname)
    
    if user is False:
        raise HTTPException(detail='nama, email anda masih belum terdaftar', status_code=403)

    if user.akunwso is False:
        return RedirectResponse(config.redirect_uri_page_masuk, status_code=404)
    
    else:
        if not cek_password(password=meta.password, user=user):
            raise HTTPException(status_code=401, detail="nama, email atau password yang anda masukan salah")
        else:
            try:
                token = create_access_token(user=user)
            
                redirect_url = f'{config.redirect_root_wso}?token={token}'
                response = JSONResponse(content={'url': redirect_url}, status_code=200)
                return response
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=500)
    
@router.post('/register/{email}')
async def register(email: str):
    token_konfirmasi = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    user = await userdata.filter(email=email).first()
    validasi_email = cek_valid_email(email=email)
    
    if validasi_email is False:
        raise HTTPException(status_code=400, detail="email yang anda masukan tidak valid")
    
    if user:
        if user.ban:
            raise HTTPException(status_code=403, detail="akun anda telah di ban")
        else:
            if user.akunwso is False:
                sendEmail01=send_verify_token(target_email=email, token=token_konfirmasi)
                if sendEmail01 is True:
                    try:
                        user.token_konfirmasi = token_konfirmasi
                        await user.save()
                        response = pesan_response(email=email, pesan=f'token konfirmasi telah dikirimakan')
                        return JSONResponse(response, status_code=200)
                    except Exception as e:
                        raise HTTPException(detail=str(e), status_code=500)
                else:
                    raise HTTPException(detail=str(sendEmail01), status_code=500)
            else:
                raise HTTPException(detail='email anda telah terdaftar pada akun wso tidak dapat membuat lagi', status_code=403)
    else:
        sendEmail02 = send_verify_token(target_email=email, token=token_konfirmasi)
        if sendEmail02 is True:
            try:
                save = userdata(email=email, token_konfirmasi=token_konfirmasi)
                await save.save()
                response = pesan_response(email=email, pesan=f'token konfirmasi telah dikirimakan')
                return JSONResponse(response, status_code=200)
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=500)
        else:
            raise HTTPException(detail=str(e), status_code=500)
    
@router.post('/simpan-user')
async def simpan_user(meta: SimpanUserWSO, access_token: str = Cookie(default=None)):
    user = await userdata.filter(email=meta.email).first()
    adminkah = cek_admin(email=meta.email)

    if meta.password == meta.konfirmasi_password:
        if cek_valid_password(meta.password) is False:
            raise HTTPException(detail='password anda kurang mantap man, minimal 8 karakter, kombinasi Lower dan Upper case huruf dan ditambahkan angka juga', status_code=400) 
        
        if user:
            if user.token_konfirmasi and user.token_konfirmasi == meta.token:
                # Token cocok dengan pengguna
                if adminkah is True:
                    try:
                        user.password = set_password(password=meta.password)  # Setel kata sandi baru
                        user.akunwso = True  # Setel akunwso menjadi Aktif
                        user.token_konfirmasi = None  # Hapus token
                        user.AtsumaruKanjo += 99999999
                        user.NegaiGoto += 999999999
                        user.admin = True
                        await user.save()
                        token = create_access_token(user=user)
                        redirect_url = f'{config.redirect_root_wso}?token={token}&tujuan=register'
                        response = JSONResponse(content={'url': redirect_url}, status_code=201)
                        return response
                    except Exception as e:
                        raise HTTPException(detail=str(e), status_code=500)
                else:
                    try:
                        user.password = set_password(password=meta.password)  # Setel kata sandi baru
                        user.akunwso = True  # Setel akunwso menjadi Aktif
                        user.token_konfirmasi = None  # Hapus token
                        user.AtsumaruKanjo += 100
                        await user.save()
                        token = create_access_token(user=user)

                        redirect_url = f'{config.redirect_root_wso}?token={token}&tujuan=register'
                        response = JSONResponse(content={'url': redirect_url}, status_code=200)
                        return response
                    except Exception as e:
                        raise HTTPException(detail=str(e), status_code=500)
            else:
                # Token tidak cocok dengan pengguna
                if user.googleAuth is True:
                    # Akun pengguna google auth aktif, hapus token
                    user.token_konfirmasi = None  # Hapus token
                    user.AtsumaruKanjo += 100
                    await user.save()
                    raise HTTPException(detail='token konfirmasi yang anda masukan salah', status_code=404)
                else:
                    # gak terhubung dengan auth lain , hapus data pengguna
                    await user.delete()  # Hapus data pengguna
                    raise HTTPException(detail='token konfirmasi yang anda masukan salah', status_code=404)
        else:
            # User tidak ditemukan
            raise HTTPException(detail='pengguna tidak ditemukan', status_code=404)
    else:
        raise HTTPException(detail='passowrd dan konfirmasi password tidak sama', status_code=418)

@router.get('/root')
async def submit(request: Request, token: str, tujuan: Optional[str] = None, access_token: str = Cookie(default=None)):
    if tujuan == 'register':
        target_url = config.redirect_uri_update
    else:
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