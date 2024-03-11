import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from database.engine import create_db
from handlers import dp

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
WB_CARD_API_URL = getenv("WB_CARD_API_URL")


async def main() -> None:
    await create_db()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
