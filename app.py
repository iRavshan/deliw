import asyncio
from aiogram import Router
from loader import dp, bot
from handlers.user import base, ordering
from data.models import migrate_data

async def main() -> None:
    dp.include_router(base.router)
    dp.include_router(ordering.router)
    migrate_data()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
