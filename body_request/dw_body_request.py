from pydantic import BaseModel
from typing import Optional

class createWaifu(BaseModel):
    input: Optional[str]
    ukuran: Optional[str]