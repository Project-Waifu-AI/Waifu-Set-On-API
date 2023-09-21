from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, Cookie, Header
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated
import io
import speech_recognition as sr
from configs import config
from database.model import logpercakapan, userdata
from helping.auth_helper import check_access_token_expired, check_premium_becomewaifu
from helping.action_helper import request_audio, to_japan, to_japan_premium

router = APIRouter(prefix='/websocket', tags=['websocket'])
r = sr.Recognizer()
'''
@router.websocket('/change-voice/{speakerId}/{bahasaYangDigunakan}')
async def change_voice(
    websocket: WebSocket,
    speakerId: int,
    BahasaYangDigunakan: int,
    access_token: Annotated[str| None, Cookie()] = None,
    ):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        check = await check_access_token_expired(access_token=access_token)
        if check is True:
            await websocket.close(code=1000, reason="access_token anda sudah basi silahkan login lagi.")
            return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
        elif check is False:
            await websocket.close(code=1000, reason="access_token anda tidak ditemukan.")
            return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
        else:
            user_id = check
        # procress bytes to a temporary audio file
        audio_file = blablablabala
        with sr.AudioFile(audio_file.file) as audio_file:
            audio_data = r.record(audio_file)
            transcript = r.recognize_google(audio_data, language=BahasaYangDigunakan)
'''

@router.websocket('/obrolan')
async def obrolan(
    websocket: WebSocket,
    speakerId: int,
    access_token: Annotated[str| None, Cookie()] = None 
    ):
    await websocket.accept()
    while True:
        pesan = await websocket.receive_text()
        check = await check_access_token_expired(access_token=access_token)
        if check is True:
            await websocket.close(code=1000, reason="access_token anda sudah basi silahkan login lagi.")
            return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
        elif check is False:
            await websocket.close(code=1000, reason="access_token anda tidak ditemukan.")
            return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
        else:
            user_id = check
        
        user_data = await logpercakapan.filter(user_id=user_id).order_by("-id_percakapan").first()
        if user_data:
            id_percakapan = user_data.id_percakapan + 1
        else:
            id_percakapan = 1  
        response = await obrolan(input_text=pesan, userid=user_id)
        user = await userdata.filter(user_id=user_id).first()
        
        if user.premium is True:
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