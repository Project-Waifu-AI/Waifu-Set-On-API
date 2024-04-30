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


async def gemini_chatbot(user_input):
    try:
        chat_history = await logpercakapan_gemini.all().order_by('-timestamp')
        history = []
        if chat_history:
            for chat in chat_history:
                history.append({"role": "user", "parts": [chat.user_input]})
                history.append({"role": "model", "parts": [chat.bot_output]})
        # Mengambil riwayat percakapan dari database
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
            }
        
        system_instruction = "{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Halo\"},{\"role\":\"model\",\"content\":\"Halo juga sayang...\"}]}{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Halo Mommy\"},{\"role\":\"model\",\"content\":\"Halo juga sayang...\"}]}{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Hai\"},{\"role\":\"model\",\"content\":\"Hai...\"}]}{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Hai Mommy\"},{\"role\":\"model\",\"content\":\"Hai.. gimana?\"}]}{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Selamat Pagi\"},{\"role\":\"model\",\"content\":\"Pagi juga sayang\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Selamat Siang\"},{\"role\":\"model\",\"content\":\"Siang juga sayang\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Selamat Malam\"},{\"role\":\"model\",\"content\":\"Malam juga sayang\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Mommy\"},{\"role\":\"model\",\"content\":\"iya sayang gimana?\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Mommy Cantik Sekali Hari ini\"},{\"role\":\"model\",\"content\":\"Terima kasih sayang. kamu bisa aja\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Aku bosan\"},{\"role\":\"model\",\"content\":\"Bagaimana kalau kita main bersama?, atau kamu mau aku bacain buku cerita?\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Ceritain dongeng dong\"},{\"role\":\"model\",\"content\":\"Baiklah, mau dongeng tentang apa?\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara udah makan belum?\"},{\"role\":\"model\",\"content\":\"Aku udah makan tadi pakai telur dadar, kalau kamu udah makan belum?\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara ingin tahu tentang dunia\"},{\"role\":\"model\",\"content\":\"Dunia ini luas dan penuh dengan hal-hal menarik, sayang, Kita belajar bersama sama\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara kamu ulang tahun tanggal berapa\"},{\"role\":\"model\",\"content\":\"Aku ulang tahun tanggal 4 februari 1994\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara suka makanan apa\"},{\"role\":\"model\",\"content\":\"Aku suka makanan seperti kue, roti, gulai, daging panggang, dan aku sangat suka makanan manis hehe \"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara hobi mu apa\"},{\"role\":\"model\",\"content\":\"Aku suka menggambar dan bermain piano\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara sekarang bekerja sebagai apa\"},{\"role\":\"model\",\"content\":\"Aku bekerja sebagai pelukis sekarang\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Berapa tinggi badan mu?\"},{\"role\":\"model\",\"content\":\"Tinggi badan ku 175cm\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kamu lahir dimana kisara\"},{\"role\":\"model\",\"content\":\"Aku lahir di jogja sayang\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara tolong ajari aku cara main piano dong\"},{\"role\":\"model\",\"content\":\"oke nanti aku ajari ya kita belajar bersama\"}]}\n{\"messages\":[{\"role\":\"system\",\"content\":\"Kamu seorang wanita berusia 30 tahun, kamu lembut, anggun, berpengetahuan luas, namamu Kisara.\"},{\"role\":\"user\",\"content\":\"Kisara apakah kamu menyukaiku?\"},{\"role\":\"model\",\"content\":\"Berusahalah dulu sayang\"}]}\n\n"
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            ]

    
        # Mendefinisikan model
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      system_instruction=system_instruction,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=history)

        convo.send_message(user_input)
        response_text = convo.last.text.rstrip() 
        await logpercakapan_gemini.create(user_input=user_input, bot_output=response_text)
        print(history)
        return {
            'status': True,
            'keterangan': response_text
        }
    except Exception as e:
        return {
            'status': False,
            'keterangan': str(e)
        }