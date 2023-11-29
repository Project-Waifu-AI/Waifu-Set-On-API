from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timezone
from database.model import logaudio, userdata, token_google
import requests
import os
import json

def create_drive_service(access_token):
    creds = Credentials(token=access_token)
    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as e:
        return{
            'status': False,
            'keterangan': str(e)
        }
    
def create_folder_gdrive(access_token: str, email: str):
    service = create_drive_service(access_token=access_token)
    namaFolder = f'WSO_{email.upper()}'
    file_metadata = {
        "name": namaFolder,
        "mimeType": "application/vnd.google-apps.folder",
    }
    cari = find_folder_id(service=service, nama_folder=namaFolder)
    if cari:
        return cari
    else:
        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

def refreshToken_google(refresh_token):
        with open('client_secret.json', 'r') as file:
            data = json.loads(file.read())

        client_id = data.get('web', {}).get('client_id', None)
        client_secret = data.get('web', {}).get('client_secret', None)

        params = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
        }

        authorization_url = "https://oauth2.googleapis.com/token"

        r = requests.post(authorization_url, data=params)
        data = r.json()
        return data['access_token']

async def use_AccessToken_google(email):
    token = await token_google.filter(email=email).first()
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    if token.token_exp.replace(tzinfo=timezone.utc) <= now:
        access_token = refreshToken_google(refresh_token=token.refersh_token)
        return access_token
    else:
        return token.access_token

async def simpanKe_Gdrive(email, audio_id, delete: bool):
    data = await logaudio.filter(email=email,audio_id=audio_id).first()
    user = await userdata.filter(email=email).first()
    
    get_audio = requests.get(data.audio_download)
    audio_filename = f'{str(data.translate)}.mp3'
    with open(audio_filename, 'wb') as audio_file:
        audio_file.write(get_audio.content)
    
    access_token = await use_AccessToken_google(email=email)
    print (access_token)
    service = create_drive_service(access_token=access_token)
    
    file_metadata = {
        'name': os.path.basename(audio_filename),
        'parents': [user.driveID]
    }
    media = MediaFileUpload(audio_filename, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    if delete is True:
        await data.delete()
        
    return file.get('id')

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