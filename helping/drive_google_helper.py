from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from database.model import logaudio, userdata
import requests
import os

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
    namaFolder = f'WSO_{email}'
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

async def simpanKe_Gdrive(email, audio_id):
    data = await logaudio.filter(email=email, audio_id=audio_id).first()
    user = await userdata.filter(email=email).first()
    
    
    
    get_audio = requests.get(data.audio_download)
    audio_filename = f'audio_bw_{email}_{audio_id}.mp3'
    with open(audio_filename, 'wb') as audio_file:
        audio_file.write(get_audio.content)
    
    service = create_drive_service()
    
    file_metadata = {
        'name': os.path.basename(audio_filename),
        'parents': [user.driveID]
    }
    media = MediaFileUpload(audio_filename, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

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