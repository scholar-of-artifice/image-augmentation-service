import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.config import settings

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
def db_session(engine):
    """
        --- FIXTURE FOR TESTING DATABASE MODELS ---
        Provides a SQLAlchemy session to the test database.
        This fixture will be created once per test session.
    """
    # Create the tables if they don't exist
    SQLModel.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
    # Drop all tables after the test session is done
    SQLModel.metadata.drop_all(bind=engine)