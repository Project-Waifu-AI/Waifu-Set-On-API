from pydantic import BaseModel
from typing import Optional

class shareToSMD(BaseModel):
    audio_id: Optional[int]
    caption: Optional[str] = None