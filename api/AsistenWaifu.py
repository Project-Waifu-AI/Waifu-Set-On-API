from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import logpercakapan, userdata
from helping.action_helper import obrolan, to_japan, request_audio, to_japan_premium
from helping.response_helper import pesan_response
from helping.auth_helper import check_access_token_expired, decode_access_token, check_premium_AI_U
from configs import config

router = APIRouter(prefix='/AsistenWaifu', tags=['AsistenWaifu-action'])

@router.get('/pesan')
async def pesan(speakerId: int, pesan: str, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        user_id = payloadJWT.get('sub')

    user_data = await logpercakapan.filter(user_id=user_id).order_by("-id_percakapan").first()
    if user_data:
        id_percakapan = user_data.id_percakapan + 1
    else:
        id_percakapan = 1  
    response = await obrolan(input_text=pesan, userid=user_id)
    user = await userdata.filter(user_id=user_id).first()
    
    premium = check_premium_AI_U(user=user)
    if premium is False:
        translate = to_japan(input=response)
    elif premium is False:
        translate = to_japan_premium(input=response)
    else:
        translate = to_japan(input=response)

    data_audio = request_audio(text=translate, speaker_id=speakerId)
    data = [{
        'pesan': pesan,
        'response': response,
        'translate': translate,
    }]
    data.append(data_audio)
    save = logpercakapan(id_percakapan=id_percakapan, user_id=user_id, input=pesan, output=response, translate=translate, audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
    await save.save()
    return JSONResponse (data)
    
@router.delete('/delete-obrolan')
async def delete_obrolan(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        user_id = payloadJWT.get('sub')
        
    try:
        user = await userdata.filter(user_id=user_id).first()
        await logpercakapan.filter(user_id=user_id).delete()
        response = pesan_response(email=user.email, pesan='log obrolan berhasil dihapus')
        return JSONResponse(response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))