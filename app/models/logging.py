from pydantic import BaseModel

class LogEntry(BaseModel):
    """
        A basic LogEntry model.
    """
    # A short descriptive name for the event
    event: str
    details: str