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

async def obrolan(input, userid):
    existing_conversations = await logpercakapan.filter(user_id=userid).count()
    
    if existing_conversations > 0:
        user_inputs = await logpercakapan.filter(user_id=userid).order_by('id_percakapan').values_list('input', flat=True)
    else:
        user_inputs = []
    
    obrolan_log = [
        {"role": "system", "content": "jawab dengan imut"},
    ]
    for input_text in user_inputs[:-1]:
        obrolan_log.append({"role": "user", "content": input_text})

    obrolan_log.append({"role": "user", "content": input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=obrolan_log
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