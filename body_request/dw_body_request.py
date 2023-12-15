from pydantic import BaseModel
from typing import Optional

class CreateDelusion(BaseModel):
    input: Optional[str]
    ukuran: Optional[str]
    jumlah: Optional[int]
    
class VariantWaifu(BaseModel):
    id: Optional[str]
    jumlah: Optional[int]