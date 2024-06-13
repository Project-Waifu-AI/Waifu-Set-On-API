from typing import Optional

def bw_response(email: str, audio_id: str, transcript: str, translation: str, url_audio: str):
    return {
        'email': email,
        'audio_id': audio_id,
        'transcript': transcript,
        'translation': translation,
        'url_audio': url_audio
    }

def aiu_response(pesan: str, japanese_response: str, display: str, id_percakapan, email: str, url_audio: str):
    return {
        'email': email,
        'id_percakapan': id_percakapan,
        'input': pesan,
        'japanese_response': japanese_response,
        'display_response': display,
        'url_audio': url_audio
    }

def dw_response(id, result_link, shape, prompt):
    return {
        'ID': id,
        'result_source': result_link
    }

def audio_management_response(url_source, character, service):
    return {
        'url_source': url_source,
        'character': character,
        
    }