from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, RedirectResponse
import requests
import base64
from io import BytesIO
import tempfile
from body_request.dw_body_request import CreateDelusion
from helper.premium import check_premium
from helper.fitur import generateDelusion
from helper.cek_and_set import cek_kalimat_promting, cek_and_set_ukuran_delusion
from database.model import logdelusion
from helper.access_token import check_access_token_expired, decode_access_token
from configs import config

router = APIRouter(prefix='/DW',tags=['Delusion-Waifu'])

@router.post('/create-delusion')
async def createWaifu(meta: CreateDelusion, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    if cek_kalimat_promting(kalimat=meta.input) is True:
        raise HTTPException(detail='prompt is forbiden', status_code=400)
    
    premium_check = await check_premium(email=email)
    if premium_check['status'] is False or premium_check['status'] is True and premium_check['keterangan'] != 'dw':    
        user_audio_count = await logdelusion.filter(email=email).count()
        if user_audio_count >= 50:
            raise HTTPException(detail='anda terlalu banyak menghayal dan anda juga miskin dimohon istirahat.', status_code=400)
        if meta.jumlah >= 3:
            raise HTTPException(detail='sadar dirilah coy lu gak premium sekali buat mau lebih dari 2 gilak lu', status_code=400)
        premium = False
    elif premium_check['status'] == True and premium_check == 'dw':
        if meta.jumlah >= 5:
            raise HTTPException(detail='bang udahlah jangan buat banyak banyak sekali jalan atuh', status_code=400)
        premium = True
    
    user_data = await logdelusion.filter(email=email).order_by("-delusion_id").first()
    if user_data:
        delusion_id = user_data.delusion_id + 1
    else:
        delusion_id = 1
        
    ukuran_hitung = cek_and_set_ukuran_delusion(meta.ukuran)
    if ukuran_hitung is False:
        raise HTTPException(detail='ukurannya salah bro', status_code=400)    
    create = generateDelusion(prompt=meta.input, ukuran=ukuran_hitung, premium=premium, jumlah=meta.jumlah)
    
    if create['status'] is False:
        raise HTTPException(detail=create['keterangan'], status_code=500)
    
    try:
        get_images = requests.get(url=create['keterangan'])
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    
    save = logdelusion(
        delusion_id=delusion_id,
        email=email,
        delusion_prompt=meta.input,
        delusion_shape=meta.ukuran,
        delusion_result=BytesIO(get_images.content)
    )
    await save.save()
    response = {
        'delusion_id': delusion_id,
        'delusion_shape': meta.ukuran,
        'delusion_image': str(create['keterangan'])
    }

    return JSONResponse(content=response, status_code=200)


'''    
@router.put('/variant-delusion')
async def variantWaifu(input: str, access_token: str = Header):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    if cek_kalimat_promting(kalimat=meta.input) is False:
        raise HTTPException(detail='prompt is forbiden', status_code=400)
    
    premium_check = await check_premium(email=email)
    if premium_check['status'] is False or premium_check['status'] is True and premium_check['keterangan'] != 'dw':    
        user_audio_count = await logdelusion.filter(email=email).count()
        if user_audio_count >= 50:
            raise HTTPException(detail='anda terlalu banyak menghayal dan anda juga miskin dimohon istirahat.', status_code=400)
        if meta.jumlah >= 3:
            raise HTTPException(detail='sadar dirilah coy lu gak premium sekali buat mau lebih dari 2 gilak lu', status_code=400)
        premium = False
    elif premium_check['status'] == True and premium_check == 'dw':
        if meta.jumlah >= 5:
            raise HTTPException(detail='bang udahlah jangan buat banyak banyak sekali jalan atuh', status_code=400)
        premium = True
        
'''