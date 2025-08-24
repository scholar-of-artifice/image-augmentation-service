from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
        Application settings, loaded from the environment variables.
    """
    # where are unprocessed images stored?
    UNPROCESSED_IMAGE_PATH: Path = Path("/image-augmentation-service/data/images/unprocessed")
    # where are processed images stored?
    PROCESSED_IMAGE_PATH: Path = Path("/image-augmentation-service/data/images/processed")
    # This tells Pydantic to be case-insensitive when matching environment variables
    model_config = SettingsConfigDict(case_sensitive=False)

settings = Settings()