import requests

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
        'download': download,
        'streaming': streaming 
    }

response = request_audio(text='そのまま試すボタンを押した場合、次のようなレスポンスが帰ってきます。', speaker_id=18)  # Perbaiki penulisan variabel speaker_id
print(response)