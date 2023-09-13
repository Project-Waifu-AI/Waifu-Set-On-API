import requests
from database.model import logaudio, logpercakapan
from pydub import AudioSegment
import io

def request_audio(text,spaeker_id:int):
    url = 'https://deprecatedapis.tts.quest/v2/voicevox/audio/'
    params = {
        'key': config.api_key_voicevox,
        'speaker': spaeker_id,
        'pitch': '0',
        'intonationScale': '1',
        'speed': '1',
        'text': text
    }

    response = requests.get(url, params=params)
    with open('voice.wav', 'wb') as file:
        file.write(response.content)

async def blob_to_wav(data_audio):
    audio = AudioSegment.from_file(io.BytesIO(data_audio), format="wav")
    output_file = config.output_file
    await audio.export(output_file, format='wav')