from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from handler.request.user import updateUser, updatePassword
from configs import config
from database.model import UserData
from send.email import send_password_change
from helper.access_token import check_access_token_expired, decode_access_token, create_access_token
from helper.cek_and_set import cek_data_user, cek_namaku_ada, cek_valid_password, set_password
from handler.response.basic import success_response, error_response
from handler.response.data import user_response

router = APIRouter(prefix='/user-wso', tags=['user-data'])

@router.put('/update')
async def update_userData(meta: updateUser, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    user = await UserData.get_or_none(email=email)
    if user is None:
        raise HTTPException(detail=error_response(pesan='User data not found, please repeat the request', penyebab='user not found', action='update-data-user-root'), status_code=404)
    
    if meta.nama:
        user.nama = meta.nama
        if await cek_namaku_ada(nama=meta.nama) == True:
            await user.save()
        else:
            raise HTTPException(detail=error_response(penyebab='the name you want is already used by another user', pesan='The name you want has been used by another user, please try again using a different name', kepada=email, action='update-data-user-root'), status_code=405)
        
    if meta.gender:
        if meta.gender in ('man', 'woman'):
            user.gender = meta.gender
            await user.save()
        else:
            raise HTTPException(detail=error_response(pesan='The gender you entered is invalid. Please re-select the gender according to the options', penyebab='The gender you selected is invalid', kepada=email, action='update-data-user-root'), status_code=403)
    
    if meta.ulang_tahun is not None:
        user.birth_date = meta.ulang_tahun
        await user.save()
    
    return JSONResponse(success_response(kepada=user.email, action='update-data-user-root', pesan='user data has been updated successfully'), status_code=201)
    
@router.get('/get')
async def user_data(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
          
    user = await UserData.get_or_none(email=email)
    if user is None:
        raise HTTPException(detail=error_response(pesan='User data not found, please repeat the request', penyebab='user not found', action='get-data-user-root'), status_code=404)
    
    response = user_response(user=user)
    return JSONResponse(response, status_code=200)

@router.post('/forgot-password')
async def forgotPassword(email:str):
    user = await cek_data_user(namaORemail=email)
    
    if user is False:
        raise HTTPException(detail=error_response(pesan='User data not found, please repeat the request', penyebab='user not found', action='forgot-password-user-root'), status_code=404)
    
    access_token = await create_access_token(user=user, permintaan='change-password')
    send = await send_password_change(target_email=email, access_toke=access_token)
    
    if send is True:
        return JSONResponse(success_response(kepada=email, action='forgot-password-user-root', pesan='A message to update your password has been sent to your email. Please check your email to take the next step'), status_code=201)
    
    raise HTTPException(detail=error_response(pesan='something gone weong', action='forgot-password-user-root', kepada=email, penyebab=send), status_code=500)

@router.put('/change-password')
async def want_change_password(request: Request, meta: updatePassword):
    access_token = request.query_params.get("access_token")

    check = check_access_token_expired(access_token=access_token)
    if check is True:
        raise HTTPException(detail=error_response(pesan='Your request to change the password is invalid. Please repeat your request again to change the password', penyebab='Your request to change your password is invalid', action='change-password-user-root'), status_code=403)
    
    payloadJWT = decode_access_token(access_token=access_token)
    permintaan = payloadJWT.get('permintaan')
    email = payloadJWT.get('sub')
    
    if permintaan != 'change-password':
        raise HTTPException(detail=error_response(pesan='Your access request is invalid', penyebab='your request in the query is invalid', kepada=email, action='change-password-user-root'), status_code=403)
    
    valid = cek_valid_password(password=meta.password)
    if valid is False:
        error_response(pesan='')
        raise HTTPException(detail=error_response(pesan='The password must consist of 8 characters, a combination of lowercase and uppercase letters and numbers added as well', kepada=user.email, penyebab='password is not valid', action='change-password-user-root'), status_code=403)

    if meta.password is not meta.konfirmasi_password:
        raise HTTPException(detail=error_response(pesan='The password and confirmation password you entered are not the same, please try again', penyebab='The password and confirmation password you entered are not the same', action='change-password-root-user', kepada=email), status_code=403)
    
    user = await UserData.get_or_none(email=email)
    user.auth.password = set_password(password=meta.password)
    user.save()

    return JSONResponse(success_response(kepada=user.email, action='change-password-user-root', pesan='Your password has been successfully changed'), status_code=201)
    
@router.delete('/delete-account')
async def deleteAcount(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    user = await UserData.get_or_none(email=email)
    if user is None:
        raise HTTPException(detail=error_response(pesan='User data not found, please repeat the request', penyebab='user not found', action='delete-account-user-root'), status_code=404)
    
    await user.delete()

    repsonse = success_response(kepada=email, pesan='Your account has been successfully deleted, thank you for using our service Waifu-Set-On', action='delete-account-user-root')
    return JSONResponse (repsonse, status_code=201)