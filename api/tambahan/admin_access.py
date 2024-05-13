from fastapi import APIRouter, Header, Response, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from database.model import KarakterData
from helper.access_token import check_access_token_expired, decode_access_token
from body_request.gachapon_body_request import SetKarakter, tambahan
from configs import config
import json

router = APIRouter(prefix='/admin', tags=['admin'])
#perlu diubah(dalam proses)
@router.post('/tambah-karakter')
async def tambah_karakter(meta: SetKarakter, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        level = payloadJWT.get('level')
        if level == 'admin':
            # Convert the character name to lowercase for case-insensitive comparison
            lowercase_nama = meta.nama.lower()
            # Query the database for characters with the same lowercase name
            cek_karakter = await KarakterData.filter(nama__iexact=lowercase_nama).first()
            if not cek_karakter:
                save = KarakterData(
                    nama=meta.nama, 
                    rarity=meta.rarity,
                    is_limited=meta.is_limited
                )
                await save.save()
                karakter = await KarakterData.filter(nama__iexact=lowercase_nama).first()
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
            raise HTTPException(status_code=403, detail=f'user anda {level}')
        
@router.put('/update-karakter')
async def update_karakter(meta: SetKarakter, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        level = payloadJWT.get('level')
        if level == 'admin':
            karakter = await KarakterData.filter(nama=meta.nama).first()
            if karakter:
                data_tambahan = tambahan(**meta.dict(exclude_unset=True))
                data_dict = data_tambahan.dict()
                if data_dict["ulang_tahun"] is not None:
                    data_dict["ulang_tahun"] = data_dict["ulang_tahun"].isoformat()
                if data_tambahan.__dict__:
                    karakter.informasi_tambahan = json.dumps(data_dict)            
                karakter.rarity = meta.rarity
                karakter.is_limited = meta.is_limited
                await karakter.save()
                return Response(status_code=200, content=f'informasi mengenai karakter {meta.nama} berhasil diupdate')
            else:
                raise HTTPException(detail=f'karakter dengan {meta.nama} tidak ditemukan', status_code=404)
        else:
            raise HTTPException(status_code=403, detail=f'user anda {level}')
                        
@router.delete('/delete-karakter')
async def delete_karakter(nama_karakter: str, access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        level = payloadJWT.get('level')
        if level == 'admin':
            karakter = await KarakterData.filter(nama=nama_karakter).first()
            if karakter:
                await karakter.delete()
                return Response(f'karakter {nama_karakter} telah dihapus', status_code=200)
            else:
                raise HTTPException(detail=f'karakter dengan {nama_karakter} tidak ditemukan', status_code=404)
        else:
            raise HTTPException(status_code=403, detail=f'user anda {level}')