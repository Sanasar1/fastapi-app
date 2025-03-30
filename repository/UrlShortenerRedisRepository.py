from config.redis.redis import get_redis_client
from entity.ShortUrl import ShortUrl
import pickle

class UrlShortenerRedisRepository:
    TIME_TO_LIVE = 60 * 60 * 24
    
    def __init__(self):
        self.redis = get_redis_client()
        
    def save(self, short_url: ShortUrl):
        serialized = pickle.dumps(short_url)
        self.redis.set(short_url.shortUrl, serialized)
        self.redis.expire(short_url.shortUrl, self.TIME_TO_LIVE)
        
    def get(self, short_url: str) -> ShortUrl | None:
        shortUrl = self.redis.get(short_url)
        if shortUrl is None:
            return None
        return pickle.loads(shortUrl)
    
    def delete(self, short_url: str):
        self.redis.delete(short_url)