from langdetect import detect
from googletrans import Translator
import requests
import openai
from database.model import logpercakapan, userdata

tl = Translator()

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

async def obrolan(input_text, userid, setKarakter):
    logObrolan = await logpercakapan.filter(user_id=userid).all()
    user = await userdata.filter(user_id=userid).first()
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
        response = openai.ChatCompletion.create(
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

def to_japan(input):
    detected_language = detect(input)
    try:  
        if detected_language != 'ja':
            response = tl.translate(input, src=detected_language, dest='ja').text
            return {
                'status': True,
                'response': response
            }
        else:
            return {
                'status': True,
                'response': input
            }
    except Exception as e:
        return{
            'status': False,
            'response': str(e)
        }
    
def to_japan_premium(input):
    set = [
        {
            'role': 'system', 'content': 'translate langsung bahasa yang diinputkan ke bahasa jepang'
        }
    ]
    trans={
        'role': 'user', 'content': input
    }
    set.append(trans)
    
    try:
        translate = openai.ChatCompletion.create(
            model='gpt-4',
            messages=set
        )
        print (translate)
        return {
            'status':True,
            'response': translate.choices[0].message.content
        }
    
    except Exception as e:
        return{
            'status': False,
            'response': str(e)
        }