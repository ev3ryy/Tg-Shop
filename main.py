import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config.settings import settings
from database.setup import init_db_session_pool
from middlewares.db_session import DbSessionMiddleware
from handlers import start, catalog, balance
from database.models import Base
from database.orm import ShopORM
from database.models import Product

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    engine, session_pool = await init_db_session_pool(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_pool() as session:
        orm = ShopORM(session)
        if not await orm.get_all_products():
            session.add_all([
                Product(name="Товар 1", description="Описание товара 1", price=98.00),
                Product(name="Товар 2", description="Описание товара 2", price=199.99),
                Product(name="Товар 3", description="Описание товара 3", price=29.37)
            ])
            await session.commit()
            logging.info("Тестовые товары успешно добавлены в БД.")

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool))

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(balance.router)

    logging.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logging.info("Bot Stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")