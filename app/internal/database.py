from sqlmodel import create_engine, SQLModel, Session
from ..config import settings

# Use the validated DATABASE_URL directly from settings
# Pydantic handles the os.getenv() part for you
engine = create_engine(str(settings.DATABASE_URL), echo=True)

def create_db_and_tables():
    """
        Creates the database and tables.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
        Creates a new database session and returns the session.
    """
    with Session(engine) as session:
        yield session