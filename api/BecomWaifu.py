from fastapi import APIRouter, HTTPException, Header, UploadFile, File
from fastapi.responses import JSONResponse, RedirectResponse
from pydub import AudioSegment
import speech_recognition as sr
from io import BytesIO
import os
import tempfile
import tweepy
import requests
from configs import config
from database.model import logaudio, userdata
from helping.response_helper import pesan_response
from helping.auth_helper import check_access_token_expired, decode_access_token, check_premium
from helping.action_helper import request_audio, to_japan, cek_bahasa, to_japan_premium

r = sr.Recognizer()
router = APIRouter(prefix='/BecomeWaifu', tags=['BecomeWaifu-action'])

@router.post('/change-voice/{speaker_id}')
async def change_voice(speaker_id: int, bahasa: str, audio_file: UploadFile = File(...), access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    premium_check = await check_premium(email=email)
    if premium_check['status'] is False:
        user_audio_count = await logaudio.filter(email=email).count()
        if user_audio_count >= 10:
            raise HTTPException(detail='logaudio data anda telah mencapai limit. Upgrade ke plan premium atau hapus logaudio.', status_code=400)
    
    user_data = await logaudio.filter(email=email).order_by("-audio_id").first()
    if user_data:
        audio_id = user_data.audio_id + 1
    else:
        audio_id = 1  
    format_audio: str = audio_file.content_type
    print(format_audio)
    if audio_file.content_type not in ['audio/wav', 'audio/x-wav', 'audio/aiff', 'audio/x-aiff', 'audio/flac']:
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio = AudioSegment.from_file(audio_file.file, format=format_audio.split("/", 1)[-1]) 
        audio.export(temp_wav.name, format="wav")
        audio_file = temp_wav
    with sr.AudioFile(audio_file.file) as audio_file:
        audio_data = r.record(audio_file)
        bahasaYangDigunakan = cek_bahasa(bahasa=bahasa)
        if bahasaYangDigunakan['status'] is False:
            raise HTTPException(detail=bahasaYangDigunakan['keterangan'], status_code=404)
        transcript = r.recognize_google(audio_data, language=bahasaYangDigunakan['keterangan'])
    if premium_check['status'] is True:
        if premium_check['keterangan'] == 'bw' or premium_check['keterangan'] == 'admin':
            translation = to_japan_premium(transcript)
        else:
            translation = to_japan(transcript)
    else:
        translation = to_japan(transcript)

    if translation['status'] is True:
        data_audio = request_audio(text=translation['response'], speaker_id=speaker_id)
        if data_audio['status'] is False:
            raise HTTPException(detail='eror audio request', status_code=500)
        save = logaudio(audio_id=audio_id, email=email, transcript=transcript, translate=translation['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
        await save.save()
        data=[{
            'email': email,
            'audiId': audio_id,
            'transcript': transcript,
            'translation': translation['response']
        }]
        data.append(data_audio)
        return JSONResponse(content=data, status_code=200)
    else:
        raise HTTPException(detail=translation, status_code=500)
    
@router.get('/get-all-logaudio/{audio}')
async def get_all_logaudio(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    user_data = await logaudio.filter(email=email).all()
    if user_data:
        result = []
        for logaudio_entry in user_data:
            logaudio_data = {
                "email": logaudio_entry.email,
                "audio_id": logaudio_entry.audio_id,
                "transcript": logaudio_entry.transcript,
                "translate": logaudio_entry.translate,
                'audio_download': logaudio_entry.audio_download
            }
            result.append(logaudio_data)
        return JSONResponse(result, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="logaudio tidak ditemukan")
    
@router.delete("/delete-audio/{audio_id}")
async def delete_audio(audio_id: int, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    try:
        audio_data = await logaudio.filter(email=email, audio_id=audio_id).first()
        if audio_data:
            await audio_data.delete()
            audio_to_update = await logaudio.filter(email=email, audio_id__gt=audio_id).all()
            for audio in audio_to_update:
                audio.audio_id -= 1
                await audio.save()
            response = pesan_response(email=audio_data.email, pesan=f'audio data dengan log-audio {audio_id} telah dihapus')
            return JSONResponse(response, status_code=200)
        else:
            raise HTTPException(detail=f'audio data dengan log-audio {audio_id} tidak ditemukan', status_code=404)
    
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(detail=str(err), status_code=500)
"""
@router.post('/save-audio-to-drive')
async def saveDrive(audio_id: int, access_token: str = Header):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub') 
"""