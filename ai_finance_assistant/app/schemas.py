from pydantic import BaseModel
from typing import Optional

class TxQuery(BaseModel):
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    category: Optional[str] = None
    q: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None

class ChatQuery(BaseModel):
    question: str
