from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from configs import config
from database.model import AIUHistory
from helper.fitur import obrolan_gpt, request_audio
from helper.translate import translate_target, translate_target_premium
from helper.access_token import check_access_token_expired, decode_access_token
from handler.response.basic import error_response, success_response
from helper.premium import check_premium

router = APIRouter(prefix='/websoket/aiu', tags=['AIU-WEBSOCKET'])
        
@router.websocket('/action')
async def socketObrolan(websocket: WebSocket, access_token: str):
    await websocket.accept()
    
    try:
        while True:
            permintaan = await websocket.receive_json()
            # check access_token setiap ws menerima json
            check = check_access_token_expired(access_token=access_token)
            if check is True:
                break
            else:
                dataJWT = decode_access_token(access_token=access_token)
                email = dataJWT.get('sub')
            
            # action obrolan aiu semua karakter
            if permintaan['action']['type'] == 'obrolan':
                # set data karakter untuk dibuat request
                pesan = permintaan['data']
                user_data = await logpercakapan.filter(email=email).order_by("-id_percakapan").first()
                
                if permintaan['action']['karakter'] == 'meimei-himari':
                    speakerId = 14
                    setkarakter = {
                        'role':'system',
                        'content':'namamu adalah meimei himari,penuai dari dunia bawah,memiliki mata untuk hal-hal yang indah,umur 18 tahun,ras reaper,tanggal lahir 1 september,hal paling disukai anak perempuan yang lucu,kepribadian baik hati dan rapi, jawab singkat'
                    }
                
                elif permintaan['action']['karakter'] == 'kusukabe-tsumugi':
                    speakerId = 8
                    setkarakter = {
                        'role':'system',
                        'content':'namamu adalah kusukabe tsumugi,gadis manusia yang bersekolah di sekolah menengah atas di Prefektur Saitama,Kepribadian terlihat nakal tetapi sebenarnya memiliki sisi yang serius,umur 18 tahun,tinggi badan 155 cm, hobi mengunjungi situs web streaming video,makanan favorit kari jepang, tempat lahir saitama jepang, jawab singkat'
                    }
                
                elif permintaan['action']['karakter'] == 'no-7':
                    speakerId = 29
                    setkarakter = {
                        'role':'system',
                        'content':'namamu adalah NO.7,Seorang wanita misterius yang identitasnya sulit dipahami,Kepribadian Minimalis, hanya menggunakan lilin untuk penerangan di kamarnya,umur 23 tahun,tinggi badan 165 cm, suka anak-anak,hobi Membudidayakan lobak daikon, jawab singkat'
                    }
                
                elif permintaan['action']['karakter'] == 'nurse-t':
                    speakerId = 47
                    setkarakter = {
                        'role':'system',
                        'content':'namamu adalah nurse-T,Robot berbentuk perawat yang dibuat oleh seorang dokter,Kepribadian ditetapkan sebagai seorang gadis,umur 5 bulan,tanggal lahir 3 desember,tinggi badan 150 - 160 cm, nama panggilan TT, produsen Robot soba kecil(dokter), jawab singkat'
                    }
                
                elif permintaan['action']['karakter'] == 'sayo':
                    setkarakter = {
                        'role':'system',
                        'content':'namamu adalah SAYO,Gadis kucing yang banyak bicara,Kepribadian Minimalis,tinggi badan 135 cm (termasuk telinga kucin),makanan favorit makanan faforit makanan kaleng, jawab singkat'
                    }
                    speakerId = 46
                
                else:
                    break
    
                if user_data:
                    id_percakapan = user_data.id_percakapan + 1
                else:
                    id_percakapan = 1  
                
                # proses audio            
                response = await obrolan_gpt(input_text=pesan, email=email, setKarakter=setkarakter)
                
                if response['status'] is True:
                    premium = await check_premium(email=email)
                    
                    if premium['status'] is False:
                        translate = translate_target(input=response['output'], bahasa_asal=None, bahasa_target='ja')
                    else:
                        
                        if premium['keterangan'].lower() == 'aiu' or premium['keterangan'].lower() == 'admin':
                            translate = translate_target_premium(input=response['output'], bahasa_target='jepang')
                        else:
                            translate = translate_target(input=response['output'], bahasa_asal=None, bahasa_target='ja')
                    
                    if translate['status'] is True:
                        data_audio = request_audio(text=translate['response'], speaker_id=speakerId)
                        
                        if data_audio['status'] is False:
                            await websocket.send_json()
                        
                        data = [{
                            'pesan': pesan,
                            'response': response['output'],
                            'translate': translate['response'],
                        }]
                        
                        data.append(data_audio)
                        save = logpercakapan(id_percakapan=id_percakapan, email=email, input=pesan, output=response['output'], translate=translate['response'], audio_streming=data_audio['streaming_audio'], audio_download=data_audio['download_audio'])
                        await save.save()            
                        await websocket.send_json(data)
                    else:
                        await websocket.send_json(error_response(kepada=email, pesan='something gone wrong', penyebab=translate['response']))
                        
                        
            elif permintaan['action']['type'] == 'delete-all-log-percakapan':
                data = await logpercakapan.filter(email=email).first()
                await data.delete()
                response = success_response(kepada=data.email, action='delete-history-percakapan-aiu', pesan='Your conversation history on the AIU feature has been successfully deleted')
                await websocket.send_json(response)
            
            else:
                break
            
    except WebSocketDisconnect or WebSocketException:
        print("Client disconnected")