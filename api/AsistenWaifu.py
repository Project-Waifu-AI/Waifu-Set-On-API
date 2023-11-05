from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import logpercakapan, userdata
from helping.action_helper import obrolan, to_japan, request_audio, to_japan_premium
from helping.response_helper import pesan_response
from helping.auth_helper import check_access_token_expired, decode_access_token, check_premium_AI_U
from configs import config

router = APIRouter(prefix='/AsistenWaifu', tags=['AsistenWaifu-action'])

@router.get('/pesan-meimei-himari')
async def pesan_meimei_himari(pesan: str, access_token: str = Header(...)):
    
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah meimei himari,penuai dari dunia bawah,memiliki mata untuk hal-hal yang indah,umur 18 tahun,ras reaper,tanggal lahir 1 september,hal paling disukai anak perempuan yang lucu,kepribadian baik hati dan rapi'
    }
    
    response = await obrolan(input_text=pesan, userid=user_id, setKarakter=setkarakter)
    user = await userdata.filter(user_id=user_id).first()
    premium = check_premium_AI_U(user=user)
    if premium is False:
        translate = to_japan(input=response)
    elif premium is False:
        translate = to_japan_premium(input=response)
    else:
        translate = to_japan(input=response)

    speakerId = 14
    data_audio = request_audio(text=translate, speaker_id=speakerId)
    data = [{
        'pesan': pesan,
        'response': response,
        'translate': translate,
    }]
    data.append(data_audio)
    save = logpercakapan(id_percakapan=id_percakapan, user_id=user_id, input=pesan, output=response, translate=translate, audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
    await save.save()
    return JSONResponse (data, status_code=200)

@router.get('/pesan-nurse-T')
async def pesan_nurse_t(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah nurse-T,Robot berbentuk perawat yang dibuat oleh seorang dokter,Kepribadian ditetapkan sebagai seorang gadis,umur 5 bulan,tanggal lahir 3 desember,tinggi badan 150 - 160 cm, nama panggilan TT, produsen Robot soba kecil(dokter)'
    }
    
    response = await obrolan(input_text=pesan, userid=user_id, setKarakter=setkarakter)
    user = await userdata.filter(user_id=user_id).first()
    premium = check_premium_AI_U(user=user)
    if premium is False:
        translate = to_japan(input=response)
    elif premium is False:
        translate = to_japan_premium(input=response)
    else:
        translate = to_japan(input=response)

    speakerId = 47
    data_audio = request_audio(text=translate, speaker_id=speakerId)
    data = [{
        'pesan': pesan,
        'response': response,
        'translate': translate,
    }]
    data.append(data_audio)
    save = logpercakapan(id_percakapan=id_percakapan, user_id=user_id, input=pesan, output=response, translate=translate, audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
    await save.save()
    return JSONResponse (data, status_code=200)

@router.get('/pesan-kusukabe-tsumugi')
async def pesan_kusukabe_tsumugi(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah kusukabe tsumugi,gadis manusia yang bersekolah di sekolah menengah atas di Prefektur Saitama,Kepribadian terlihat nakal tetapi sebenarnya memiliki sisi yang serius,umur 18 tahun,tinggi badan 155 cm, hobi mengunjungi situs web streaming video,makanan favorit kari jepang, tempat lahir saitama jepang'
    }
    
    response = await obrolan(input_text=pesan, userid=user_id, setKarakter=setkarakter)
    user = await userdata.filter(user_id=user_id).first()
    premium = check_premium_AI_U(user=user)
    if premium is False:
        translate = to_japan(input=response)
    elif premium is False:
        translate = to_japan_premium(input=response)
    else:
        translate = to_japan(input=response)
    
    speakerId = 8
    data_audio = request_audio(text=translate, speaker_id=speakerId)
    data = [{
        'pesan': pesan,
        'response': response,
        'translate': translate,
    }]
    data.append(data_audio)
    save = logpercakapan(id_percakapan=id_percakapan, user_id=user_id, input=pesan, output=response, translate=translate, audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
    await save.save()
    return JSONResponse (data, status_code=200)

@router.get('/pesan-no.7')
async def pesan_no7(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah NO.7,Seorang wanita misterius yang identitasnya sulit dipahami,Kepribadian Minimalis, hanya menggunakan lilin untuk penerangan di kamarnya,umur 23 tahun,tinggi badan 165 cm, suka anak-anak,hobi Membudidayakan lobak daikon'
    }
    
    response = await obrolan(input_text=pesan, userid=user_id, setKarakter=setkarakter)
    user = await userdata.filter(user_id=user_id).first()
    premium = check_premium_AI_U(user=user)
    if premium is False:
        translate = to_japan(input=response)
    elif premium is False:
        translate = to_japan_premium(input=response)
    else:
        translate = to_japan(input=response)

    speakerId = 29
    data_audio = request_audio(text=translate, speaker_id=speakerId)
    data = [{
        'pesan': pesan,
        'response': response,
        'translate': translate,
    }]
    data.append(data_audio)
    save = logpercakapan(id_percakapan=id_percakapan, user_id=user_id, input=pesan, output=response, translate=translate, audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
    await save.save()
    return JSONResponse (data, status_code=200)

@router.get('/pesan-SAYO')
async def pesan_sayo(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah SAYO,Gadis kucing yang banyak bicara,Kepribadian Minimalis,tinggi badan 135 cm (termasuk telinga kucin),makanan favorit makanan faforit makanan kaleng'
    }
    
    response = await obrolan(input_text=pesan, userid=user_id, setKarakter=setkarakter)
    user = await userdata.filter(user_id=user_id).first()
    premium = check_premium_AI_U(user=user)
    if premium is False:
        translate = to_japan(input=response)
    elif premium is False:
        translate = to_japan_premium(input=response)
    else:
        translate = to_japan(input=response)

    speakerId = 46
    data_audio = request_audio(text=translate, speaker_id=speakerId)
    data = [{
        'pesan': pesan,
        'response': response,
        'translate': translate,
    }]
    data.append(data_audio)
    save = logpercakapan(id_percakapan=id_percakapan, user_id=user_id, input=pesan, output=response, translate=translate, audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
    await save.save()
    return JSONResponse (data, status_code=200)

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