import requests
import tempfile
import os
import base64
import time
from configs import config

def post_audio_to_smd(user, caption, audio_download):
    get_audio = requests.get(url=audio_download)
    if get_audio is None:
        return {
            'status': False,
            'keterangan': 'Failed to download audio after max retries.'
        }

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(get_audio.content)

    with open(temp_file.name, "rb") as file:
        audio = base64.b64encode(file.read()).decode("utf-8")

    
    post_data = {
        'userId': user.smdID,
        'desc': caption,
        'file': f"data:{file.name.split('.')[-1]};base64,{audio}"
    }
    
    post_response = requests.post(url=f'{config.smd_domain}posts', data=post_data)
    
    if post_response.status_code is False:
        return {
            'status': False,
            'keterangan': 'Failed to make post request after max retries.'
        }
    else:
        return {
            'status': True,
            'keterangan': 'File berhasil diupload'
        }