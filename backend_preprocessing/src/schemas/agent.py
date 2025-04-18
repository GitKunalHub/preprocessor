from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SchedulingConfig(BaseModel):
    type: str = Field(default="daily")
    start_time: str = Field(default="00:00")

class AgentConfig(BaseModel):
    _id: str
    scheduling: Optional[SchedulingConfig]
    # Add more agent config fields as needed