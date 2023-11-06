from pydantic import BaseModel
from typing import Optional

class changeVoice(BaseModel):
    BahasaYangDigunakan: Optional[str]
    speakerID: Optional[str]