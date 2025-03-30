from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from entity.ShortUrl import ShortUrl
from fastapi import HTTPException
import datetime
from sqlalchemy import and_

class UrlShortenerRepository:

    def save(self, shortUrl: ShortUrl, db: Session):
        existing = db.query(ShortUrl).filter(ShortUrl.shortUrl == shortUrl.shortUrl).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Alias '{shortUrl.shortUrl}' already exists"
            )
            
        try:
            db.add(shortUrl)
            db.commit()
            db.refresh(shortUrl)
            return shortUrl
        except IntegrityError:
            db.rollback()
            return None

    def update(self, shortUrl: ShortUrl, db: Session):
        try:
            db.add(shortUrl)
            db.commit()
            db.refresh(shortUrl)
            return shortUrl
        except IntegrityError:
            db.rollback()
            return None

    def update_short_url(self, short_url: str, new_original_url: str, db: Session):
        db_entry = db.query(ShortUrl).filter(ShortUrl.shortUrl == short_url).first()
        
        if db_entry:
            db_entry.longUrl = new_original_url
            db.commit()
            db.refresh(db_entry)
            return db_entry
        else:
            return None

    def delete_short_url(self, short_url: str, db: Session):
        db_entry = db.query(ShortUrl).filter(ShortUrl.shortUrl == short_url).first()
        if db_entry:
            db.delete(db_entry)
            db.commit()
            return db_entry
        return None

    def get(self, short_url: str, db: Session):
        return db.query(ShortUrl).filter(ShortUrl.shortUrl == short_url).first()
    
    def delete_expired(self, db: Session) -> int:
        now = datetime.utcnow()
        expired = db.query(ShortUrl).filter(
            and_(
                ShortUrl.expiresAt.isnot(None),
                ShortUrl.expiresAt <= now
            )
        ).all()
        
        count = len(expired)
        for entry in expired:
            db.delete(entry)
        db.commit()
        return count