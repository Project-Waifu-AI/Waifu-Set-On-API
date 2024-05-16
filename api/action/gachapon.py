from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from helper.gacha_logic import gacha_pull, get_user_data, get_gacha_history
from helper.access_token import check_access_token_expired, decode_access_token
from configs import config

router = APIRouter(prefix='/gacha', tags=['gachapon system'])

@router.get("/karakteryangdimiliki")
async def get_obtained_characters(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    user_data = await get_user_data(email)
    if user_data:
        return {"karakterYangDimiliki": user_data.karakterYangDimiliki}
    else:
        return {"message": "User not found"}
    
@router.get("/gacha/single/non-limited")
async def gacha_single_non_limited(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    email = email
    results = await gacha_pull(email, 1, limited=False)
    return [char.nama for char in results]

@router.get("/gacha/multi/non-limited")
async def gacha_multi_non_limited(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    email = email
    results = await gacha_pull(email, 10, limited=False)
    return [char.nama for char in results]
    

@router.get("/gacha/single/limited")
async def gacha_single_limited(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    email = email
    results = await gacha_pull(email, 1, limited=True)
    return [char.nama for char in results]
    

@router.get("/gacha/multi/limited")
async def gacha_multi_limited(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    email = email
    results = await gacha_pull(email, 10, limited=True)
    return [char.nama for char in results]


@router.get("/gacha/history")
async def gacha_history(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    history = await get_gacha_history(email)
    return history