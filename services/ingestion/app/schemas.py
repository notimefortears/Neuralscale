from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class RawThreatEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    created_at: datetime
    title: Optional[str] = None
    text: str
    url: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
