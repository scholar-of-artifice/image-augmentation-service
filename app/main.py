from fastapi import FastAPI
from pathlib import Path
import logging.config
import json
from app.routers import image, health, user

def set_up_logging():
    config_file = Path(__file__).parent / "logging_config.json"
    with config_file.open(mode='r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

set_up_logging()
app = FastAPI()
logger = logging.getLogger(__name__)

app.include_router(image.router, prefix="/image-api")
app.include_router(health.router, prefix="/healthcheck-api")
app.include_router(user.router, prefix="/users-api")

