from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

# Use the validated DATABASE_URL directly from settings
# Pydantic handles the os.getenv() part for you
engine = create_engine(str(settings.DATABASE_URL), echo=True)


def create_db_and_tables():
    """
    Creates the database and tables.
    """
    SQLModel.metadata.create_all(engine)


# Asynchronous session

async_db_url = str(settings.DATABASE_URL).replace(
    "postgresql://", "postgresql+psycopg://"
)
async_engine = create_async_engine(async_db_url, echo=True)


async def get_async_session():
    """
    Creates a new async database session and returns the session.
    """
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
