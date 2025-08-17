# How to try the application

FastAPI provides an interactive page to try out the API right out of the box. You just need to run the application.

## Prerequisites
You need to have downloaded the application and get it running locally.

reference: https://fastapi.tiangolo.com/tutorial/first-steps/#check-it

Then you need to go to:
```
http://127.0.0.1:8000/docs
```

## Example
Try out the following endpoint:
```
/image-api/upload/
```

Then define the request body:
- Choose a file
- enter the following string for the `body` field:
    ```
        {"arguments": {"processing": "rotate", "angle": 45}}
    ```
    