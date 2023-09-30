from fastapi import APIRouter, Header, Response, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import KarakterData
from helping.auth_helper import check_access_token_expired, check_access_token_level
from body_request.gachapon_body_request import SetKarakter, tambahan
from configs import config
import json

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
            cek_karakter = await KarakterData(nama=meta.nama).first()
            if not cek_karakter:
                list = [int(angka) for angka in meta.speakerID.split(',')]
                save = KarakterData(nama=meta.nama, bahasaYangDigunakan=meta.bahasaYangDigunakan, speakerID = json.dumps(list))
                await save.save()
                karakter = await KarakterData.filter(nama=meta.nama).first()
                if meta:
                    data_tambahan = tambahan(**meta.dict(exclude_unset=True))
                    data_dict = data_tambahan.dict()
                    if data_dict["ulang_tahun"] is not None:
                        data_dict["ulang_tahun"] = data_dict["ulang_tahun"].isoformat()
                    if data_tambahan.__dict__:
                        karakter.informasi_tambahan = json.dumps(data_dict)            
                    await karakter.save()
                return Response(status_code=201, content=f'karakter {meta.nama} berhasil dibuat')
            else:
                raise HTTPException(status_code=400, detail=f'karakter dengan nama {meta.nama}, sudah pernah dibuat')
        else:
            raise HTTPException(status_code=403, detail=f'user anda {check_lvl}')
        
@router.put('/update-data-karakter')
async def update_karakter(meta: SetKarakter, access_token: str = Header(...)):
    check_exp = await check_access_token_expired(access_token=access_token)
    if check_exp is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check_exp is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        check_lvl = await check_access_token_level(access_token=access_token)
        if check_lvl == 'admin':
            karakter = await KarakterData.filter(nama=meta.nama).first()
            if karakter:
                data_tambahan = tambahan(**meta.dict(exclude_unset=True))
                data_dict = data_tambahan.dict()
                if data_dict["ulang_tahun"] is not None:
                    data_dict["ulang_tahun"] = data_dict["ulang_tahun"].isoformat()
                if data_tambahan.__dict__:
                    karakter.informasi_tambahan = json.dumps(data_dict)            
                if meta.bahasaYangDigunakan:
                    karakter.bahasaYangDigunakan = meta.bahasaYangDigunakan
                if meta.speakerID:
                    karakter.speakerID = meta.speakerID
                await karakter.save()
                return Response(status_code=200, content=f'informasi mengenai karakter {meta.nama} berhasil diupdate')
            else:
                raise HTTPException(detail=f'karakter dengan {meta.nama} tidak ditemukan', status_code=404)
        else:
            raise HTTPException(status_code=403, detail=f'user anda {check_lvl}')
                        
@router.delete('/delete-karakter-data')
async def delete_karakter(nama_karakter: str, access_token: str = Header(...)):
    check_exp = await check_access_token_expired(access_token=access_token)
    if check_exp is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check_exp is False:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    else:
        check_lvl = await check_access_token_level(access_token=access_token)
        if check_lvl == 'admin':
            karakter = await KarakterData.filter(nama=nama_karakter).first()
            if karakter:
                await karakter.delete()
                return Response(f'karakter {nama_karakter} telah dihapus', status_code=200)
            else:
                raise HTTPException(detail=f'karakter dengan {nama_karakter} tidak ditemukan', status_code=404)
        else:
            raise HTTPException(status_code=403, detail=f'user anda {check_lvl}')