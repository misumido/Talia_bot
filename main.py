from aiogram import Bot, Dispatcher
import asyncio
from bot import bot_router
from admin import admin_router
from database import Base, engine
from configs import TELEGRAM_API_TOKEN
# TODO токен
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher()
Base.metadata.create_all(bind=engine)

async def main():
    dp.include_router(admin_router)
    dp.include_router(bot_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())