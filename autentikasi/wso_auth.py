from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import random
from body_request.auth_body_request import LoginWSO, SimpanUserWSO
from database.model import userdata
from webhook.send_email import send
from helping.auth_helper import check_password, create_access_token, validation_email, set_password, userIni, valid_password
from helping.response_helper import pesan_response, user_response
from webhook.send_email import send
from configs import config

router = APIRouter(prefix='/wso-auth', tags=['Waifu-Set-On-autentikasi'])

@router.post('/login')
async def login_wso(meta: LoginWSO):
    user = await userIni(namaORemail=meta.emailORname)
    
    if user is False:
        raise HTTPException(detail='nama, email anda masih belum terdaftar', status_code=403)

    if user.akunwso is False:
        return RedirectResponse(config.redirect_uri_page_masuk, status_code=404)
    
    else:
        if not check_password(password=meta.password, user=user):
            raise HTTPException(status_code=401, detail="nama, email atau password yang anda masukan salah")
        else:
            try:
                access_token = create_access_token(user=user)
                return JSONResponse(content={'access_token': str(access_token)}, status_code=200)
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=500)
    
@router.post('/register/{email}')
async def register(email: str):
    token_konfirmasi = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    user = await userdata.filter(email=email).first()
    validasi_email = validation_email(email=email)
    
    if validasi_email is False:
        raise HTTPException(status_code=400, detail="email yang anda masukan tidak valid")
    
    if user:
        if user.ban:
            raise HTTPException(status_code=403, detail="akun anda telah di ban")
        else:
            if user.akunwso is False:
                sendEmail01=send(target_email=email, token=token_konfirmasi)
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
                raise HTTPException(detail='email anda telah terdaftar pada akunbw tidak dapat membuat lagi', status_code=403)
    else:
        sendEmail02 = send(target_email=email, token=token_konfirmasi)
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
async def simpan_user(meta: SimpanUserWSO):
    user = await userdata.filter(email=meta.email).first()

    if meta.password == meta.konfirmasi_password:
        if valid_password(meta.password) is False:
            raise HTTPException(detail='password anda kurang mantap man, minimal 8 karakter, kombinasi Lower dan Upper case huruf dan ditambahkan angka juga', status_code=400) 
        
        if user:
            if user.token_konfirmasi and user.token_konfirmasi == meta.token:
                # Token cocok dengan pengguna
                try:
                    user.password = set_password(password=meta.password)  # Setel kata sandi baru
                    user.akunwso = True  # Setel akunwso menjadi Aktif
                    user.token_konfirmasi = None  # Hapus token
                    user.AtsumaruKanjo += 100
                    await user.save()
                    access_token = create_access_token(user=user)
                    return JSONResponse({'access_token':str(access_token)}, status_code=201)
                except Exception as e:
                    raise HTTPException(detail=str(e), status_code=500)
            else:
                # Token tidak cocok dengan pengguna
                if user.googleAuth is True:
                    # Akun pengguna google auth aktif, hapus token
                    user.token_konfirmasi = None  # Hapus token
                    user.AtsumaruKanjo += 100
                    await user.save()
                    user_data = user_response(user=user)
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