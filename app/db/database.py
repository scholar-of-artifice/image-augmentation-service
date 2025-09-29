from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from app.config import settings

# call a function to get the application settings establish a connection to the
# ... database.
engine = create_engine(str(settings.DATABASE_URL), echo=True)


def create_db_and_tables():
    """
    Creates the database and tables.
    """
    SQLModel.metadata.create_all(engine)


# Asynchronous session

# takes the original database connection string and modifies it to create a new one
# ... that's specifically for asynchronous database operations.
async_db_url = str(settings.DATABASE_URL).replace(
    "postgresql://", # look for this string
    "postgresql+psycopg://" # replace with this string and use this driver
)

# create a new database engine specifically for asynchronous communication.
async_engine = create_async_engine(
    async_db_url,
    echo=True
)


async def get_async_session():
    """
    Creates a new async database session and returns the session.
    """
    # use the session factory to make a new asynchronous session
    async_session = sessionmaker(
        # the engine instance to use
        bind=async_engine,
        # the type of session
        class_=AsyncSession,
        # the session will close when a transaction is finished
        expire_on_commit=False
    )
    # closes the session when the block is exited
    async with async_session() as session:
        yield session # makes a session available
