from langdetect import detect
from typing import Optional
from google_trans_new import google_translator
from configs import config
from openai import OpenAI

client_openai = OpenAI(api_key=config.api_key_openai)

tl = google_translator(url_suffix="com",timeout=5)
    
def translate_target_premium(input: str, bahasa_target: str):
    set = [
        {
            'role': 'system', 'content': f'translate langsung bahasa yang diinputkan ke bahasa {bahasa_target}'
        }
    ]
    trans={
        'role': 'user', 'content': input
    }
    set.append(trans)
    
    try:
        translate = client_openai.chat.completions.create(
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

def translate_target(input: str, bahasa_target: str, bahasa_asal: str | None):
    if bahasa_asal is None:
        bahasa_asal = detect(input)
    
    try:  
        response = tl.translate(input.lower(), lang_src=bahasa_asal, lang_tgt=bahasa_target)
        return {
            'status': True,
            'response': response
        }
    except Exception as e:
        return{
            'status': False,
            'response': str(e)
        }
       
def cek_bahasa(bahasa: str):
    if bahasa in config.bahasa:
        value = config.bahasa[bahasa]
        return {
            'status': True,
            'keterangan': str(value)
        }
    else:
        return {
            'status': False,
            'keterangan': 'bahasa yang anda gunakan tidak valid'
        }