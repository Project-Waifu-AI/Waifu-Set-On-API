from pydantic import BaseModel
from typing import Optional

class ChatCommunity(BaseModel):
    community_name: Optional[str]
    community_desc: Optional[str]
    community_member: Optional[dict]
    