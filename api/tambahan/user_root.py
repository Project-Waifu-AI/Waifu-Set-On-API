from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from body_request.auth_body_request import updateUser, updatePassword
from configs import config
from database.model import userdata
from webhook.send_email import send_password_change
from helping.auth_helper import check_access_token_expired, decode_access_token, apakahNamakuAda, userIni, create_access_token, valid_password, set_password
from helping.response_helper import pesan_response, user_response

router = APIRouter(prefix='/user-root', tags=['user-data'])

@router.put('/update-data')
async def update_userData(meta: updateUser, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    user = await userdata.filter(email=email).first()
    if user:
        try:    
            if meta.nama:
                user.nama = meta.nama
                if await apakahNamakuAda(nama=meta.nama) == True:
                    await user.save()
                else:
                    raise HTTPException(detail='nama yang ingin anda gunakan sudah digunakan oleh orang lain', status_code=405)
                
            if meta.gender:
                if meta.gender in ('pria', 'perempuan'):
                    user.gender = meta.gender
                    await user.save()
                else:
                    raise HTTPException(detail='gender yang anda masukan tidak valid', status_code=400)
            
            if meta.ulang_tahun is not None:
                user.ulang_tahun = meta.ulang_tahun
                await user.save()
            response = pesan_response(email=user.email, pesan=f'data user {email} telah berhasil di update')
            return JSONResponse(response, status_code=200)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
    else:
        raise HTTPException(status_code=404, detail='data user tidak ditemukan')
    
@router.get('/get-data')
async def user_data(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
          
    user = await userdata.filter(email=email).first()
    
    if user is None:
        raise HTTPException(detail='user data not found', status_code=404)
    response = user_response(user=user)
    return JSONResponse(response, status_code=200)


@router.post('/forgot-password')
async def forgotPassword(email:str):
    user = await userIni(namaORemail=email)
    
    if user is False:
        raise HTTPException(detail='your email is not found', status_code=404)
    else:
        access_token = await create_access_token(user=user, permintaan='change-password')
        send = await send_password_change(target_email=email, access_toke=access_token)
        if send is True:
            return JSONResponse(pesan_response(email=email, pesan='email untuk melakukan reset password sudah dikirimkan ke email anda'), status_code=200)
        else:
            raise HTTPException(detail=send, status_code=500)

@router.get('/change-password')
async def want_change_password(request: Request, meta: updatePassword):
    access_token = request.query_params.get("access_token")
    if meta.password == meta.konfirmasi_password:
        check = check_access_token_expired(access_token=access_token)
        if check is True:
            raise HTTPException(detail='kirimkan permintaan ulang untuk reset password')
        elif check is False:
            payloadJWT = decode_access_token(access_token=access_token)
            permintaan = payloadJWT.get('permintaan')
            email = payloadJWT.get('sub')
            if permintaan != 'change-password':
                raise HTTPException(detail='permintaan tidak valid', status_code=403)
            valid = valid_password(password=meta.password)
            if valid is False:
                raise HTTPException(detail='password anda lemah coy', status_code=400)
            user = await userdata.filter(email=email).first()
            user.password = set_password(password=meta.password)
            user.save()
            return JSONResponse(pesan_response(email=user.email, pesan='password anda telah berhasil di update'), status_code=200)
    else:
        raise HTTPException(detail='password anda dengan konfirmasi password tidak sama', status_code=400)

@router.delete('/delete-account')
async def deleteAcount(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub') 
    user = await userdata.filter(email=email).first()
    if user is None:
        raise HTTPException(detail='user tidak ditemukan', status_code=404)
    await user.delete()
    repsonse = pesan_response(email=user.email, pesan='akun anda telah berhasil dihapus')
    return JSONResponse (repsonse, status_code=200)