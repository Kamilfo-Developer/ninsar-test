import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.enums import ParseMode

from bot.bot.handlers import dp
from bot.bot.settings import app_settings


async def main():
    bot = Bot(app_settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
