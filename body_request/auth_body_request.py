from pydantic import BaseModel
from typing import Optional
from datetime import date

class updateUser(BaseModel):
    nama: Optional[str]
    gender: Optional[str]
    ulang_tahun: Optional[date]

class LoginWSO(BaseModel):
    emailORname: Optional[str]
    password: Optional[str]

class SimpanUserWSO(BaseModel):
    email: Optional[str]
    password: Optional[str]
    konfirmasi_password: Optional[str]
    token: Optional[str]

class updatePassword(BaseModel):
    password: Optional[str]
    konfirmasi_password: Optional[str]