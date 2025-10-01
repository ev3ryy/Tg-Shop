from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

async def init_db_session_pool(database_url: str):
    engine = create_async_engine(database_url, echo=False)

    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    return engine, AsyncSessionLocal