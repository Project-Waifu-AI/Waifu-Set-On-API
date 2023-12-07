from langdetect import detect
from googletrans import Translator
import openai
from configs import config

tl = Translator()

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