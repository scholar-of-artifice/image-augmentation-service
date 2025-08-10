from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    print("Hello from root")
    message = "Hell from image-augmentation-service"
    return {"message": message}
