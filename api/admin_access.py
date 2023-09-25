from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse
from database.model import KarakterData
from body import SetKarakter

router = APIRouter(prefix='/admin-access', tags=['admin'])

@router.get('/+karakter')
async def tambah_karakter(data: SetKarakter, password: str = Header(...)):
    save = KarakterData(nama=data.nama, kepribadian=data.kepribadian, usia=data.usia, ulang_tahun=data.ulang_tahun)
    await save.save()
    
@router.get('/ge-all-data-karakter')
async def getAllDataKarakter(password: str = Header(...)):
    karakter = await KarakterData.all()

@router.put('/EditKarakter')
async def edit_karakter(data: SetKarakter, password: str = Header(...)):
    karakter = await KarakterData.filter(nama=data.nama).first()
    if karakter:
        if data.nama:
            karakter.nama = data.nama
        if data.kepribadian:
            karakter.kepribadian = data.kepribadian
        if data.usia:
            karakter.usia = data.usia
        if data.ulang_tahun:
            karakter.ulang_tahun = data.ulang_tahun
            
        karakter.save()
        return JSONResponse(
            {
                'pesan': 'data telah diperbarui'
            }
        )
    else:
        raise HTTPException(detail='karakter tidak ditemukan', status_code=404)
    
@router.delete('/delete-karakter')
async def deleteKarakter(nama: str, password: str = Header(...)):
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