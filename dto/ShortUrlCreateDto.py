from pydantic import BaseModel
from datetime import datetime

class ShortUrlCreateDto(BaseModel):
    url: str
    expiresAt: datetime = None
    alias: str = ""