from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import random
from body_request.auth_body_request import LoginWSO, SimpanUserWSO
from database.model import userdata
from webhook.send_email import send
from helping.auth_helper import check_password, create_access_token, validation_email, set_password
from helping.response_helper import access_token_response, pesan_response, user_response
from webhook.send_email import send
from database.model import userdata
from configs import config

router = APIRouter(prefix='/wso-auth', tags=['Waifu-Set-On-autentikasi'])

@router.post('/login')
async def login_wso(meta: LoginWSO):
    user = await userdata.filter(email=meta.email).first()

    if user:
        if user.akunwso is False:
            return RedirectResponse(config.redirect_uri_page_masuk)
        else:
            if not check_password(password=meta.password, user=user):
                raise HTTPException(status_code=401, detail="password anda salah")
            await create_access_token(user=user)
            response = await access_token_response(user=user, password=meta.password)
            return JSONResponse(response, status_code=200)
    else:
        raise HTTPException(status_code=403, detail="anda masih belum mendaftar")
    
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
            if user.googleAuth is True:
                send(target_email=email, token=token_konfirmasi)
                user.token_konfirmasi = token_konfirmasi
                await user.save()
                response = pesan_response(email=email, pesan=f'token konfirmasi telah dikirimakan')
                return JSONResponse(response, status_code=200)
            if user.akunwso is True:
                raise HTTPException(detail='email anda telah terdaftar pada akunbw tidak dapat membuat lagi', status_code=403)
    else:
        send(target_email=email, token=token_konfirmasi)
        save = userdata(email=email, token_konfirmasi=token_konfirmasi, NegaiKanjo=0)
        await save.save()
        response = pesan_response(email=email, pesan=f'token konfirmasi telah dikirimakan')
        return JSONResponse(response, status_code=200)
    
@router.post('/simpan-user')
async def simpan_user(meta: SimpanUserWSO):
    user = await userdata.filter(email=meta.email).first()

    if meta.password == meta.konfirmasi_password:
        if user:
            if user.token_konfirmasi and user.token_konfirmasi == meta.token:
                # Token cocok dengan pengguna
                user.password = set_password(password=meta.password)  # Setel kata sandi baru
                user.akunwso = True  # Setel akunwso menjadi Aktif
                user.token_konfirmasi = None  # Hapus token
                user.NegaiKanjo += 100
                await user.save()
                await create_access_token(user=user)
                access_token = await access_token_response(user=user, password=meta.password)
                return JSONResponse(access_token, status_code=201)
            else:
                # Token tidak cocok dengan pengguna
                if user.googleAuth is True:
                    # Akun pengguna google auth aktif, hapus token
                    user.token_konfirmasi = None  # Hapus token
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