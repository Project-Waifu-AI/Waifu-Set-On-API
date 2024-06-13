from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse

from io import BytesIO
import uuid
import httpx

from database.model import AudioData

from configs import config

from helper.access_token import check_access_token_expired, decode_access_token
from helper.cek_and_set import cek_data_user, set_karakter_id
from helper.fitur import request_audio

from handler.response.basic import error_response
from handler.response.fitur import audio_management_response

router = APIRouter(prefix='/audio-data', tags=['Audio-Data'])

@router.get('/stream/{service}/{UUID}')
async def stream_audio(service: str, UUID: str, email: str):
    user = cek_data_user(namaORemail=email)
    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='stream-audio-data'), status_code=404)
        
    audio_data = await user.audio_data.get_or_none(UUID_number=uuid.UUID(UUID), service=service)
    if audio_data is None:
        raise HTTPException(error_response(pesan='sorry your audio was not found please create audio data using the available features.', penyebab='audio data not found', kepada=email), status_code=404)
    
    audio_stream = BytesIO(audio_data.audio_data)

    return StreamingResponse(audio_stream, media_type="audio/mpeg")

@router.get('/source/{service}/{UUID}')
async def get_source(service: str, UUID: str, email: str):
    user = cek_data_user(namaORemail=email)

    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='stream-audio-data'), status_code=404)
    
    # audio_data = await AudioData.get_or_none(user=user, UUID_number=uuid.UUID(UUID), service=service)
    audio_data = await user.audio_data.get_or_none(UUID_number=uuid.UUID(UUID), service=service)
    if audio_data is None:
        raise HTTPException(error_response(pesan='sorry your audio was not found please create audio data using the available features.', penyebab='audio data not found', kepada=email), status_code=404)
    
    karakter_id = set_karakter_id(nama=audio_data.character)
    if karakter_id is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)

    audio_url = request_audio(text=audio_data.japanese_text, speaker_id=karakter_id)
    if audio_url['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=audio_url['penyebab'], action='obrolan-gpt-aiu'), status_code=500)
    
    return JSONResponse(audio_management_response(url_source=audio_url['streaming_audio'], service=audio_data.service, character=audio_data.character), status_code=200)

@router.get('/source-stream/{service}/{UUID}')
async def get_source(service: str, UUID: str, email: str):
    user = cek_data_user(namaORemail=email)

    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='stream-audio-data'), status_code=404)
    
    audio_data = await user.audio_data.get_or_none(UUID_number=uuid.UUID(UUID), service=service)
    if audio_data is None:
        raise HTTPException(error_response(pesan='sorry your audio was not found please create audio data using the available features.', penyebab='audio data not found', kepada=email), status_code=404)
     
    karakter_id = set_karakter_id(nama=audio_data.character)
    if karakter_id is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)

    audio_url = request_audio(text=audio_data.japanese_text, speaker_id=karakter_id)
    if audio_url['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=audio_url['penyebab'], action='obrolan-gpt-aiu'), status_code=500)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(audio_url['streaming_audio'], stream=True)
        return StreamingResponse(response.aiter_bytes(), media_type="audio/mpeg")