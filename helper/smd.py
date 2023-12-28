import requests
import tempfile
import os
import base64
import time
from configs import config

def post_audio_to_smd_blob(user, caption, audio_download):
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
        
def post_audio_to_smd_file(user, caption, audio_download):
    get_audio = requests.get(url=audio_download)
    if get_audio.status_code != 200:
        return{
            'status': False,
            'keterangan': 'Failed to download audio'
        }
        
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(get_audio._content)
        
    path_file = temp_file.name
    file_name = f'{int(time.time())}_audio_wso_{user.email}.mp3'
    
    file = {'file': (file_name, open(path_file, 'rb'))}
    data = {'name': file_name}
    
    upload_response =requests.post(
        url=f'{config.smd_domain}upload', files=file, data=data
    )
    
    if upload_response.status_code != 200:
        return{
            'status': False,
            'keterangan': str(upload_response.text)
        }
    
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
    
    if post_response.status_code != 200:
        return{
            'status': False,
            'keterangan': 'something wrong when uploud to smd'
        }
    
    return{
        'status': True,
        'keterangan': 'file success uploud to SMD'
    }