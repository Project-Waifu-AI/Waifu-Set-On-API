from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, RedirectResponse
from body_request.dw_body_request import createWaifu
from helper.fitur import generateWaifu
from database.model import logdelusion
from helper.access_token import check_access_token_expired, decode_access_token
from configs import config

router = APIRouter(prefix='/DW',tags=['Delusion-Waifu'])

@router.post('/create-waifu')
async def createWaifu(meta: createWaifu, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    user_data_count = await logdelusion.filter(email=email).count()
    if user_data_count >= 50:
        raise HTTPException(detail='logaudio data anda telah mencapai limit. Upgrade ke plan premium atau hapus logaudio.', status_code=400)
    
    user_data = await logdelusion.filter(email=email).order_by("-audio_id").first()
    
    if user_data:
        delusion_id = user_data.delusion_id + 1
    else:
        delusion_id = 1
        
    