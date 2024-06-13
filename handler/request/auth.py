from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoginWSO(BaseModel):
    emailORname: Optional[str]
    password: Optional[str]

class SimpanUserWSO(BaseModel):
    email: Optional[str]
    password: Optional[str]
    konfirmasi_password: Optional[str]
    token: Optional[str]
    
class smd_login(BaseModel):
    username: Optional[str]
    password: Optional[str]

class smd_register(BaseModel):
    username: Optional[str]
    email: Optional[str]
    displayName: Optional[str]
    password: Optional[str]