from entity.ShortUrl import ShortUrl
from dto.ShortUrlDto import ShortUrlDto
from dto.LongUrlDto import LongUrlDto
from dto.ShortUrlStatsDto import ShortUrlStatsDto

class UrlMapper:

    def toShortUrlDto(self, shortUrl: ShortUrl) -> ShortUrlDto:
        return ShortUrlDto(url=shortUrl.shortUrl)
    
    def toLongUrlDto(self, shortUrl: ShortUrl) -> LongUrlDto:
        return LongUrlDto(url=shortUrl.longUrl)
    
    def toShortUrlStatsDto(self, shortUrl: ShortUrl) -> ShortUrlStatsDto:
        return ShortUrlStatsDto(originalUrl=shortUrl.shortUrl,
                                lastTimeUsed=shortUrl.lastVisited, 
                                createdAt=shortUrl.createdAt,
                                visits=shortUrl.timesVisited)