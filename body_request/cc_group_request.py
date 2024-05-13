from pydantic import BaseModel
from typing import Optional

class ChatGroup(BaseModel):
    group_name: Optional[str]
    group_desc: Optional[str]
    group_member: Optional[dict]
    