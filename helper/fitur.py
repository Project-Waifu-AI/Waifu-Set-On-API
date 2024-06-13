import openai
import requests
from io import BytesIO
from configs import config

client_openai = openai.OpenAI(api_key=config.api_key_openai)

def request_audio(text, speaker_id: int):
    try:
        url = 'https://api.tts.quest/v3/voicevox/synthesis/'
        params = {
            'speaker': speaker_id, 
            'text': text
        }
        response = requests.get(url, params=params)
        data = response.json()
        download = data.get('mp3DownloadUrl')
        streaming = data.get('mp3StreamingUrl') 
        return {
            'status': True,
            'download_audio': download,
            'streaming_audio': streaming
        }
    
    except Exception as e:
        return{
            'status': False,
            'penyebab': str(e)
        }

async def obrolan_gpt(input_text, user, setKarakter):
    logObrolan = await user.aiu_history.all()
    obrolan = []
    obrolan.append(setKarakter)
    obrolanBaru = {
            'role': 'user', 'content': input_text
        }
    setNama = f'nama user adalah {user.nama}' if user.nama is not None else ''
    setUlangTahun = f'ulang tahun user adalah {user.birth_date}' if user.birth_date is not None else ''
    setGender = f'gender user adalah {user.gender}' if user.gender is not None else ''
    setUser = {
        'role': 'assistant', 'content': f'{setNama},{setUlangTahun},{setGender}'
    }
    obrolan.append(setUser)
    if logObrolan:
        for data in logObrolan:
            jsonLog = {
                'role': 'user', 'content': data.user_input
            }
            obrolan.append(jsonLog)
        obrolan.append(obrolanBaru)
    else:
        obrolan.append(obrolanBaru)
    try:
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=obrolan,
            temperature = 0.5,
            max_tokens = 40
        )
        print (response)
        return {
            'status': True,
            'output':response.choices[0].message.content
        }
    except Exception as e:
        return{
            'status': False,
            'penyebab': str(e)
        }
        
def generateDelusion(prompt: str, ukuran: str, premium: str, jumlah: str):
    data = []
    index = -1
    if premium == True:    
        try:  
          response = client_openai.images.generate(
              model="dall-e-2",
              prompt=f"{prompt}, anime style images",
              size=ukuran,
              quality="hd",
              n=jumlah,
          )
              
          for _ in range (jumlah):
              index += 1 
              url_data = {
                  'status': True,
                  'keterangan': response.data[index].url
              }
              data.append(url_data)
          return data
        except Exception as e:
          data.append(
            {
              'status': False,
              'penyebab': str(e)
            }
          )
    
    elif premium == False:    
        try:
          response = client_openai.images.generate(
              model="dall-e-2",
              prompt=f"{prompt}, anime style images",
              size=ukuran,
              quality="standard",
              n=jumlah,
          )
          
          for _ in range (jumlah):
              index += 1 
              url_data = {
                  'status': True,
                  'keterangan': response.data[index].url
              }
              data.append(url_data)
        except Exception as e:
          data.append(
            {
              'status': False,
              'penyebab': str(e)
            }
          )
        
        return data
    
    
def generateDelusionVariant(images_data, jumlah: str):
    data = []
    index = -1    
    try:  
        response = client_openai.images.create_variation(
            image = images_data,
            n=jumlah,
            size='1024x1024'
        )
            
        for _ in range (jumlah):
            index += 1 
            url_data = {
                'status': True,
                'keterangan': response.data[index].url
            }
            data.append(url_data)
        return data
    except Exception as e:
        data.append(
        {
            'status': False,
            'penyebab': str(e)
        }
        )
        
        return data
    
def download_audio(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        audio_data = BytesIO(response.content)
        return audio_data.getvalue()
    except requests.RequestException as e:
        return str(e)
