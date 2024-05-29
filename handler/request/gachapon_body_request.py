from pydantic import BaseModel
from typing import Optional
from datetime import date

class SetKarakter(BaseModel):
    nama: Optional[str]
    variant: Optional[str]
    rarity: Optional[int]
    desc:Optional[str]

class tambahan(BaseModel):
    nama_panggilan: Optional[str]
    deskripsi: Optional[str]
    ras: Optional[str]
    kepribadian: Optional[str]
    kesukaan: Optional[str]
    makanan_kesukaan: Optional[str]
    hobi: Optional[str]
    tinggi_badan: Optional[str]
    berat_badan: Optional[str]
    produsen: Optional[str]
    tempat_lahir: Optional[str]
    titik_pesona: Optional[str]
    usia: Optional[int]
    ulang_tahun: Optional[date]