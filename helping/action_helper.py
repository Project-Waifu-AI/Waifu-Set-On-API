from langdetect import detect
from googletrans import Translator
import requests
import openai
from database.model import logpercakapan, userdata

tl = Translator()

def request_audio(text, speaker_id: int):
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
        'download_audio': download,
        'streaming_audio': streaming
    }

async def obrolan(input_text, userid, setKarakter):
    logObrolan = await logpercakapan.filter(user_id=userid).all()
    user = await userdata.filter(user_id=userid).first()
    obrolan = []
    obrolan.append(setKarakter)
    obrolanBaru = {
            'role': 'user', 'content': input_text
        }
    if user.ulang_tahun is not None:
        ulang_tahun = user.ulang_tahun
    
    if user.nama is not None:
        nama= user.nama
    
    if user.gender:
        gender = user.gender

    setUser = {
        'role': 'user', 'content': f'namaku adalah {nama}'
    }
    
    if logObrolan:
        for data in logObrolan:
            jsonLog = {
                'role': 'user', 'content': data.input
            }
            obrolan.append(jsonLog)
        obrolan.append(obrolanBaru)
    else:
        obrolan.append(obrolanBaru)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=obrolan,
        temperature = 0
    )
    print (response)
    return response.choices[0].message.content

def to_japan(input):
    detected_language = detect(input)  
    if detected_language != 'ja':
        response = tl.translate(input, src=detected_language, dest='ja').text
        return response
    else:
        return input
    
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
    translate = openai.ChatCompletion.create(
        model='gpt-4',
        messages=set
    )
    print (translate)
    return translate.choices[0].message.content