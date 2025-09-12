from fastapi import FastAPI
from pathlib import Path
import logging.config
import json
from app.db.database import create_db_and_tables
from app.routers import image, health, user
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("creating database and tables...")
    create_db_and_tables()
    yield
    print('application shutdown.')

def set_up_logging():
    config_file = Path(__file__).parent / "logging_config.json"
    with config_file.open(mode='r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

set_up_logging()
app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)

app.include_router(image.router, prefix="/image-api")
app.include_router(health.router, prefix="/healthcheck-api")
app.include_router(user.router, prefix="/users-api")

