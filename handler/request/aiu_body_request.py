from typing import Optional
from pydantic import BaseModel

class obrolan_aiu(BaseModel):
    karakter: Optional[str]
    input: Optional[str]
    bahasa: Optional[str]