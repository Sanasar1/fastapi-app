from pydantic import BaseModel

class LongUrlDto(BaseModel):
    url: str