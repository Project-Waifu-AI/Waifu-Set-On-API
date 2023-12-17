from database.model import userdata
from database.model import logdelusion
from configs import config
import requests
import tempfile
import base64
import random
import bcrypt
import re
import os

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

async def set_response_save_delusion(jumlah, data, first_id, email, input, ukuran):
    
    delusion_id = first_id - 1

    url_index = -1
    
    data_response = []
    
    for _ in range(jumlah):
        delusion_id += 1
        url_index += 1

        try:
            get_images = requests.get(url=data[url_index]['keterangan'])
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(get_images.content)
            images = open(temp_file.name, 'rb').read()
            images = base64.b64encode(images)    
            save = logdelusion(
                delusion_id=delusion_id,
                email=email,
                delusion_prompt=input,
                delusion_shape=ukuran,
                delusion_result=images
            )
            await save.save()
            os.remove(temp_file.name)
            response = {
                'delusion_id': delusion_id,
                'delusion_shape': ukuran,
                'delusion_image': data[url_index]['keterangan']
            }
            data_response.append(response)
        
        except Exception as e:
            delusion_id -= 1
            url_index -= 1
            jumlah += 1
    
    return data_response
        