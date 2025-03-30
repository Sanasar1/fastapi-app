from pydantic import BaseModel

class ShortUrlDto(BaseModel):
    url: str