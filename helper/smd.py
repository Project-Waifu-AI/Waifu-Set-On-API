import requests
import tempfile
import os
import time
from configs import config

def post_audio_to_smd(user, log, caption):
    get_audio = requests.get(log.audio_download)
    if get_audio.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(get_audio.content)
    else:
        return{
            'status': False,
            'keterangan': str(get_audio.text)
        }

    file_path = temp_file.name
    file_name = f'{int(time.time())}_audio_wso_{user.email}_{log.translate}.mp3'

    file = {'file': (file_name, open(file_path,'rb'))}
    data = {'name': file_name}

    upload_response = requests.post(url=f'{config.smd_domain}upload', files=file, data=data)
    if upload_response.status_code != 200:
        return{
            'status': False,
            'keterangan': str(upload_response.text)
        }
    else:    
        
        if caption is None:
            post_data={
                'userId': user.smdID,
                'file': file_name
            }
        
        else:
            post_data={
                'userId': user.smdID,
                'desc': caption,
                'file': file_name
            }
        
        post_response = requests.post(
        url=f'{config.smd_domain}posts',
        json=post_data,
        headers={"Content-Type": "application/json"}
        )
        
        return{
            'status': True,
            'keterangan': 'file berhasil di upload'
        }