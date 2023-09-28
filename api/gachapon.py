from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse, RedirectResponse
from numpy.random import choice
from helping.auth_helper import check_access_token_expired
from helping.response_helper import pesan_response
from database.model import KarakterData, userdata
from configs import config

router = APIRouter(prefix='/gacha', tags=['gachapon system'])

@router.get('/gacha-normal-1')
async def gacha_normal1(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check
    email = await userdata.filter(user_id=user_id).first()
    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [0.001] * len(listKarakter)
    
    user = await userdata.filter(user_id=user_id).first()
    if user.NegaiKanjo >= 35:
        user.NegaiKanjo -= 35
        hasil = choice(listKarakter, p=probality)
        response.append(hasil)
        return JSONResponse (response)
    else:
        pesan = pesan_response(email=email.email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        return JSONResponse (pesan)
    
@router.get('gacha-normal-10')
async def gacha_normal10(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check
    email = await userdata.filter(user_id=user_id).first()
    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [0.001] * len(listKarakter)
    
    user = await userdata.filter(user_id=user_id).first()
    if user.NegaiKanjo >= 300:
        for i in range(10):
            hasil = choice(listKarakter, p=probality)
            response.append(hasil)
        return JSONResponse (response)
    else:
        pesan = pesan_response(email=email.email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        return JSONResponse (pesan)
    
@router.get('gacha-banner-meimei-himari-1')
async def banner_meimei_himari1(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check
    email = await userdata.filter(user_id=user_id).first()
    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [0.001] * len(listKarakter)
    MeiMeiHimari_index = listKarakter.index("meimei himari")
    probality[MeiMeiHimari_index] = 0.05
    user = await userdata.filter(user_id=user_id).first()
    if user.NegaiKanjo >= 35:
        user.NegaiKanjo -= 35
        hasil = choice(listKarakter, p=probality)
        response.append(hasil)
        return JSONResponse (response)
    else:
        pesan = pesan_response(email=email.email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        return JSONResponse (pesan)
    
@router.get('gacha-banner-meimei-himari-10')
async def gacha_normal10(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check
    email = await userdata.filter(user_id=user_id).first()
    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [0.001] * len(listKarakter)
    MeiMeiHimari_index = listKarakter.index("meimei himari")
    probality[MeiMeiHimari_index] = 0.05
    user = await userdata.filter(user_id=user_id).first()
    if user.NegaiKanjo >= 300:
        for i in range(10):
            hasil = choice(listKarakter, p=probality)
            response.append(hasil)
        return JSONResponse (response)
    else:
        pesan = pesan_response(email=email.email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        return JSONResponse (pesan)

@router.get('/get-all-karakter-data')
async def getAllKarakter(access_token: str = Header(...)):
    check = await check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        user_id = check
    data = await KarakterData.all()
    response = []
    for karakter in data:
        karakter_dict = {
                'nama': karakter.nama,
                'bahasa_yang_digunakan': karakter.bahasaYangDigunakan,
                'kepribadian': karakter.kepribadian,
                'usia': karakter.usia,
                'ulang_tahun': str(karakter.ulang_tahun),
                'speakerID': karakter.speakerID
            }
        response.append(karakter_dict)
    return JSONResponse(response, status_code=200)