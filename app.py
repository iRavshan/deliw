import asyncio
from aiogram import Router
from loader import dp, bot, create_tables
from handlers.user import base, ordering

async def main() -> None:
    dp.include_router(base.router)
    dp.include_router(ordering.router)
    create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
