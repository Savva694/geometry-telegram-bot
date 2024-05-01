import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token="7004003107:AAFDoI6W3NJL9x_4fIlB9zCyO9bQ0n9AreE")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except():
        print("Бот выключен")
