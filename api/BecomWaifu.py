from fastapi import APIRouter, HTTPException, Header, UploadFile, File, Form, Response
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse, StreamingResponse
from pydub import AudioSegment
from googletrans import Translator
import speech_recognition as sr
import tempfile
import base64
from configs import config
from database.model import logaudio, userdata
from helping.response_helper import pesan_response
from helping.auth_helper import check_access_token_expired, check_premium
from helping.action_helper import request_audio, blob_to_wav

translator = Translator()
r = sr.Recognizer()
router = APIRouter(prefix='/BecomeWaifu', tags=['BecomeWaifu-action'])

@router.post('/change-voice')
async def change_voice(BahasaYangDigunakan: str, SpeakerId: str, access_token: str = Header(...), audio_file: UploadFile = File(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check

    premium_check = await check_premium(user_id=user_id)
    if premium_check:
        raise HTTPException(status_code=400, detail=premium_check)
    
    user_data = await logaudio.filter(user_id=user_id).order_by("-audio_id").first()
    if user_data:
        audio_id = user_data.audio_id + 1
    else:
        audio_id = 1  

    if audio_file.content_type not in ['audio/wav', 'audio/x-wav', 'audio/aiff', 'audio/x-aiff', 'audio/flac']:
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio = AudioSegment.from_file(audio_file.file, format="mp3")  # Adjust format as needed
        audio.export(temp_wav.name, format="wav")
        audio_file = temp_wav

    with sr.AudioFile(audio_file.file) as audio_file:
        audio_data = r.record(audio_file)
        transcript = r.recognize_google(audio_data, language=BahasaYangDigunakan)
    
    translation = translator.translate(transcript, dest='ja')
    await request_audio(spaeker_id=SpeakerId, text=translation.text)
    
    with open("voice.wav", "rb") as file:
        audio_rb = file.read()

    save = logaudio(audio_id=audio_id, user_id=user_id, transcript=transcript, translate=translation.text, audio_file=audio_rb)
    await save.save()
    return FileResponse('voice.wav', media_type='audio/wav')

@router.get('/audio-response/{audio_id}')
async def audio_response(audio_id: int, access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check

    try:
        audio_data = await logaudio.filter(user_id=user_id, audio_id=audio_id).first()
        if audio_data:
            def chunk():
                yield from base64.b64encode(audio_data.audio_file).decode('utf-8')
            return StreamingResponse(content=chunk(), media_type='audio/wav')
        else:
            raise HTTPException(status_code=404, detail=f'audio data dengan audio-id {audio_id} tidak ditemukan')
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)

@router.get('/test')
async def test():
    audio_data = await logaudio.filter(user_id='ea2d3023-65ee-455b-a053-e583b28e84ee', audio_id=1).first()
    def chunk():
        yield from base64.b64encode(audio_data.audio_file).decode('utf-8')

    return StreamingResponse(content=chunk(), media_type='audio/wav')

@router.get('/get-audio-file/{audio_id}')
async def get_audio_file(audio_id: int, access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check

    try:
        user = await userdata.filter(user_id=user_id).first()
        audio_data = await logaudio.filter(user_id=user_id, audio_id=audio_id).first()
        if audio_data:
            await blob_to_wav(data_audio=audio_data.audio_file)
            audio_file = 'voice.wav'
            return FileResponse(audio_file, media_type="audio/wav")
        else:
            raise HTTPException(detail=f'audio data dengan log-audio {audio_id} tidak ditemukan', status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/get-all-logaudio/{audio}')
async def get_all_logaudio(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check
    
    user_data = await logaudio.filter(user_id=user_id).all()
    if user_data:
        result = []
        for logaudio_entry in user_data:
            logaudio_data = {
                "user_id": logaudio_entry.user_id,
                "audio_id": logaudio_entry.audio_id,
                "user_id": logaudio_entry.user_id,
                "transcript": logaudio_entry.transcript,
                "translate": logaudio_entry.translate
            }
            result.append(logaudio_data)
        return JSONResponse(result, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="logaudio tidak ditemukan")
    
@router.delete("/delete-audio/{audio_id}")
async def delete_audio(audio_id: int, access_token: str = Header(...)):
    result = await check_access_token_expired(access_token=access_token)
    if result is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif result is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = result
    try:
        audio_data = await logaudio.filter(user_id=user_id, audio_id=audio_id).first()
        user = await userdata.filter(user_id=user_id).first()
        if audio_data:
            await audio_data.delete()
            audio_to_update = await logaudio.filter(user_id=user_id, audio_id__gt=audio_id).all()
            for audio in audio_to_update:
                audio.audio_id -= 1
                await audio.save()
            response = pesan_response(email=user.email, pesan=f'audio data dengan log-audio {audio_id} telah dihapus')
            return JSONResponse(response, status_code=200)
        else:
            raise HTTPException(detail=f'audio data dengan log-audio {audio_id} tidak ditemukan', status_code=404)
    
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(detail=str(err), status_code=500)