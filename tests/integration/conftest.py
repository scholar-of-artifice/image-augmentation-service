import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from app.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_session
from httpx import AsyncClient, ASGITransport


# --- SYNCHRONOUS FIXTURES ---


@pytest.fixture(scope="session")
def engine():
    """
    Creates a SQLAlchemy engine instance
    """
    return create_engine(str(settings.DATABASE_URL))


@pytest.fixture(scope="session")
def setup_database(engine):
    """
    Create and drop all tables once for the entire test session.
    """
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(engine, setup_database):
    """
    --- FIXTURE FOR TESTING DATABASE MODELS ---
    Provides a SQLAlchemy session to the test database.
    This fixture will be created once per test function.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        if transaction.is_active:
            transaction.rollback()
        session.close()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    --- FIXTURE FOR TESTING API ---
    A fixture that provides a TestClient with a transactional database session.
    """

    def override_get_session():
        """
        A dependency override that provides a session for one test.
        """
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    return


# --- ASYNCHRONOUS FIXTURES ---


@pytest_asyncio.fixture(scope="session")
def async_engine():
    """
    creates an asyncio-compatible SQLAlchemy engine instance.
    """
    # use an async-compatible driver in the URL, e.g., postgresql+psycopg
    async_db_url = str(settings.DATABASE_URL).replace(
        "postgresql://", "postgresql+psycopg://"
    )
    return create_async_engine(async_db_url)


@pytest_asyncio.fixture(scope="session")
async def setup_database_async(async_engine):
    """
    Creates and drops all tables once for the entire test session.
    """
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    yield
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_db_session(async_engine, setup_database_async):
    """
    create fixture for async database operations.
    provides a transactional SQLAlchemy AsyncSession to the test database.
    this fixture will be created once per test function.
    """
    # the `sessionmaker` is configured to use the AsyncSession class
    async_session_maker = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        async with session.begin():
            try:
                yield session
            finally:
                # The transaction is automatically rolled back by the context manager
                await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session):
    """
    fixture for testing async API
    provides an AsyncClient with a transactional async database session.
    """

    async def override_get_session_async():
        """
        A dependency override that provides an async session for one test.
        """
        yield async_db_session

    app.dependency_overrides[get_session] = override_get_session_async

    transport = ASGITransport(app=app)
    # use httpx.AsyncClient for async requests
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
