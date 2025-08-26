from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, DateTime

class UnprocessedImage(SQLModel, table=True):
    """
    Class representing a unprocessed image in the database.
    """
    # which image is this?
    id: int | None = Field(default=None, primary_key=True)
    # who wrote this image?
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    # what is the original name of this image?
    original_filename: str = Field(nullable=False, max_length=40)
    # what is the uuid name of this image?
    storage_filename: str = Field(default_factory=lambda: f"{str(uuid.uuid4())}.png" , unique=True, nullable=False, max_length=40)
    # where is this image stored? This field will be populated by the logic in __post_init__
    storage_filepath: str = Field(unique=True, nullable=False, max_length=255)
    # when was this image created?
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False) # This tells SQLAlchemy to use a timezone-aware database column type
    )

@event.listens_for(UnprocessedImage, "before_insert")
def generate_storage_filepath(mapper, connection, target):
    """
        Generate the storage_filepath after the model is initialized.
    """
    # This check is useful if you ever create an instance with the path already provided
    if target.storage_filepath is None:
        target.storage_filepath = str(os.path.join(settings.UNPROCESSED_IMAGE_PATH, target.storage_filename))
