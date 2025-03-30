from apscheduler.schedulers.background import BackgroundScheduler
from config.database.database import SessionLocal
from repository.UrlShortenerRepository import UrlShortenerRepository
import pytz

scheduler = BackgroundScheduler()
repo = UrlShortenerRepository()

def scheduled_delete_expired():
    with SessionLocal() as db:
        repo.delete_expired(db)

scheduler.add_job(scheduled_delete_expired, "interval", days=1, timezone=pytz.UTC)
scheduler.start()