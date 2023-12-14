from langdetect import detect
from typing import Optional
from google_trans_new import google_translator
from configs import config
from openai import OpenAI

client_openai = OpenAI(api_key=config.api_key_openai)

tl = google_translator(url_suffix="com",timeout=5)

def to_japan(input: str, bahasa: Optional[str] = None):
    if bahasa == None:
        src = detect(input)
    else:
        src = bahasa
    
    try:  
        if src != 'ja':
            response = tl.translate(input.lower(), lang_src=src, lang_tgt='ja')
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