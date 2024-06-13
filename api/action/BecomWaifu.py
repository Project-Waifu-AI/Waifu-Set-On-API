from fastapi import APIRouter, HTTPException, Header, UploadFile, File
from fastapi.responses import JSONResponse, RedirectResponse

from pydub import AudioSegment
import speech_recognition as sr

import tempfile

from configs import config

from database.model import UserData, BWResult, AudioData

from handler.request.bw import shareToSMD
from handler.response.basic import success_response, error_response
from handler.response.fitur import bw_response

from helper.access_token import check_access_token_expired, decode_access_token
from helper.premium import check_premium
from helper.fitur import request_audio, download_audio
from helper.cek_and_set import set_karakter_id, cek_data_user
from helper.translate import cek_bahasa, translate_target, translate_target_premium
# from helper.drive_google import simpanKe_Gdrive
from helper.smd import post_audio_to_smd_blob, post_audio_to_smd_file

r = sr.Recognizer()
router = APIRouter(prefix='/bw', tags=['BecomeWaifu-action'])

@router.post('/change-voice/{nama_karakter}')
async def change_voice(nama_karakter: str, bahasa: str, audio_file: UploadFile = File(...), access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    user = cek_data_user(namaORemail=email)
    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='change-voice-bw'), status_code=404)

    premium_check = await check_premium(email=email)
    if premium_check['status'] is False or premium_check['status'] is True and premium_check['keterangan'] != 'bw':
        user_audio_count = await BWResult.filter(user=user).count()
        if user_audio_count >= 10:
            raise HTTPException(detail=error_response(pesan='logaudio your data has reached the limit. Upgrade to a premium plan or remove logaudio', penyebab='audio storage limit with a limit of 10 audio only', action='change-voice-bw', kepada=email), status_code=405)
    
    user_data = await BWResult.filter(user=user).order_by("-ID_number").first()
    if user_data:
        audio_id = user_data.ID_number + 1
    else:
        audio_id = 1
    format_audio: str = audio_file.content_type
    
    if audio_file.content_type not in ['audio/wav', 'audio/x-wav', 'audio/aiff', 'audio/x-aiff', 'audio/flac']:
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio = AudioSegment.from_file(audio_file.file, format=format_audio.split("/", 1)[-1]) 
        audio.export(temp_wav.name, format="wav")
        audio_file = temp_wav
    
    with sr.AudioFile(audio_file.file) as audio_file:
        audio_data = r.record(audio_file)
        
        bahasaYangDigunakan = cek_bahasa(bahasa=bahasa)
        if bahasaYangDigunakan['status'] is False:
            raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=bahasaYangDigunakan['penyebab'], kepada=email, action='change-voice=bw'), status_code=404)
        bahasaYangDigunakan = bahasaYangDigunakan['keterangan']
        
        transcript = r.recognize_google(audio_data, language=bahasaYangDigunakan)
        transcript = ' '.join([kata.capitalize() for kata in transcript.split()])
    
    if premium_check['status'] == True and premium_check['keterangan'] == 'bw' or premium_check['keterangan'] == 'admin':
        translation = translate_target_premium(input=transcript, bahasa_target='jepang')
    else:
        translation = translate_target(input=transcript, bahasa_asal=bahasaYangDigunakan, bahasa_target='ja')
    
    if translation['status'] is False:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=translation['penyebab'], kepada=email, action='change-voice=bw'), status_code=500)
    
    translation = translation['response']
    
    speaker_id = set_karakter_id(nama=nama_karakter)
    if speaker_id is False:
        raise HTTPException(detail=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='change-voice-bw'), status_code=404)
    
    url_audio = request_audio(text=translation, speaker_id=speaker_id)
    if url_audio['status'] is False or url_audio['status'] is None:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=url_audio['penyebab'], kepada=email, action='change-voice-bw'), status_code=500)
    
    audio_data = download_audio(url=url_audio['download_audio'])
    if isinstance(audio_data, str):
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=audio_data, kepada=email, action='change-voice-bw'))

    save_audio = await AudioData.create(user=user, audio_data=audio_data, service='BW')

    url_audio = f'{config.domain}audio_data/stream/BW/{save_audio.UUID_number})?email={email}'

    await BWResult.create(ID_number=audio_id, user=user, transcript=transcript, translation=translation, character=nama_karakter, audio_url=url_audio)
    
    return JSONResponse(content=bw_response(email=email, audio_id=audio_id, transcript=transcript, translation=translation, url_audio=url_audio), status_code=201)

# MOVE TO AUDIO MANAGEMENT
'''
@router.get('/get-audio-data')
async def streamAudio(audio_id: str, access_token: str= Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    data_audio = await logaudio.filter(email=email, audio_id=audio_id).first()
    if not data_audio:
        raise HTTPException(detail=error_response(pesan='The audio you want was not found', penyebab='The audio you want does not exist in the database', kepada=email, action='get-audio-data-bw'), status_code=404)
    
    id_karakter = set_karakter_id(data_audio.karakter)
    if id_karakter is False:
        raise HTTPException(detail=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='get-audio-data-bw'), status_code=404)
    
    data_audio = request_audio(text=data_audio.translate, speaker_id=id_karakter)
    if data_audio['status'] is False or data_audio['status'] is None:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=data_audio['keterangan'], kepada=email, action='get-audio-data-bw'), status_code=500)
    
    return JSONResponse(data_audio, status_code=201)

@router.get('/get-all-audio-data')
async def get_all_logaudio(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    user_data = await logaudio.filter(email=email).all()
    if user_data is None:
        raise HTTPException(detail=error_response(pesan='The audio you want was not found', penyebab='The audio you want does not exist in the database', kepada=email, action='get-all-audio-data-bw'), status_code=404)
    
    result = []
    for logaudio_entry in user_data:
        logaudio_data = bw_response(email=logaudio_entry.email, audio_id=logaudio_entry.audio_id, transcript=logaudio_entry.transcript, translation=logaudio_entry.translate)
        result.append(logaudio_data)
    
    return JSONResponse(result, status_code=200)

@router.delete("/delete-audio-data/{audio_id}")
async def delete_audio(audio_id: int, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    audio_data = await logaudio.filter(email=email, audio_id=audio_id).first()
    if audio_data is None:
        raise HTTPException(detail=error_response(pesan='The audio you want was not found', penyebab='The audio you want does not exist in the database', kepada=email, action='delete-audio-data-bw'), status_code=404)
    
    await audio_data.delete()
    audio_to_update = await logaudio.filter(email=email, audio_id__gt=audio_id).all()
    for audio in audio_to_update:
        audio.audio_id -= 1
        await audio.save()
    
    response = success_response(kepada=audio_data.email, action='delete-audio-data-bw', pesan=f'audio data success to been deleted')
    return JSONResponse(response, status_code=200)
    
@router.post('/save-to-drive-only')
async def saveDrive(audio_id: int, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub') 
    
    user = await userdata.filter(email=email).first()
    if user.googleAuth is False:
        raise HTTPException(detail=error_response(pesan='This feature is not available for you, please first connect your account with Google authentication to the Waifu-Set-On application before accessing this feature', penyebab='your account is not yet connected to google auth', kepada=email, action='save-to-drive-only-bw'), status_code=405)
    
    data = await logaudio.filter(email=email,audio_id=audio_id).first()
    if not data:
        raise HTTPException(detail='data tidak ditemukan', status_code=404)
    
    speaker_id = set_karakter_id(data.karakter)
    
    audio_data = request_audio(text=data.translate, speaker_id=speaker_id)
    if audio_data['status'] is False:
        raise HTTPException(detail=audio_data['keterangan'], status_code=400)
    
    send = await simpanKe_Gdrive(data=data, delete=False, download_audio=audio_data['download_audio'])
    
    if send['status'] is False:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=send['keterangan'], kepada=email, action='save-to-drive-only-bw'), status_code=500)
    
    response = success_response(kepada=email, action='save-to-drive-only', pesan=f'audio-id {audio_id} telah berhasil disimpan ke google drive')
    
    return JSONResponse(response, status_code=201)

@router.post('/save-to-drive-delete')
async def saveDrive(audio_id: int, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub') 
    
    user = await userdata.filter(email=email).first()
    if user is None:
        raise HTTPException(detail=error_response(pesan='user not found please register with the WSO application using your google account to access this endpoint', penyebab='user not found', kepada=email, action='save-to-drive-delete-bw'), status_code=404)
    
    if user.googleAuth is False:
        raise HTTPException(detail=error_response(pesan='This feature is not available for you, please first connect your account with Google authentication to the Waifu-Set-On application before accessing this feature', penyebab='your account is not yet connected to google auth', kepada=email, action='save-to-drive-delete-bw'), status_code=400)
    
    data = await logaudio.filter(email=email,audio_id=audio_id).first()
    if not data:
        raise HTTPException(detail=error_response(pesan='The audio you want was not found', penyebab='The audio you want does not exist in the database', kepada=email, action='save-to-drive-delete-bw'), status_code=404)
    
    speaker_id = set_karakter_id(data.karakter)
    
    audio_data = request_audio(text=data.translate, speaker_id=speaker_id)
    if audio_data['status'] is False:
        raise HTTPException(detail=audio_data['keterangan'], status_code=400)
    
    send = await simpanKe_Gdrive(data=data, delete=True, download_audio=audio_data['download_audio'])
    
    if send['status'] is False:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=send['keterangan'], kepada=email, action='save-to-drive-delete-bw'), status_code=500)
    
    response = success_response(kepada=email, action='save-to-drive-delete-bw', pesan=f'audio-id {audio_id} telah berhasil disimpan ke google drive dan data dihapus dari database')
    
    return JSONResponse(response, status_code=201)


@router.post('/share-to-smd')
async def shareSMD(meta: shareToSMD, access_token: str = Header()):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub') 
    
    data = await logaudio.filter(email=email,audio_id=meta.audio_id).first()
    if not data:
        raise HTTPException(detail='data tidak ditemukan', status_code=404) 
    
    user = await userdata.filter(email=email).first()
    if user.smdAuth is False:
        raise HTTPException(detail='your account is not yet connected to smd auth', status_code=400)
    speaker_id = set_karakter_id(data.karakter)
    
    audio_data = request_audio(text=data.translate, speaker_id=speaker_id)
    if audio_data['status'] is False:
        raise HTTPException(detail=audio_data['keterangan'], status_code=400)
    
    response = post_audio_to_smd_file(user=user, audio_download=audio_data['download_audio'], caption=meta.caption)
    if response['status'] is True:
        pesan = success_response(kepada=email, action='share-to-smd-wso', pesan=response['keterangan'])
        return JSONResponse(content=pesan, status_code=201)
    else:
        raise HTTPException(detail='something wrong', status_code=500)

'''