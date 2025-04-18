from pydantic import BaseModel
from typing import Optional, List

class InteractionMessage(BaseModel):
    role: Optional[str]
    message: Optional[str]

class Interaction(BaseModel):
    interaction_id: str
    interactions: str  # JSON string of messages
    session_id: Optional[str]
    timestamp: Optional[str]
    user_id: Optional[str]
    ip_address: Optional[str]
    agent_id: Optional[str]
    agent_name: Optional[str]