from typing import Optional

def user_response(user, password=None):
    response = {
        "nama": user.nama,
        "email": user.email,
        'akunwso': user.wsoAuth,
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