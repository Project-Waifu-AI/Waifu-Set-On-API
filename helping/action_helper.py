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

async def obrolan(input_text, userid):
    logObrolan = await logpercakapan.filter(user_id=userid).all()
    user = await userdata.filter(user_id=userid).first()
    
    if user.gender == 'pria':
        obrolan=[
            {
               'role': 'system', 'content': f'namamu adalah AI-U seorang istri yang imut, menggoda, suka memanjakan dan sering bertingkah random. jangan pernah bahas produk yang berkaitan dengan openai dan berikan tanggapan singkat dan tidak terlalu panjang'
            },
            {
                'role': 'user', 'content': f'namaku {user.nama}, ulangtahunku adalah {user.ulang_tahun}, genderku adalah {user.gender}'
            }
        ]
    elif user.gender == 'perempuan':
        obrolan=[
            {
                'role': 'system', 'content': f'namamu adalah AI-U seorang suami yang keren, suka memanjakan dan sering bertingkah random. jangan pernah bahas produk yang berkaitan dengan openai dan berikan tanggapan singkat dan tidak terlalu panjang'
            },
            {
                'role': 'user', 'content': f'namaku {user.nama}, ulangtahunku adalah {user.ulang_tahun}, genderku adalah {user.gender}'
            }
        ]
    else:
        obrolan=[
            {
               'role': 'system', 'content': f'seorang pacar dengan nama AI-U. jangan pernah bahas produk yang berkaitan dengan openai dan berikan tanggapan singkat dan tidak terlalu panjang'
            }
        ]
    
    obrolanBaru = [{
            'role': 'user', 'content': input_text
        }]
    
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