# --- BASE STAGE ---
# Sets a build-time variable for the Python version, making it easy to update.
ARG PYTHON_VERSION=3.13.7
# Specifies the official lightweight Python image as the base for our container.
FROM python:${PYTHON_VERSION}-slim AS base
# Adds metadata to the image, in this case, the author's name.
LABEL authors="scholar-of-artifice"
# PYTHONUNBUFFERED
# This prevents Python from buffering the output.
# It ensures that any print() statements or application logs are sent directly to the container's log stream in real-time.
# Without this, you might not see your logs until the program finishes, which makes debugging difficult.
# PYTHONDONTWRITEBYTECODE
# This tells Python not to create .pyc files.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# Change the working directory to the `image-augmentation-service` directory
WORKDIR /image-augmentation-service
# Copies the 'uv' executable from a multi-stage build to install Python packages quickly.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# --- DEV STAGE ---
FROM base AS dev
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --all-extras
# Copy the project into the image
COPY ./app /image-augmentation-service/app

# --- TEST STAGE ---
FROM dev AS test
# Copy the tests into the image
COPY ./tests /image-augmentation-service/tests

# --- END-TO-END STAGE ---
# This stage is for the container that runs the API server.
# It only needs the app code, not the tests.
# Sets a build-time variable for the Python version, making it easy to update.
ARG PYTHON_VERSION=3.13.7
# Specifies the official lightweight Python image as the base for our container.
FROM python:${PYTHON_VERSION} AS endtoend
# Adds metadata to the image, in this case, the author's name.
LABEL authors="scholar-of-artifice"
# PYTHONUNBUFFERED
# This prevents Python from buffering the output.
# It ensures that any print() statements or application logs are sent directly to the container's log stream in real-time.
# Without this, you might not see your logs until the program finishes, which makes debugging difficult.
# PYTHONDONTWRITEBYTECODE
# This tells Python not to create .pyc files.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# Change the working directory to the `image-augmentation-service` directory
WORKDIR /image-augmentation-service
# Copies the 'uv' executable from a multi-stage build to install Python packages quickly.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --all-extras
# Copy the project into the image
COPY ./app /image-augmentation-service/app

# --- PROD STAGE ---
FROM base AS prod
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
# Copy the project into the image
COPY ./app /image-augmentation-service/app
# Run with uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# TODO: Run as a Non-Root User to reduce security risks
# TODO: Use a Multi-Stage Build to create smaller, more secure final images.
# TODO: Harden the Production Server Command to handle real-world traffic.
# TODO: Modernise the uv Installer to align with current best practices.
# TODO: Add a HEALTHCHECK to allow Docker to monitor the container's status.