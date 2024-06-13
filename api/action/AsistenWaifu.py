from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from database.model import AIUHistory, AudioData

from handler.response.basic import success_response, error_response
from handler.response.fitur import aiu_response
from handler.request.aiu import obrolan_aiu

from helper.fitur import obrolan_gpt, request_audio, download_audio
from helper.translate import cek_bahasa, translate_target, translate_target_premium
from helper.aiu.model import obrolan_bot
from helper.cek_and_set import set_karakter_id, set_karakter_persona, cek_data_user
from helper.access_token import check_access_token_expired, decode_access_token
from helper.premium import check_premium

from configs import config

router = APIRouter(prefix='/aiu', tags=['AsistenWaifu-action'])

@router.post('/obrolan-gpt')
async def pesan_meimei_himari(meta: obrolan_aiu, access_token: str = Header(...)):
    
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    
    payloadJWT = decode_access_token(access_token=access_token)
    email = payloadJWT.get('sub')

    user = cek_data_user(namaORemail=email)
    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='obrolan-gpt-aiu'), status_code=404)
    
    chat_history = await AIUHistory.filter(user=user).order_by("-ID_number").first()
    if chat_history:
        id_percakapan = chat_history.ID_number + 1
    else:
        id_percakapan = 1
    
    karakter_persona = set_karakter_persona(nama=meta.karakter)
    if karakter_persona is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)
    
    karakter_id = set_karakter_id(nama=meta.karakter)
    if karakter_id is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)

    response = await obrolan_gpt(input_text=meta.input, user=user, setKarakter=karakter_persona)
    if response['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=response['penyebab'], action='obrolan-gpt-aiu'), status_code=500)
    response = response['output']
    
    premium = await check_premium(user=user)
    
    if premium['status'] == True and premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
        translate = translate_target_premium(input=response, bahasa_target='jepang')
    
    else:
        translate = translate_target(input=response, bahasa_asal=None, bahasa_target='ja')
    
    if translate['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=translate['penyebab'], action='obrolan-gpt-aiu'), status_code=500)

    translate = translate['response']

    url_audio = request_audio(text=translate, speaker_id=karakter_id)
    if url_audio['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=url_audio['penyebab'], action='obrolan-gpt-aiu'), status_code=500)
    
    audio_data = download_audio(url=url_audio['download_audio'])
    if isinstance(audio_data, str):
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=audio_data, kepada=email, action='obrolan-gpt-aiu'))

    save_audio = await AudioData.create(user=user, japanese_text=translate,audio_data=audio_data, service='AIU')

    url_audio = f'{config.domain}audio_data/stream/AIU/{save_audio.UUID_number})?email={email}'
    
    await AIUHistory.create(
        ID_number=id_percakapan,
        user=user,
        user_input=meta.input,
        display_output=response,
        japanese_output=translate,
        character=meta.karakter,
        audio_url=url_audio,
        service='GPT'
    )
    
    return JSONResponse(aiu_response(pesan=meta.input, display=response, japanese_response=translate, id_percakapan=id_percakapan, email=email, url_audio=url_audio), status_code=201)
    
@router.post('/obrolan-beta')
async def obrolanAIU(meta: obrolan_aiu, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)

    payloadJWT = decode_access_token(access_token=access_token)
    email = payloadJWT.get('sub')

    user = cek_data_user(namaORemail=email)
    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='obrolan-gpt-aiu'), status_code=404)
    
    bahasa = cek_bahasa(bahasa=meta.bahasa)
    if bahasa['status'] == False:
        raise HTTPException(detail=error_response(pesan='The language you have chosen is still not registered in the WSO application, please enter and select the language that is already registered in the WSO application', penyebab=bahasa['keterangan'], kepada=email, action='obrolan-beta-aiu'), status_code=404)

    karakter_id = set_karakter_id(nama=meta.karakter)
    if karakter_id is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)

    user_data = await AIUHistory.filter(user=user).order_by("-UUID_number").first()
    if user_data:
        id_percakapan = user_data.UUID_number + 1
    else:
        id_percakapan = 1
    
    premium = await check_premium(email=email)
    if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
        premium = True
    else:
        premium = False
    
    bahasa = bahasa['keterangan']

    if meta.bahasa != 'bahasa indonesia':
        if premium == True:
            input_user = translate_target_premium(input=meta.input, bahasa_target='indonesia')
        else:
            input_user = translate_target(input=meta.input, bahasa_asal=bahasa, bahasa_target='id')  
        
        if input_user['status'] == False:
            raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=input_user['response'], action='obrolan-gpt-aiu', kepada=email), status_code=500)  
        input_user = input_user['response']
    
    else:
        input_user = meta.input
        
    jawaban = obrolan_bot(input=input_user, karakter=meta.karakter)
    if jawaban['status'] == False:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=jawaban['keterangan'], action='obrolan-beta-aiu', kepada=email), status_code=500)
    
    jawaban = jawaban['keterangan']

    if meta.bahasa != '日本語':
        
        if premium == False:
            translate_response = translate_target(input=jawaban, bahasa_target=bahasa, bahasa_asal='ja')
            if translate_response['status'] == False:
                raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=translate_response['response'], action='obrolan-beta-aiu', kepada=email), status_code=500)
            
            jawaban_display = translate_response['response']
        
        else:
            translate_response = translate_target_premium(input=jawaban, bahasa_target=meta.bahasa)
            if translate_response['status'] == False:
                raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=translate_response['response'], action='obrolan-beta-aiu', kepada=email), status_code=500)
            
            jawaban_display = translate_response['response']
    else:
        jawaban_display = jawaban
    
    jawaban_japan = jawaban  
    
    url_audio = request_audio(text=jawaban_japan, speaker_id=karakter_id)
    if url_audio['status'] is False:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=url_audio['penyebab'], action='obrolan-beta-aiu', kepada=email), status_code=500)
    
    audio_data = download_audio(url=url_audio['download_audio'])
    if isinstance(audio_data, str):
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=audio_data, kepada=email))

    save_audio = await AudioData.create(user=user, japanese_text=jawaban_japan,audio_data=audio_data, service='AIU')

    url_audio = f'{config.domain}audio_data/stream/AIU/{save_audio.UUID_number})?email={email}'

    await AIUHistory.create(
        ID_number=id_percakapan,
        user=user,
        user_input=meta.input,
        display_output=jawaban_display,
        japanese_output=jawaban_japan,
        character=meta.karakter,
        audio_url=url_audio,
        service='BETA'
    )
    
    return JSONResponse(aiu_response(pesan=meta.input, response=jawaban_display, translate=jawaban_japan, id_percakapan=id_percakapan, email=email), status_code=201)

@router.delete('/delete-all-history-percakapan')
async def delete_obrolan(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    user = cek_data_user(namaORemail=email)
    if user is False:
        raise HTTPException(detail=error_response(pesan='Sorry the user is not found, please register first to the WSO application with the authentication registered in the WSO application.', penyebab='user not found in database', action='obrolan-gpt-aiu'), status_code=404)

    await user.aiu_history.all().delete()

    return JSONResponse(success_response(kepada=email, action='delete-history-percakapan-aiu', pesan='Your conversation history on the AIU feature has been successfully deleted'), status_code=200)