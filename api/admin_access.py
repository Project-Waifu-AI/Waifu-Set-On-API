from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import KarakterData
from helping.auth_helper import check_access_token_expired, check_access_token_level
from helping.response_helper import pesan_response
from body_request.gachapon_body_request import SetKarakter
from configs import config

router = APIRouter(prefix='/admin-access', tags=['admin'])

@router.post('/+karakter')
async def tambah_karakter(meta: SetKarakter, access_token: str = Header(...)):
    check_exp = await check_access_token_expired(access_token=access_token)
    if check_exp is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check_exp is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        check_lvl = await check_access_token_level(access_token=access_token)
        if check_lvl == 'admin':
            save = KarakterData(nama=meta.nama)
            await save.save()
            karakter = await KarakterData.filter(nama=meta.nama).first()
            if meta.bahasaYangDigunakan:
                karakter.bahasaYangDigunakan = meta.bahasaYangDigunakan
            if meta.kepribadian:
                karakter.kepribadian = meta.kepribadian
            if meta.usia:
                karakter.usia = meta.usia
            if meta.ulang_tahun:
                karakter.ulang_tahun = meta.ulang_tahun
            if meta.speakerID:
                karakter.speakerID = meta.speakerID
            await karakter.save()
            return ('karakter berhasil dibuat')
        else:
            return f'user anda {check_lvl}'