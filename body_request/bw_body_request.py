from pydantic import BaseModel
from typing import Optional

class share_to_twiter(BaseModel):
    audio_id: Optional[int]
    caption: Optional[str] = None