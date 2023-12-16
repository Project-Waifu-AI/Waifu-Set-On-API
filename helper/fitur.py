import openai
import requests
from database.model import logpercakapan, userdata
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
            'keterangan': str(e)
        }

async def obrolan(input_text, email, setKarakter):
    logObrolan = await logpercakapan.filter(email=email).all()
    user = await userdata.filter(email=email).first()
    obrolan = []
    obrolan.append(setKarakter)
    obrolanBaru = {
            'role': 'user', 'content': input_text
        }
    setNama = f'nama user adalah {user.nama}' if user.nama is not None else ''
    setUlangTahun = f'ulang tahun user adalah {user.ulang_tahun}' if user.ulang_tahun is not None else ''
    setGender = f'gender user adalah {user.gender}' if user.gender is not None else ''
    setUser = {
        'role': 'assistant', 'content': f'{setNama},{setUlangTahun},{setGender}'
    }
    obrolan.append(setUser)
    if logObrolan:
        for data in logObrolan:
            jsonLog = {
                'role': 'user', 'content': data.input
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
            'output': str(e)
        }
        
def generateDelusion(prompt: str, ukuran: str, premium: str, jumlah: str):
    if premium is True:
        try:
            response = client_openai.images.generate(
                model="dall-e-2",
                prompt=f"{prompt}, anime style images",
                size=ukuran,
                quality="hd",
                n=jumlah,
            )
        except Exception as e:
            return {
                'status': False,
                'keterangan': str(e)
            }
        
    if premium is False:
        try:
            response = client_openai.images.generate(
                model="dall-e-3",
                prompt=f"{prompt}, anime style images",
                size=ukuran,
                quality="standard",
                n=jumlah,
            )
        except Exception as e:
            return {
                'status': False,
                'keterangan': str(e)
            }
            
def varint_delusion(image_array, jumlah):
    try:
        response = client_openai.images.create_variation(
            image=image_array,
            n=jumlah,
            model="dall-e-2",
            size="1024x1024"
        )
    except openai.OpenAIError as e:
        return{
            'status': False,
            'keterangan': str(e)
        }
    return{
        'status': True,
        'keterangan': {response.data}
    }
