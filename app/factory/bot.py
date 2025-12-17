from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import settings


def create_bot() -> Bot:
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        parse_mode=ParseMode.HTML,
    )


def create_dispatcher() -> Dispatcher:
    return Dispatcher()
