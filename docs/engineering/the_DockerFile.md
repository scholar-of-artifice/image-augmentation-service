# The `Dockerfile`

In this article, you will learn:
- What a Dockerfile is.
- Why it is essential for modern software development.
- How the Dockerfile is structured.
- How to interpret common commands in a `Dockerfile`

By the end of this article, you should be able to understand the Dockerfile(s) in this repository.

## What is a `Dockerfile`?

A Dockerfile is a plain text file that contains a set of instructions on how to build a Docker image.
Think of it as a recipe for your application's environment.
Just like a recipe lists all the ingredients (e.g., a specific version of Python, system libraries) and steps (e.g., copy files, install dependencies, run a command) needed to make a cake, a Dockerfile lists everything needed to create a containerized version of your application.

Docker reads these instructions sequentially to create a final, runnable image that packages your application, its dependencies, and the necessary runtime environment into a single, isolated unit.

## Why do I need a `Dockerfile`?

You need a Dockerfile to solve one of the most common problems in software engineering: "it works on my machine."
It provides a standardized, automated, and portable way to set up an application's environment.

### Consistency & Reproducibility

A Dockerfile guarantees that the environment is identical everywhere (on a developer's laptop, on a testing server, or in production).
The use of a container eliminates inconsistencies between different setups.

### Automation

Docker automates the entire setup process.
Instead of manually installing software, configuring files, and setting environment variables, you just define it once in the file and let Docker handle the rest.

### Portability

Because the Dockerfile creates a self-contained image, your application can run on any system that has Docker installed, regardless of the underlying operating system.
Your running container will have all the required dependencies to run your application or tests without the need to install further items on your host machine. 

### Version Control

Since it's just a text file, you can track it in version control systems like Git.
This allows you to see the history of your environment's configuration, roll back changes, and collaborate with your team effectively.

## How is the `Dockerfile` structured?

A Dockerfile is structured as a sequence of instructions, where each instruction creates a new layer in the Docker image.
This layered approach is very efficient for building and distributing images.
The basic definition of a layer is simple:
```
    INSTRUCTION arguments
```

#### References

Here is where you can find more information.

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Learn Docker in 7 Easy Steps - Full Beginner's Tutorial](https://www.youtube.com/watch?v=gAkwW2tuIqE&t=160s)

In the following headings, you will find an explanation of common instructions.
I have also defined how some of these instructions are used in the Dockerfile(s) in this repo.

### `FROM`

This must be the first instruction.
It specifies the base image to build upon.

#### Example
```Dockerfile
FROM python:3.13.7-slim
```
This starts your build from a pre-made, lightweight Python 3.13 image.
You can change this to use a different image if you want.
Generally, a smaller image is used in order to keep the memory requirements of the container smaller.

### `AS`

The `AS` keyword is used in a `FROM` instruction to give a build stage a name.
This is the cornerstone of creating multi-stage builds.

#### Example
```Dockerfile
# Specifies the official lightweight Python image as the base for our container.
FROM python:${PYTHON_VERSION}-slim AS base
```

By naming a stage, such as `base` in the example above, you can refer to it in later instructions.
This is most commonly seen in two scenarios:

1. Building upon a previous stage:
   - A new stage can use a previously named stage as its foundation, inheriting everything from it.
   - This is useful for creating a common base for different environments (like `dev` and `prod`).
2. Copying artifacts from a previous stage:
   - The `COPY --from` instruction can selectively copy files or directories from a named stage into the current stage.
   - This allows you to compile code or install build-time dependencies in an earlier stage, and then copy only the necessary compiled application into a clean final stage, resulting in a much smaller production image.

### `ARG`

The `ARG` instruction defines a build-time variable.
This is a variable that can be passed to the Docker builder at the time you run the docker build command.

Think of it as a parameter for your build recipe.
It allows you to make your `Dockerfile` more flexible without having to edit its contents directly.

#### Example
```Dockerfile
# Sets a build-time variable for the Python version, making it easy to update.
ARG PYTHON_VERSION=3.13.7
# Specifies the official lightweight Python image as the base for our container.
FROM python:${PYTHON_VERSION}-slim
```
This means we will use `python:3.13.7-slim`.

#### Override
You can override the default value from the command line using the `--build-arg` flag:

```terminaloutput
docker build --build-arg PYTHON_VERSION=3.12 .
```

#### Scope

An `ARG` variable is only available during the build process of a single stage.
It is defined from the line of its declaration until the next `FROM` instruction.
If you need to use the same `ARG` in a subsequent stage of a multi-stage build, you must declare it again.

### `WORKDIR`

Sets the working directory for any subsequent `RUN`, `CMD`, `COPY`, and `ADD` instructions.
It's like running the `cd` command inside a Linux operating system.

### `COPY`

Copies files and directories from your local machine into the container's filesystem.

#### Example
```Dockerfile
# Copy the project into the image
COPY ./app /image-augmentation-service/app
```

### `RUN`

Executes a command during the image build process.
This is typically used to install system packages or Python libraries.

#### Example
```Dockerfile
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --all-extras
```

### `ENV`

Sets persistent environment variables inside the container.

#### Example
```Dockerfile
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
```

### `CMD`

Provides the default command to execute when a container is started from the image.
There can only be one `CMD` instruction in a file.
This default command will be overridden:
- if you provide a different command when using `docker run` 
- by specifying a command in a` docker-compose.yml` file


