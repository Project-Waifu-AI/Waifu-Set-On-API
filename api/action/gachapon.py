from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from numpy.random import choice
from helper.access_token import check_access_token_expired, decode_access_token
from handler.response.response import pesan_response, karakter_response
from database.model import KarakterData, userdata
from configs import config

router = APIRouter(prefix='/gacha', tags=['gachapon system'])

@router.get('/gacha-normal-1')
async def gacha_normal1(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [1 / len(listKarakter) * len(listKarakter)]
    
    user = await userdata.filter(email=email).first()
    if user.AtsumaroKanjo >= 35:
        user.AtsumaroKanjo -= 35
        hasil = choice(listKarakter, p=probality)
        response.append(hasil)
        
        if user.karakterYangDimiliki is not None:
            user.karakterYangDimiliki += response
        else:
            user.karakterYangDimiliki = response
        await user.save()
        
        return JSONResponse (user.karakterYangDimiliki, status_code=200)
    else:
        pesan = pesan_response(email=email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        raise HTTPException (detail=HTTPException, status_code=403)
    
@router.get('gacha-normal-10')
async def gacha_normal10(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [1 / len(listKarakter) * len(listKarakter)]
    
    user = await userdata.filter(email=email).first()
    if user.AtsumaruKanjo >= 300:
        user.AtsumaruKanjo -= 300
        for i in range(10):
            hasil = choice(listKarakter, p=probality)
            response.append(hasil)
        
        if user.karakterYangDimiliki is not None:
            user.karakterYangDimiliki += response
        else:
            user.karakterYangDimiliki = response
        await user.save()
        
        return JSONResponse (user.karakterYangDimiliki, status_code=200)
    else:
        pesan = pesan_response(email=email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        raise HTTPException (detail=pesan, status_code=403)
    
@router.get('gacha-banner-meimei-himari-1')
async def banner_meimei_himari1(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [1 / len(listKarakter) * len(listKarakter)]
    MeiMeiHimari_index = listKarakter.index("meimei himari")
    probality[MeiMeiHimari_index] += 0.05
    user = await userdata.filter(email=email).first()
    if user.NegaiGoto >= 35:
        user.NegaiGoto -= 35
        hasil = choice(listKarakter, p=probality)
        response.append(hasil)
        
        if user.karakterYangDimiliki is not None:
            user.karakterYangDimiliki += response
        else:
            user.karakterYangDimiliki = response
        await user.save()
        
        return JSONResponse (user.karakterYangDimiliki, status_code=200)
    else:
        pesan = pesan_response(email=email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        raise HTTPException (detail=pesan, status_code=403)
    
@router.get('gacha-banner-meimei-himari-10')
async def gacha_normal10(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')

    karakter = await KarakterData.all()
    response = []
    listKarakter = [karakter.nama for karakter in karakter]
    probality = [0.001] * len(listKarakter)
    MeiMeiHimari_index = listKarakter.index("meimei himari")
    probality[MeiMeiHimari_index] += 0.05
    user = await userdata.filter(email).first()
    if user.NegaiGoto >= 300:
        user.NegaiGoto -= 300
        for i in range(10):
            hasil = choice(listKarakter, p=probality)
            response.append(hasil)
        
        if user.karakterYangDimiliki is not None:
            user.karakterYangDimiliki += response
        else:
            user.karakterYangDimiliki = response
        await user.save()
        
        return JSONResponse (user.karakterYangDimiliki, status_code=200)
    else:
        pesan = pesan_response(email=email, pesan= f'jumlah NK anda sekarang adalah {user.NegaiKanjo}, NK anda tidak mencukupi')
        raise HTTPException (detail=pesan, status_code=403)

@router.get('/get-all-karakter-data')
async def getAllKarakter(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    
    data = await KarakterData.all()
    response = []
    for karakter in data:
        karakter_dict =karakter_response(karakter=karakter)
        response.append(karakter_dict)
    return JSONResponse(response, status_code=200)

@router.get('/get-spesifik-data-karakter')
async def getSpesifikKarakter(nama: str, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)

    else:
        karakter = await KarakterData.filter(nama=nama).first()
        if karakter:
            karakter_data = karakter_response(karakter=karakter)
            return JSONResponse(karakter_data)
        else:
            raise HTTPException(detail='karakter tidak ditemukan', status_code=404)