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
        "akunwso": user.akunwso,
        "status": user.status
    }
    
    if password is not None:
        response["password"] = password
    
    return response

async def access_token_response(user, password=None):
    user_id = user.user_id
    access_tokens = await access_token_data.filter(user_id=user_id).all()
    valid_access_tokens = []

    for data in access_tokens:
        is_valid = await check_access_token_expired(data.access_token)

        if not is_valid:
            continue

        valid_access_tokens.append(data)

    if valid_access_tokens:
        response_list = []

        for data in valid_access_tokens:
            response = {
                'access_token': str(data.access_token),
                'waktu_basi': str(data.waktu_basi),
                'data_user': {
                    "user_id": str(user.user_id),
                    "nama": user.nama,
                    "email": user.email,
                    "akunwso": user.akunwso,
                    "status": user.status
                }
            }

            if password is not None:
                response['data_user']['password'] = password

            response_list.append(response)

        return response_list
    else:
        return []
