from pydantic import BaseModel, SecretStr
from typing import Optional

class ChatCommunity(BaseModel):
    community_name: Optional[str]
    community_desc: Optional[str]
    community_type: Optional[str]
    