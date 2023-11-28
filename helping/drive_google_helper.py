from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database.model import logaudio, userdata
import requests
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
    
def folder_set_drive(access_token: str, email: str):
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
        file = service.files().create(body=file_metadata, fields='id').excute()
        return file.get('id')
async def store_audio(audio_id, email):
    data = await logaudio.filter(email=email, audio_id=audio_id).first()
    user = await userdata.filter(email=email).first()
    get_audio = requests.get(data.audio_download)
    audio_filename = 'share_audio.mp3'
    with open(audio_filename, 'wb') as audio_file:
        audio_file.write(get_audio.content)

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