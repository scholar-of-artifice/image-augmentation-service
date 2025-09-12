# How to try the application

In order to run this application you will need to install Docker.
The Dockerfile will build the application using the code from the repository.
The docker-compose file will get all of the required components and assemble them in a logical way.

## Prerequisites

### .env
I have included a `.env.example` file. Docker will source important variables for connecting the database from here.
Please:
- make a copy of this file
- remove the `.example` extension from the filename
- insert your own value where it says: `# replace_with_your_own_information`

#### Important Note
Never commit your `.env` file.

### Docker
This application runs using Docker containers!
site: https://www.docker.com
Follow the installation instructions for your system.

#### Docker Commands
To run the application use the following command:
```
docker compose up
```
To stop the application use the following command:
```
docker compose down
```


### Try the API
The application uses FastAPI as a core dependency.
FastAPI provides an interactive page to try out the API right out of the box.

reference: https://fastapi.tiangolo.com/tutorial/first-steps/#check-it

You just need to run the application.
When the application is running, you just need to go to the following URL:
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
    