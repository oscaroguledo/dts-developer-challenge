from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import settings

Base = declarative_base()
CHAR_LENGTH=255

DATABASE_URL = str(settings.DATABASE_URL) 
engine_db1 = create_async_engine(DATABASE_URL, echo=True)

# Session factory for the first database (Async)
AsyncSessionDB1 = sessionmaker(
    bind=engine_db1, 
    class_=AsyncSession, 
    expire_on_commit=False, 
)

# Dependency to get the async session for the first database
async def get_db1():
    try:
        async with AsyncSessionDB1() as session:
            yield session
    except Exception as e:
        # Log the error or handle it accordingly
        print(f"Database connection failed: {e}")
        raise
