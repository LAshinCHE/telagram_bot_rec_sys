import asyncio

from fastapi import FastAPI
from aiogram import Bot, Dispatcher

from app.api.router import api_router
from app.telegram.handlers import start, recommendations
from app.settings import settings
from app.db.database import engine, Base


app = FastAPI(title="Places API")
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

    print("Starting Telegram bot...")
    asyncio.create_task(start_bot())


async def start_bot():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(recommendations.router)

    await dp.start_polling(bot)

