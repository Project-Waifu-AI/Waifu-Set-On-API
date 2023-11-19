from helping.auth_helper import check_access_token_expired
from typing import Optional

def pesan_response(pesan: str, email: Optional[str] = None):
    return {
        'email':email,
        'pesan':pesan
    }

def user_response(user, password=None):
    response = {
        "user_id": str(user.user_id),
        "nama": user.nama,
        "email": user.email,
        'akunwso': user.akunwso,
        'googleauth': user.googleAuth,
        'gender': user.gender,
        'ulang tahun': str(user.ulang_tahun),
        'karakter_yang_dimiliki': user.karakterYangDimiliki,
        'NegaiGoto': user.NegaiGoto,
        'AtsumaruKanjo': user.AtsumaruKanjo,
    }
    if user.admin is True:
        response['role'] = 'admin'
    elif user.admin is False:
        response['role'] = 'user'
    if password is not None:
        response["password"] = password
    
    return response

def karakter_response(karakter):
    karakter_dict = {
                'nama': karakter.nama,
                'bahasa_yang_digunakan': karakter.bahasaYangDigunakan,
                'speaker id': karakter.speakerID,
                'informasi tambahan': karakter.informasi_tambahan,
                }
    return karakter_dict