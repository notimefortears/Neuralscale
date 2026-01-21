from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List

class RawThreatEvent(BaseModel):
    id: str
    source: str
    created_at: datetime
    title: Optional[str] = None
    text: str
    url: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)

class EnrichedThreatEvent(RawThreatEvent):
    severity: float
    entities: List[dict]  # {"label": "...", "text": "...", "score": ...}
