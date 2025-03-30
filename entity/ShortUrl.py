from sqlalchemy import Column, Integer, String, DateTime, func
from config.database.database import Base

class ShortUrl(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    shortUrl = Column(String, name="short_url", nullable=False, unique=True)
    longUrl = Column(String, name="long_url", nullable=False)
    timesVisited = Column(Integer, name="times_visited", default=0, nullable=False)
    createdAt = Column(DateTime, name="created_at", server_default=func.now(), nullable=False)
    lastVisited = Column(DateTime, name="last_visited", server_default=func.now(), nullable=False)
    expiresAt = Column(DateTime, name="expires_at", nullable=True)
    
    def __init__(self, shortUrl: str, longUrl: str):
        self.shortUrl = shortUrl
        self.longUrl = longUrl
        self.timesVisited = 0
        self.createdAt = func.now()
        self.lastVisited = func.now()