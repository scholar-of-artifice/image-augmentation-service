from fastapi import FastAPI
from app.routers import image

app = FastAPI()
app.include_router(image.router, prefix="/image-api")


@app.get("/")
def root():
    print("Hello from root")
    message = "Hello from image-augmentation-service"
    return {"message": message}
