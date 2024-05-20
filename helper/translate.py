from langdetect import detect
from typing import Optional
from google_trans_new import google_translator
from configs import config
from openai import OpenAI
import asyncio
import re

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
            model='gpt-3.5-turbo',
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

def detect_text_in_parentheses(text: str):
    # Gunakan regex untuk mendeteksi teks di dalam kurung
    matches = re.findall(r'\((.*?)\)', text)
    # Kembalikan teks yang ada di dalam kurung
    return matches

async def translate_to_japanese(text: str):
    # Deteksi teks di dalam kurung
    texts_in_parentheses = detect_text_in_parentheses(text)
    # Hapus teks di dalam kurung dari teks asli
    for t in texts_in_parentheses:
        text = text.replace(f'({t})', '')
    # Terjemahkan teks tanpa teks di dalam kurung ke bahasa Jepang
    translated_text = await asyncio.to_thread(tl.translate, text, lang_tgt='ja')
    # Tambahkan kembali teks yang ada di dalam kurung ke dalam teks terjemahan
    for t in texts_in_parentheses:
        translated_text = translated_text.replace(f'({t})', f'({t})')
    return translated_text