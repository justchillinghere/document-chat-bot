import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, new_collection
from models.base import init_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
	logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
	)
	# Если не указать storage, то по умолчанию всё равно будет MemoryStorage
	# Но явное лучше неявного =]
	dp = Dispatcher(storage=MemoryStorage())
	bot = Bot(BOT_TOKEN)

	dp.include_router(common.router)
	dp.include_router(new_collection.router)

	await dp.start_polling(bot)


if __name__ == '__main__':
	init_db()
	asyncio.run(main())
