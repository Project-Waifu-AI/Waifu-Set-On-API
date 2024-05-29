from typing import Optional


# BASIC RESPONSE
def success_response(action: str, pesan: str, kepada: Optional[str] = 'user', dari: Optional[str] = 'system'):
    return {
        'kepada': kepada,
        'dari': dari,
        'pesan':pesan,
        'action': action
    }

def error_response(pesan: str, penyebab: str, action: str, kepada: Optional[str] = 'user', dari: Optional[str] = 'system'):
    return {
        'kepada': kepada,
        'dari': dari,
        'pesan': pesan,
        'penyebab': penyebab,
        'action': action,
    }

# MASIVE RESPONSE
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

def karakter_response(karakter):
    karakter_dict = {
                'nama': karakter.nama,
                'variant': karakter.variant,
                'rarity': karakter.rarity,
                'desc': karakter.desc,
                'asset': 'dummy_link'
                }
    return karakter_dict

# FITUR RESPONSE
def bw_response(email: str, audio_id: str, transcript: str, translation: str):
    return {
        'email': email,
        'audio_id': audio_id,
        'transcript': transcript,
        'translation': translation
    }

def aiu_response(pesan: str, response: str, translate: str, id_percakapan, email: str):
    return {
        'email': email,
        'id_percakapan': id_percakapan,
        'pesan': pesan,
        'response': response,
        'translate': translate 
    }