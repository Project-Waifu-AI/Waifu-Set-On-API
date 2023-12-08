import requests
import tempfile
import os
import time
from configs import config

def post_audio_to_smd(user, log, caption):
    get_audio = retry_request(log.audio_download)
    if get_audio is None:
        return {
            'status': False,
            'keterangan': 'Failed to download audio after max retries.'
        }

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(get_audio.content)
    
    file_path = temp_file.name
    file_name = f'{int(time.time())}_audio_wso_{user.email}_{log.translate}.mp3'

    file = {'file': (file_name, open(file_path,'rb'))}
    data = {'name': file_name}

    upload_response = retry_request(f'{config.smd_domain}upload', files=file, data=data)
    if upload_response is False:
        return {
            'status': False,
            'keterangan': 'Failed to upload file after max retries.'
        }
    
    if caption is None:
        post_data = {
            'userId': user.smdID,
            'file': file_name
        }
    else:
        post_data = {
            'userId': user.smdID,
            'desc': caption,
            'file': file_name
        }
    post_response = retry_request(f'{config.smd_domain}posts', json=post_data)
    if post_response is False:
        return {
            'status': False,
            'keterangan': 'Failed to make post request after max retries.'
        }
    else:
        return {
            'status': True,
            'keterangan': 'File berhasil diupload'
        }
        
def retry_request(url, files=None, data=None, json=None, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(url, files=files, data=data, json=json)
            response.raise_for_status()
            return response
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            print(f"Error: {e}")
            print(f"Retrying request ({retries + 1}/{max_retries})...")
            time.sleep(1)
            retries += 1
    return False
