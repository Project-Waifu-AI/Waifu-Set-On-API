from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import logpercakapan
from helper.fitur import obrolan_gpt, request_audio
from helper.translate import cek_bahasa, translate_target, translate_target_premium
from helper.response import success_response, error_response, aiu_response
from body_request.aiu_body_request import obrolan_aiu
from helper.aiu.model import obrolan_bot
from helper.cek_and_set import set_karakter_id, set_karakter_persona
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

    user_data = await logpercakapan.filter(email=email).order_by("-id_percakapan").first()
    if user_data:
        id_percakapan = user_data.id_percakapan + 1
    else:
        id_percakapan = 1  
    
    karakter_persona = set_karakter_persona(nama=meta.karakter)
    if karakter_persona is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)
    
    karakter_id = set_karakter_id(nama=meta.karakter)
    if karakter_id is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)

    response = await obrolan_gpt(input_text=meta.input, email=email, setKarakter=karakter_persona)
    if response['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=response['output'], action='obrolan-gpt-aiu'), status_code=500)
    response = response['output']
    
    premium = await check_premium(email=email)
    if premium['status'] == True and premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
        translate = translate_target_premium(input=response, bahasa_target='jepang')
    else:
        translate = translate_target(input=response, bahasa_asal=None, bahasa_target='ja')
    
    if translate['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=translate['response'], action='obrolan-gpt-aiu'), status_code=500)

    translate = translate['response']

    data_audio = request_audio(text=translate, speaker_id=karakter_id)
    if data_audio['status'] is False:
        raise HTTPException(detail=error_response(kepada=email, pesan='something gone wrong', penyebab=data_audio['keterangan'], action='obrolan-gpt-aiu'), status_code=500)
    
    data = [aiu_response(pesan=meta.input, response=response, translate=translate, id_percakapan=id_percakapan, email=email)]
    data.append(data_audio)
    
    save = logpercakapan(
        id_percakapan=id_percakapan,
        email=email,
        input=meta.input,
        output=response['output'],
        translate=translate['response'],
        karakter=meta.karakter
        )
    await save.save()
    
    return JSONResponse (data, status_code=200)
    
@router.post('/obrolan-beta')
async def obrolanAIU(meta: obrolan_aiu, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)

    payloadJWT = decode_access_token(access_token=access_token)
    email = payloadJWT.get('sub')

    bahasa = cek_bahasa(bahasa=meta.bahasa)
    if bahasa['status'] == False:
        raise HTTPException(detail=error_response(pesan='The language you have chosen is still not registered in the WSO application, please enter and select the language that is already registered in the WSO application', penyebab=bahasa['keterangan'], kepada=email, action='obrolan-beta-aiu'), status_code=404)

    karakter_id = set_karakter_id(nama=meta.karakter)
    if karakter_id is False:
        raise HTTPException(detail=error_response(pesan=error_response(pesan='The character you selected was not found, please select another character', penyebab='The character you selected is not in the list', kepada=email, action='obrolan-gpt-aiu')), status_code=404)

    user_data = await logpercakapan.filter(email=email).order_by("-id_percakapan").first()
    if user_data:
        id_percakapan = user_data.id_percakapan + 1
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
            raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=input_user['response'], action='obrolan-beta-aiu', kepada=email), status_code=500)  
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
            
            jawaban_response = translate_response['response']
        
        else:
            translate_response = translate_target_premium(input=jawaban, bahasa_target=meta.bahasa)
            if translate_response['status'] == False:
                raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=translate_response['response'], action='obrolan-beta-aiu', kepada=email), status_code=500)
            
            jawaban_response = translate_response['response']
    else:
        jawaban_response = jawaban
    
    jawaban_japan = jawaban  
    
    data_audio = request_audio(text=jawaban_japan, speaker_id=karakter_id)
    if data_audio['status'] is False:
        raise HTTPException(detail=error_response(pesan='something gone wrong', penyebab=data_audio['keterangan'], action='obrolan-beta-aiu', kepada=email), status_code=500)
    
    save = logpercakapan(
        id_percakapan=id_percakapan,
        email=email,
        input=meta.input,
        output=jawaban_response,
        translate=jawaban_japan,
        karakter=meta.karakter
    )
    await save.save()
    
    response = [aiu_response(pesan=meta.input, response=response, translate=jawaban_japan, id_percakapan=id_percakapan, email=email)]
    response.append(data_audio)
    
    return JSONResponse(response)

@router.delete('/delete-history-percakapan')
async def delete_obrolan(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    try:
        data = await logpercakapan.filter(email=email).first()
        await data.delete()
        return JSONResponse(success_response(kepada=data.email, action='delete-history-percakapan-aiu', pesan='Your conversation history on the AIU feature has been successfully deleted'), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response(pesan='something gone wrong', penyebab=str(e), kepada=email, action='delete-history-percakapan-aiu'))