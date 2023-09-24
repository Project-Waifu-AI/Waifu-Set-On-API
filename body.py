from pydantic import BaseModel
from typing import Optional
from datetime import date

class update(BaseModel):
    nama: Optional[str]
    gender: Optional[str]
    ulang_tahun: Optional[date]
    
class SetKarakter(BaseModel):
    nama: Optional[str]
    kepribadian: Optional[str]
    usia: Optional[int]
    ulang_tahun: Optional[date]