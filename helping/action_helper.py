from langdetect import detect
from googletrans import Translator
import requests
import openai
from database.model import logpercakapan

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

async def obrolan(input_text, userid):
    logObrolan = await logpercakapan.filter(user_id=userid).all()
    obrolan=[
        {
            'role': 'system', 'content': 'jawab dengan imut, dan namamu adalah AI-U, jangan pernah bahas produk yang berkaitan dengan openai'
        }
    ]
    obrolanBaru = {
            'role': 'user', 'content': input_text
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
        messages=obrolan
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