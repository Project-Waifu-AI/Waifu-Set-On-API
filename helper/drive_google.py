from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timezone
from database.model import UserData, UserGoogleAuth
import requests
import time
import json
import os
import tempfile

def create_drive_service(access_token):
    creds = Credentials(token=access_token)
    try:
        
        service = build("drive", "v3", credentials=creds)
        return {
            'status': True,
            'keterangan': service
        }
    
    except HttpError as e:
        return{
            'status': False,
            'penyebab': str(e)
        }
    
def create_folder_gdrive(access_token: str):
    service_response = create_drive_service(access_token=access_token)
    
    if service_response['status'] is False:
        return {
            'status': False,
            'penyebab': service_response['keterangan']
        }
    else:
        service = service_response['keterangan']

    namaFolder = f'WaifuSetOn'
    
    file_metadata = {
        "name": namaFolder,
        "mimeType": "application/vnd.google-apps.folder",
    }
    
    cari = find_folder_id(service=service, nama_folder=namaFolder)
    
    if cari:
        return {
            'status': True,
            'keterangan': cari
        }
    
    else:
        try:
            folder = service.files().create(body=file_metadata, fields='id').execute()
        except HttpError as e:
            return {
                'status': False,
                'penyebab': str(e)
            }
        
        return {
            'status': True,
            'keterangan': folder.get('id')
        }

async def use_AccessToken_google(user):
    token_data = await UserGoogleAuth.get_or_none(user=user)
    if token_data is None:
        return {
            'status': False,
            'penyebab': 'Your Google token was not found'
        }
    
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    
    with open('client_secret.json', 'r') as file:
        data = json.loads(file.read())
    
    client_id = data.get('web', {}).get('client_id', None)
    client_secret = data.get('web', {}).get('client_secret', None)
    
    if token_data.token_exp.replace(tzinfo=timezone.utc) <= now:
        
        params = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": token_data.refresh_token
        }

        authorization_url = "https://oauth2.googleapis.com/token"
        
        try:
            r = requests.post(authorization_url, data=params)
            data = r.json()
        
        except Exception as e:
            return{
                'status': False,
                'penyebab': str(e)
            }
        
        return {
            'status': True,
            'keterangan': data['access_token']
        }
    
    else:
        return {
            'status': True,
            'keterangan': token_data.access_token
        }

# MAINTAIN
'''
async def simpanKe_Gdrive(user, download_audio,delete: bool):
    can_i = await use_AccessToken_google(email=user.email)
    data_audio = await user.bw_history
    if can_i['status'] is False:
        return can_i
    else:
        access_token = can_i['keterangan']
    
    get_audio = requests.get(download_audio)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(get_audio.content)
    
    service_response = create_drive_service(access_token=access_token)
    
    if service_response['status'] is False:
        os.remove(temp_file.name)
        return {
            'status': False,
            'penyebab': service_response['keterangan']
        }
    else:
        service = service_response['keterangan']
    
    file_metadata = {
        'name': f'{str(user.aiu_history.japanese_output)}.mp3',
        'parents': [user.google_auth.drive_id]
    }
    try:
        media = MediaFileUpload(temp_file.name, mimetype='application/octet-stream')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        if delete is True:
            await user.aiu_his.delete()
        
        return {
            'status': True,
            'keterangan': file.get('id')
        }
    
    except HttpError as e:
        os.remove(temp_file.name)
        return {
            'status': False,
            'penyebab': str(e)
        }
'''

def find_folder_id(service, nama_folder):
    query = f"name = '{nama_folder}' and mimeType = 'application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, fields="files(id)").execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']  
    else:
        return None 
    
def find_file_id(service, nama_file):
    query = f"name = '{nama_file}' and trashed=false"
    response = service.files().list(q=query, fields="files(id)").execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']  
    else:
        return None