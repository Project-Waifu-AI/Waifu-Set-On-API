from database.model import userdata, token_google
from configs import config
import random
import bcrypt
import re

def cek_password(password: str, user):
    bytes = password.encode('utf-8')
    password_data = user.password
    result = bcrypt.checkpw(bytes, password_data)
    return result

def set_password(password: str):
    salt = bcrypt.gensalt()
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    return hash
    
def cek_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False
    
async def cek_namaku_ada(nama:str):
    user = await userdata.filter(nama=nama).first()
    if user:
        return False
    else:
        return True
    
async def set_name_unik(nama:str):
    while True:
        random_suffix = random.randint(1, 9999)
        new_name = f"{nama}#{random_suffix}"
        user = await userdata.filter(nama=new_name).first()
        if user is None:
            return new_name
        
async def cek_data_user(namaORemail: str):
    nama = await userdata.filter(nama=namaORemail).first()
    if nama:
        return nama
    else:
        email = await userdata.filter(email=namaORemail).first()
        if email:
            return email
        else:
            return False

def cek_valid_password(password: str):
    if len(password) < 8:
        return False
    
    if not (re.search("[a-z]", password) and
            re.search("[A-Z]", password) and
            re.search("[0-9]", password)):
            return False
    
    return True

def cek_admin(email: str):
    if email in config.admin.split(','):
        return True
    else:
        return False
    
def cek_kalimat_promting(kalimat):
    forbiden = [
    'realistic',
    'real',
    'real person',
    'asli',
    ]


    kata_ditemukan = [kata for kata in forbiden if kata.lower() in kalimat.lower()]
    
    if kata_ditemukan:
        return True
    else:
        return False

def cek_and_set_ukuran_delusion(ukuran: str):
    if ukuran == 'persegi-sama-sisi': 
        ukuran_hitung = '1024x1024'
    elif ukuran == 'persegi-panjang-horizontal':
        ukuran_hitung = '1024x1792'
    elif ukuran == 'persegi-panjang-vertikal':
        ukuran_hitung = '1792x1024'
    else:
        return False
    return ukuran_hitung