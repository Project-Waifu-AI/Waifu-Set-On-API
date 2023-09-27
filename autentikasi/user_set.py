from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from body_request.auth_body_request import updateUser
from configs import config
from database.model import userdata
from helping.auth_helper import check_access_token_expired
from helping.response_helper import pesan_response, user_response

router = APIRouter(prefix='/user', tags=['user-data'])

@router.put('/update-user-data')
async def update_userData(meta: updateUser, access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check

    user = await userdata.filter(user_id=user_id).first()
    if user:
        if meta.nama:
            user.nama = meta.nama
            await user.save()
        if meta.gender:
            if meta.gender in ('pria', 'perempuan'):
                user.gender = meta.gender
                await user.save()
            else:
                raise HTTPException(detail='gender yang anda masukan tidak valid', status_code=400)
        if meta.ulang_tahun is not None:
            user.ulang_tahun = meta.ulang_tahun
            await user.save()
        response = pesan_response(email=user.email, pesan=f'data user dengan id {user_id} telah berhasil di update')
        return JSONResponse(response, status_code=200)
    else:
        raise HTTPException(status_code=404, detail='data user tidak ditemukan')
    
@router.get('/user-data')
async def user_data(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check

    user = await userdata.filter(user_id=user_id).first()
    response = user_response(user=user)
    return JSONResponse(response, status_code=200)

@router.delete('/delete-account')
async def deleteAcount(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check

    user = await userdata.filter(user_id=user_id).first()
    await user.delete()
    repsonse = pesan_response(email=user.email, pesan='akun anda telah berhasil dihapus')
    return JSONResponse (repsonse, status_code=200)