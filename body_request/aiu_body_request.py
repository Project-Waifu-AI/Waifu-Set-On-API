from typing import Optional
from pydantic import BaseModel

class obrolan_aiu(BaseModel):
    karakter: Optional[str]
    input: Optional[str]
    bahasa: Optional[str]

class Gemini_aiu(BaseModel):
    message:str

class ChatRequest(BaseModel):
    input_text: str
    email: str