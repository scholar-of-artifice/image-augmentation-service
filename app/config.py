from pathlib import Path
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
        Application settings, loaded from the environment variables.
    """
    # where are unprocessed images stored?
    UNPROCESSED_IMAGE_PATH: Path = Path("/image-augmentation-service/data/images/unprocessed")
    # where are processed images stored?
    PROCESSED_IMAGE_PATH: Path = Path("/image-augmentation-service/data/images/processed")
    # use a single field for the database connection string
    DATABASE_URL: PostgresDsn
    # This tells Pydantic to be case-insensitive when matching environment variables
    model_config = SettingsConfigDict(
        case_sensitive=False
    )

settings = Settings()