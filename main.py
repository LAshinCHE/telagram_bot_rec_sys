import asyncio
import logging

from app.factory.bot import create_bot, create_dispatcher
from app.config import config

async def main():
    logging.basicConfig(level=config.log_level)

    bot = create_bot()
    dp = create_dispatcher()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
