from pydantic import BaseModel
from datetime import datetime

class ShortUrlStatsDto(BaseModel):
    originalUrl: str
    visits: int
    lastTimeUsed: datetime
    createdAt: datetime