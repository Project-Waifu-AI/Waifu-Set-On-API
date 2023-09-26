from pydantic import BaseModel
from typing import Optional
from datetime import date

class SetKarakter(BaseModel):
    nama: Optional[str]
    bahasaYangDigunakan: Optional[str]
    kepribadian: Optional[str]
    usia: Optional[int]
    ulang_tahun: Optional[date]