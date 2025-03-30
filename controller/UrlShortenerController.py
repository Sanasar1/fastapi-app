from dto.ShortUrlCreateDto import ShortUrlCreateDto
from dto.LongUrlDto import LongUrlDto
from dto.ShortUrlDto import ShortUrlDto
from dto.ShortUrlStatsDto import ShortUrlStatsDto
from service.UrlShortenerService import UrlShortenerService
from fastapi import APIRouter, status

router = APIRouter()

urlShortenerService = UrlShortenerService()

@router.post("/links/shorten")
async def shorten(longUrlDto: ShortUrlCreateDto, status_code=status.HTTP_201_CREATED) -> ShortUrlDto:
    return urlShortenerService.shorten(longUrlDto)

@router.get("/links/{short_url}")
async def get_full_url(short_url: str) -> LongUrlDto:
    return urlShortenerService.get_full_url(short_url)

@router.get("/links/{short_url}/stats")
async def get_short_url_stats(short_url: str) -> ShortUrlStatsDto:
    return urlShortenerService.get_short_url_stats(short_url)

@router.delete("/links/{short_url}")
async def delete_by_short_url(short_url: str) -> LongUrlDto:
    return urlShortenerService.delete_by_short_url(short_url)
    
@router.put("/links/{short_url}")
async def update_long_url(long_url_dto: LongUrlDto, short_url: str) -> LongUrlDto:
    return urlShortenerService.update_long_url(long_url_dto, short_url)