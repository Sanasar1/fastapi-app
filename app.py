from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller.UrlShortenerController import router
from scheduler.OldUrlsCleaner import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not scheduler.running:
        scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(router)