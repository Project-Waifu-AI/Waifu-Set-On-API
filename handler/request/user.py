from pydantic import BaseModel
from typing import Optional
from datetime import date

class updateUser(BaseModel):
    nama: Optional[str]
    gender: Optional[str]
    ulang_tahun: Optional[date]

class updatePassword(BaseModel):
    password: Optional[str]
    konfirmasi_password: Optional[str]

class updatePassword(BaseModel):
    password: Optional[str]
    konfirmasi_password: Optional[str]