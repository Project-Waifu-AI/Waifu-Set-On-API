from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from configs import config
from helping.response_helper import pesan_response
from helping.auth_helper import check_access_token_expired, decode_access_token, create_token_premium

router = APIRouter(prefix='/premium-regis', tags=['premium'])

@router.put('/plan-wso')
async def daftarPremium(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    create_premium_data = await create_token_premium(email=email, plan='wso')
    if create_premium_data['status'] is False:
        raise HTTPException(detail=create_premium_data['keterangan'], status_code=500)
    return JSONResponse(pesan_response(pesan=create_premium_data['keterangan']))

@router.put('/plan-bw')
async def daftarPremium(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    create_premium_data = await create_token_premium(email=email, plan='bw')
    if create_premium_data['status'] is False:
        raise HTTPException(detail=create_premium_data['keterangan'], status_code=500)
    return JSONResponse(pesan_response(pesan=create_premium_data['keterangan']))

@router.put('/plan-aiu')
async def daftarPremium(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    create_premium_data = await create_token_premium(email=email, plan='ai-u')
    if create_premium_data['status'] is False:
        raise HTTPException(detail=create_premium_data['keterangan'], status_code=500)
    return JSONResponse(pesan_response(pesan=create_premium_data['keterangan']))

