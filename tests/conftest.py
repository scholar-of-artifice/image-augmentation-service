import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.internal.database import get_session

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
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(engine):
    """
        --- FIXTURE FOR TESTING API ---
        A fixture that provides a TestClient with a transactional database session.
        This ensures each test is isolated.
    """

    SQLModel.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()

    def override_get_session():
        """
            A dependency override that provides a session for one test.
        """
        with Session(connection) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    # Clean up after the test
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()
    # Drop all tables after the test session is done
    SQLModel.metadata.drop_all(bind=engine)