from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import logpercakapan, logpercakapan_gemini
from helper.fitur import obrolan, request_audio, gemini_chatbot
from helper.translate import cek_bahasa, translate_target, translate_target_premium
from helper.response import pesan_response
from body_request.aiu_body_request import obrolan_aiu, Gemini_aiu
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
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    user_data = await logpercakapan.filter(email=email).order_by("-id_percakapan").first()
    if user_data:
        id_percakapan = user_data.id_percakapan + 1
    else:
        id_percakapan = 1  
    
    setkarakter = set_karakter_persona(nama=meta.karakter)
    if setkarakter is False:
        raise HTTPException(detail='karakter tidak ditemukan', status_code=404)
    
    response = await obrolan(input_text=meta.input, email=email, setKarakter=setkarakter)
    if response['status'] is True:
        premium = await check_premium(email=email)
        if premium['status'] == True and premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
            translate = translate_target_premium(input=response['output'], bahasa_target='jepang')
        else:
            translate = translate_target(input=response['output'], bahasa_asal=None, bahasa_target='ja')
        
        if translate['status'] is True:
            speakerId = 14
            data_audio = request_audio(text=translate['response'], speaker_id=speakerId)
            
            if data_audio['status'] is False:
                raise HTTPException(detail=data_audio, status_code=500)
            
            data = [{
                'pesan': meta.input,
                'response': response['output'],
                'translate': translate['response'],
            }]
            
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
        
        else:
            raise HTTPException (detail=translate['response'], status_code=500)
    else:
        raise HTTPException(detail=response['output'], status_code=500)

@router.post('/obrolan-beta')
async def obrolanAIU(meta: obrolan_aiu, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
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
                
    
    bahasa = cek_bahasa(bahasa=meta.bahasa)
    if bahasa['status'] == False:
        raise HTTPException(detail=bahasa['keterangan'], status_code=404)
    
    if meta.bahasa != 'bahasa indonesia':
        if premium == True:
            input_user = translate_target_premium(input=meta.input, bahasa_target='indonesia')
        else:
            input_user = translate_target(input=meta.input, bahasa_asal=bahasa['keterangan'], bahasa_target='id')  
        if input_user['status'] == False:
            raise HTTPException(detail=input_user['response'])
        input_user = input_user['response']
    else:
        input_user = meta.input
        
    jawaban = obrolan_bot(input=input_user, karakter=meta.karakter)
    print (jawaban)
    if jawaban['status'] == False:
        raise HTTPException(detail=jawaban['keterangan'], status_code=404)
    
    if meta.bahasa != '日本語':
        if premium == False:
            translate_response = translate_target(input=jawaban['keterangan'], bahasa_target=bahasa['keterangan'], bahasa_asal='ja')
            print(translate_response)
            if translate_response['status'] == False:
                raise HTTPException(detail=translate_response['response'], status_code=500)
            jawaban_response = translate_response['response']
        else:
            translate_response = translate_target_premium(input=jawaban['keterangan'], bahasa_target=meta.bahasa)
            if translate_response['status'] == False:
                raise HTTPException(detail=translate_response['response'], status_code=500)
            jawaban_response = translate_response['response']
    else:
        jawaban_response = jawaban['keterangan']
    
    jawaban_japan = jawaban['keterangan']   
    
    karakter_id = set_karakter_id(nama=meta.karakter)
    if karakter_id is False:
        raise HTTPException(detail='karakter tidak ditemukan', status_code=404)
    
    data_audio = request_audio(text=jawaban_japan, speaker_id=karakter_id)
    
    if data_audio['status'] is False:
        raise HTTPException(detail=data_audio, status_code=500)
    
    save = logpercakapan(
        id_percakapan=id_percakapan,
        email=email,
        input=meta.input,
        output=jawaban_response,
        translate=jawaban_japan,
        karakter=meta.karakter
        )
    
    await save.save()
    
    response = [
        {
            'pesan': meta.input,
            'response': jawaban_response,
            'translate': jawaban_japan
            
        }
    ]
    response.append(data_audio)
    
    return JSONResponse(response)

@router.delete('/delete-all-log-percakapan')
async def delete_obrolan(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    try:
        data = await logpercakapan.filter(email=email).first()
        await data.delete()
        response = pesan_response(email=data.email, pesan='log obrolan berhasil dihapus')
        return JSONResponse(response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/obrolan-gemini')
async def obrolan_gemini(gemini_aiu: Gemini_aiu, access_token: str = Header(...)):
    try:
        check = check_access_token_expired(access_token=access_token)
        if check:
            return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
        
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        if not email:
            return JSONResponse({"error": "Email tidak tersedia dalam token akses"}, status_code=400)

        user_data = await logpercakapan_gemini.filter(email=email).order_by("-id").first()
        if user_data:
            id_percakapan = user_data.id + 1
        else:
            id_percakapan = 1
        
        history = await logpercakapan_gemini.filter(email=email).order_by("-id").limit(10).all()
        print(f"History for {email}: {history}")

        response = await gemini_chatbot(gemini_aiu.message, history)
        
       
        save = logpercakapan_gemini(
            id=id_percakapan,
            email=email,
            input_text=gemini_aiu.message,
            output_text=response,
            role="user"  
        )
        await save.save()

        data = {
            'pesan': gemini_aiu.message,
            'response': response,
        }
        return JSONResponse(data, status_code=200)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)