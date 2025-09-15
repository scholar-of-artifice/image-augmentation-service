from datetime import datetime

from pydantic import BaseModel


class LogEntry(BaseModel):
    """
        A basic LogEntry model.
    """
    # A short descriptive name for the event
    date_time: datetime
    event: str
    details: str