from database.model import access_token_data
from helping.auth_helper import check_access_token_expired

def pesan_response(email: str, pesan: str):
    return {
        'email':email,
        'pesan':pesan
    }

def user_response(user, password=None):
    response = {
        "user_id": str(user.user_id),
        "nama": user.nama,
        "email": user.email,
        'gender': user.gender,
        'ulang tahun': user.ulang_tahun,
        'karakter_yang_dimiliki': user.karakterYangDimiliki,
        'NegaiKanjo': user.NegaiKanjo,
        "akunwso": user.akunwso,
        "status": user.status
    }
    if user.admin is True:
        response['role'] = 'admin'
    elif user.admin is False:
        response['role'] = 'user'
    if password is not None:
        response["password"] = password
    
    return response

async def access_token_response(user, password=None):
    access_tokens = await access_token_data.filter(user_id=user.user_id).all()
    response = []
    for data in access_tokens:
        validasi = await check_access_token_expired(access_token=data.access_token)
    
    for valid in access_tokens:
        access_token = {
            'access_token': str(valid.access_token),
            'waktu_basi': str(valid.waktu_basi),
            'level': valid.level,
            'data_user': user_response(user=user, password=password)
        }
        response.append(access_token)
    return response

def karakter_response(karakter):
    karakter_dict = {
                'nama': karakter.nama,
                'bahasa_yang_digunakan': karakter.bahasaYangDigunakan,
                'speaker id': karakter.speakerID,
                'informasi tambahan': karakter.informasi_tambahan,
                }
    return karakter_dict