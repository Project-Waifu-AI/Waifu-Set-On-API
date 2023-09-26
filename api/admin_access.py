from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import KarakterData
from helping.auth_helper import check_access_token_expired, check_access_token_level
from helping.response_helper import pesan_response
from body_request.gachapon_body_request import SetKarakter
from configs import config

router = APIRouter(prefix='/admin-access', tags=['admin'])

@router.post('/+karakter')
async def tambah_karakter(data: SetKarakter, access_token: str = Header(...)):
    check_expired = await check_access_token_expired(access_token=access_token)
    check_level = await check_access_token_level(access_token=access_token)
    if check_expired is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check_expired is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        if check_level is True:        
            pass    
        elif check_level is False:
            return JSONResponse(
                {
                    'pesan':'anda bukanlah admin'
                },
                status_code=403
            )
        else:
            return JSONResponse(
                {
                    'pesan':check_level
                },
                status_code=403
            )
        
        try:
            save = KarakterData(nama=data.nama, bahasaYangDigunakan=data.bahasaYangDigunakan, kepribadian=data.kepribadian, usia=data.usia, ulang_tahun=data.ulang_tahun)
            await save.save()
            return JSONResponse(
                {
                    'pesan':'karakter berhasil dibuat'
                }
            )
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

@router.put('/EditKarakter')
async def edit_karakter(meta: SetKarakter, access_token: str = Header(...)):
    check_expired = await check_access_token_expired(access_token=access_token)
    check_level = await check_access_token_level(access_token=access_token)
    if check_expired is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check_expired is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        if check_level is True:        
            pass    
        elif check_level is False:
            return JSONResponse(
                {
                    'pesan':'anda bukanlah admin'
                },
                status_code=403
            )
        else:
            return JSONResponse(
                {
                    'pesan':check_level
                }
            )
        
        try:
            karakter = await KarakterData.filter(nama=meta.nama).first()
            if karakter:
                if meta.nama:
                    karakter.nama = meta.nama
                if meta.bahasaYangDigunakan:
                    karakter.bahasaYangDigunakan = meta.bahasaYangDigunakan
                if meta.kepribadian:
                    karakter.kepribadian = meta.kepribadian
                if meta.usia:
                    karakter.usia = meta.usia
                if meta.ulang_tahun:
                    karakter.ulang_tahun = meta.ulang_tahun
                        
                karakter.save()
                return JSONResponse(
                    {
                        'pesan': 'data karakter telah diperbarui'
                    }
                )
            else:
                raise HTTPException(detail='karakter tidak ditemukan', status_code=404)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
    
@router.delete('/delete-karakter')
async def deleteKarakter(nama: str, access_token: str = Header(...)):
    check_expired = await check_access_token_expired(access_token=access_token)
    check_level = await check_access_token_level(access_token=access_token)
    if check_expired is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check_expired is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        if check_level is True:        
            pass    
        elif check_level is False:
            return JSONResponse(
                {
                    'pesan':'anda bukanlah admin'
                },
                status_code=403
            )
        else:
            return JSONResponse(
                {
                    'pesan':check_level
                }
            )
        
        try:
            karakter = await KarakterData.filter(nama=nama).first()
            if karakter:
                karakter.delete()
                return JSONResponse(
                    {
                        'pesan': f'data mengenai karakter {nama} telah dipahapus'
                    }
                )
            else:
                raise HTTPException(detail='karakter tidak ditemukan', status_code=404)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)