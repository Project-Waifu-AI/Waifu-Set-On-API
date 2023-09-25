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

class login(BaseModel):
    email: Optional[str]
    password: Optional[str]

class simpan_user(BaseModel):
    email: Optional[str]
    password: Optional[str]
    konfirmasi_password: Optional[str]
    token: Optional[str]