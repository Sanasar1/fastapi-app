import base64
from dto.ShortUrlCreateDto import ShortUrlCreateDto
from dto.ShortUrlDto import ShortUrlDto
from dto.LongUrlDto import LongUrlDto
from entity.ShortUrl import ShortUrl
from entity.Sequence import get_next_sequence_value
from config.database.database import SessionLocal
from sqlalchemy.orm import Session
from mapper.UrlMapper import UrlMapper
from repository.UrlShortenerRepository import UrlShortenerRepository
from repository.UrlShortenerRedisRepository import UrlShortenerRedisRepository
from sqlalchemy import func

class UrlShortenerService:
    
    def __init__(self):  
        self.urlMapper = UrlMapper()
        self.urlShortenerRepository = UrlShortenerRepository()
        self.urlShortenerRedisRepository = UrlShortenerRedisRepository()
    
    def shorten(self, longUrlDto: ShortUrlCreateDto) -> ShortUrlDto:
        db = SessionLocal()
        alias = longUrlDto.alias if longUrlDto.alias else self.create_alias(db)
        shortUrl = ShortUrl(alias, longUrlDto.url)
        
        self.urlShortenerRepository.save(shortUrl, db)
        self.urlShortenerRedisRepository.save(shortUrl)
        
        db.close()
        
        return self.urlMapper.toShortUrlDto(shortUrl)

    def update_long_url(self, long_url_dto: LongUrlDto, short_url):
        db = SessionLocal()
        short_url = self.urlShortenerRepository.update_short_url(short_url, long_url_dto.url, db)
        self.urlShortenerRedisRepository.save(short_url)
        db.close()
        return self.urlMapper.toLongUrlDto(short_url)
    
    def get_full_url(self, short_url: str) -> LongUrlDto:
        shortUrl = self.get_short_url(short_url)
        return self.urlMapper.toLongUrlDto(shortUrl)

    def delete_by_short_url(self, short_url: str):
        db = SessionLocal()
        short_url_dto = self.urlShortenerRepository.delete_short_url(short_url, db)
        self.urlShortenerRedisRepository.delete(short_url)
        db.close()
        return self.urlMapper.toLongUrlDto(short_url_dto)

    def get_short_url_stats(self, short_url: str):
        shortUrl = self.get_short_url(short_url)
        return self.urlMapper.toShortUrlStatsDto(shortUrl)
        
    def get_short_url(self, short_url: str) -> ShortUrl:
        db = SessionLocal()
        shortUrl = self.urlShortenerRedisRepository.get(short_url)
        if shortUrl is None:
            shortUrl = self.urlShortenerRepository.get(short_url, db)
            
        shortUrl.timesVisited += 1
        shortUrl.lastVisited = func.now()
        self.urlShortenerRepository.update(shortUrl, db)
        self.urlShortenerRedisRepository.save(shortUrl)
        
        db.close()
        
        return shortUrl
        
    def create_alias(self, db: Session) -> str:
        sequence = get_next_sequence_value(db)
        sequence_bytes = sequence.to_bytes((sequence.bit_length() + 7) // 8, 'big')
        encoded = base64.urlsafe_b64encode(sequence_bytes).decode('utf-8')
        
        base_str = encoded.rstrip('=')[:7]
        
        padded = base_str.ljust(7, '0')
        
        return padded