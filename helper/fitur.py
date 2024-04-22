import openai
import requests
import google.generativeai as genai
from database.model import logpercakapan, logpercakapan_gemini, userdata
from configs import config

client_gemini = genai.configure(api_key=config.api_key_gemini)
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
    data = []
    index = -1
    if premium == True:    
        try:  
          response = client_openai.images.generate(
              model="dall-e-2",
              prompt=f"{prompt}, anime style images",
              size=ukuran,
              quality="hd",
              n=jumlah,
          )
              
          for _ in range (jumlah):
              index += 1 
              url_data = {
                  'status': True,
                  'keterangan': response.data[index].url
              }
              data.append(url_data)
          return data
        except Exception as e:
          data.append(
            {
              'status': False,
              'keterangan': str(e)
            }
          )
    
    elif premium == False:    
        try:
          response = client_openai.images.generate(
              model="dall-e-2",
              prompt=f"{prompt}, anime style images",
              size=ukuran,
              quality="standard",
              n=jumlah,
          )
          
          for _ in range (jumlah):
              index += 1 
              url_data = {
                  'status': True,
                  'keterangan': response.data[index].url
              }
              data.append(url_data)
        except Exception as e:
          data.append(
            {
              'status': False,
              'keterangan': str(e)
            }
          )
        
        return data
    
    
def generateDelusionVariant(images_data, jumlah: str):
    data = []
    index = -1    
    try:  
        response = client_openai.images.create_variation(
            image = images_data,
            n=jumlah,
            size='1024x1024'
        )
            
        for _ in range (jumlah):
            index += 1 
            url_data = {
                'status': True,
                'keterangan': response.data[index].url
            }
            data.append(url_data)
        return data
    except Exception as e:
        data.append(
        {
            'status': False,
            'keterangan': str(e)
        }
        )
        
        return data



async def gemini_chatbot(input_text, email):
    try:

        history = await logpercakapan_gemini.filter(email=email).order_by("-id").limit(10).all()
        print(f"Retrieved history: {history}")
        
        model = genai.GenerativeModel("gemini-pro")
        messages = []
        for item in history:
            messages.append({
                "role": "user",
                "parts": [item.input_text]
            })

            messages.append({
                "role": "model",
                "parts": [item.output_text]
            })

        messages.append({
            "role": "user",
            "parts": [input_text]
        })
        
        response = model.generate_content(messages)
        return response.text

    except Exception as e:
        return str(e)