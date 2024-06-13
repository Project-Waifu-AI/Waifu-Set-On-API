from typing import Optional

def success_response(action: str, pesan: str, kepada: Optional[str] = 'user', dari: Optional[str] = 'system'):
    return {
        'kepada': kepada,
        'dari': dari,
        'pesan':pesan,
        'action': action
    }

def error_response(pesan: str, penyebab: str, action: str, kepada: Optional[str] = 'user', dari: Optional[str] = 'system'):
    return {
        'kepada': kepada,
        'dari': dari,
        'pesan': pesan,
        'penyebab': penyebab,
        'action': action,
    }