from pydantic import BaseModel
from typing import Optional

class CreateDelusion(BaseModel):
    input: Optional[str]
    ukuran: Optional[str]
    jumlah: Optional[int]
    
class VariantDelusion(BaseModel):
    id: Optional[int]
    jumlah: Optional[int]
    resize: Optional[bool] = False