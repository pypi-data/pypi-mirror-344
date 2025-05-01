import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DATABASE_HOST", "db")  # Default 'db' matches Docker Compose service name
DB_PORT = os.getenv("DATABASE_PORT", "5432")

# Use your actual database URL (this example uses PostgreSQL)
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

# Create the asynchronous engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session maker
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create the base class for our models
Base = declarative_base()
