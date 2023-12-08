from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import logpercakapan, userdata
from helper.fitur import obrolan, request_audio
from helper.translate import to_japan, to_japan_premium
from helper.response import pesan_response
from helper.access_token import check_access_token_expired, decode_access_token
from helper.premium import check_premium
from configs import config

router = APIRouter(prefix='/aiu', tags=['AsistenWaifu-action'])

@router.get('/pesan-meimei-himari')
async def pesan_meimei_himari(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah meimei himari,penuai dari dunia bawah,memiliki mata untuk hal-hal yang indah,umur 18 tahun,ras reaper,tanggal lahir 1 september,hal paling disukai anak perempuan yang lucu,kepribadian baik hati dan rapi, jawab singkat'
    }
    
    response = await obrolan(input_text=pesan, email=email, setKarakter=setkarakter)
    if response['status'] is True:
        premium = await check_premium(email=email)
        if premium['status'] is False:
            translate = to_japan(input=response['output'])
        else:
            if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
                translate = to_japan_premium(input=response['output'])
            else:
                translate = to_japan(input=response['output'])
        
        if translate['status'] is True:
            speakerId = 14
            data_audio = request_audio(text=translate['response'], speaker_id=speakerId)
            
            if data_audio['status'] is False:
                raise HTTPException(detail=data_audio, status_code=500)
            
            data = [{
                'pesan': pesan,
                'response': response['output'],
                'translate': translate['response'],
            }]
            
            data.append(data_audio)
            save = logpercakapan(id_percakapan=id_percakapan, email=email, input=pesan, output=response['output'], translate=translate['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
            await save.save()
            return JSONResponse (data, status_code=200)
        
        else:
            raise HTTPException (detail=translate['response'], status_code=500)
    else:
        raise HTTPException(detail=response['output'], status_code=500)

@router.get('/pesan-nurseT')
async def pesan_nurse_t(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah nurse-T,Robot berbentuk perawat yang dibuat oleh seorang dokter,Kepribadian ditetapkan sebagai seorang gadis,umur 5 bulan,tanggal lahir 3 desember,tinggi badan 150 - 160 cm, nama panggilan TT, produsen Robot soba kecil(dokter), jawab singkat'
    }
    
    response = await obrolan(input_text=pesan, email=email, setKarakter=setkarakter)
    if response['status'] is True:
        premium = await check_premium(email=email)
        if premium['status'] is False:
            translate = to_japan(input=response['output'])
        else:
            if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
                translate = to_japan_premium(input=response['output'])
            else:
                translate = to_japan(input=response['output'])

        if translate['status'] is True:
            speakerId = 47
            data_audio = request_audio(text=translate['response'], speaker_id=speakerId)
            
            if data_audio['status'] is False:
                raise HTTPException(detail=data_audio, status_code=500)
            
            data = [{
                'pesan': pesan,
                'response': response['output'],
                'translate': translate['response'],
            }]
            data.append(data_audio)
            save = logpercakapan(id_percakapan=id_percakapan, email=email, input=pesan, output=response['output'], translate=translate['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
            await save.save()
            return JSONResponse (data, status_code=200)
        else:
            raise HTTPException(detail=translate, status_code=500)
    else:
        raise HTTPException(detail=response['output'], status_code=500)

@router.get('/pesan-kusukabe-tsumugi')
async def pesan_kusukabe_tsumugi(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah kusukabe tsumugi,gadis manusia yang bersekolah di sekolah menengah atas di Prefektur Saitama,Kepribadian terlihat nakal tetapi sebenarnya memiliki sisi yang serius,umur 18 tahun,tinggi badan 155 cm, hobi mengunjungi situs web streaming video,makanan favorit kari jepang, tempat lahir saitama jepang, jawab singkat'
    }
    
    response = await obrolan(input_text=pesan, email=email, setKarakter=setkarakter)
    if response['status'] is True:
        premium = await check_premium(email=email)
        if premium['status'] is False:
            translate = to_japan(input=response['output'])
        else:
            if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
                translate = to_japan_premium(input=response['output'])
            else:
                translate = to_japan(input=response['output'])

        if translate['status'] is True:
            speakerId = 8
            data_audio = request_audio(text=translate['response'], speaker_id=speakerId)
            
            if data_audio['status'] is False:
                raise HTTPException(detail=data_audio, status_code=500)
            
            data = [{
                'pesan': pesan,
                'response': response['output'],
                'translate': translate['response'],
            }]
            data.append(data_audio)
            save = logpercakapan(id_percakapan=id_percakapan, email=email, input=pesan, output=response['output'], translate=translate['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
            await save.save()
            return JSONResponse (data, status_code=200)
        else:
            raise HTTPException(detail=translate['response'], status_code=500)
    else:
        raise HTTPException(detail=response['output'], status_code=500)

@router.get('/pesan-no7')
async def pesan_no7(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah NO.7,Seorang wanita misterius yang identitasnya sulit dipahami,Kepribadian Minimalis, hanya menggunakan lilin untuk penerangan di kamarnya,umur 23 tahun,tinggi badan 165 cm, suka anak-anak,hobi Membudidayakan lobak daikon, jawab singkat'
    }
    
    response = await obrolan(input_text=pesan, email=email, setKarakter=setkarakter)
    
    if response['status'] is True:
        premium = await check_premium(email=email)
        if premium['status'] is False:
            translate = to_japan(input=response['output'])
        else:
            if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
                translate = to_japan_premium(input=response['output'])
            else:
                translate = to_japan(input=response['output'])

        if translate['status'] is True:
            speakerId = 29
            data_audio = request_audio(text=translate['response'], speaker_id=speakerId)
            
            if data_audio['status'] is False:
                raise HTTPException(detail=data_audio, status_code=500)
            
            data = [{
                'pesan': pesan,
                'response': response['output'],
                'translate': translate['response'],
            }]
            data.append(data_audio)
            save = logpercakapan(id_percakapan=id_percakapan, email=email, input=pesan, output=response['output'], translate=translate['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
            await save.save()
            return JSONResponse (data, status_code=200)
        else:
            raise HTTPException(detail=translate['response'], status_code=500)
    else:
        raise HTTPException(detail=response['output'], status_code=500)

@router.get('/pesan-sayo')
async def pesan_sayo(pesan: str, access_token: str = Header(...)):
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
    
    setkarakter = {
        'role':'system',
        'content':'namamu adalah SAYO,Gadis kucing yang banyak bicara,Kepribadian Minimalis,tinggi badan 135 cm (termasuk telinga kucin),makanan favorit makanan faforit makanan kaleng, jawab singkat'
    }
    
    response = await obrolan(input_text=pesan, email=email, setKarakter=setkarakter)
    
    if response['status'] is True:
        premium = await check_premium(email=email)
        if premium['status'] is False:
            translate = to_japan(input=response['output'])
        else:
            if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
                translate = to_japan_premium(input=response['output'])
            else:
                translate = to_japan(input=response['output'])

        if translate['status'] is True:
            speakerId = 46
            data_audio = request_audio(text=translate, speaker_id=speakerId)
            
            if data_audio['status'] is False:
                raise HTTPException(detail=data_audio, status_code=500)
            
            data = [{
                'pesan': pesan,
                'response': response['output'] ,
                'translate': translate['response'],
            }]
            data.append(data_audio)
            save = logpercakapan(id_percakapan=id_percakapan, email=email, input=pesan, output=response['output'], translate=translate['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
            await save.save()
            return JSONResponse (data, status_code=200)
        else:
            raise HTTPException(detail=translate['response'], status_code=500)
    else:
        raise HTTPException(detail=response['output'], status_code=500)

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