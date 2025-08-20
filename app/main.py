from fastapi import FastAPI
from app.routers import image, health

app = FastAPI()
app.include_router(image.router, prefix="/image-api")
app.include_router(health.router, prefix="/healthcheck-api")

