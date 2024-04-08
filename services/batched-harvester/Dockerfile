# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy both the pyproject.toml and poetry.lock files to the /app
# The following RUN command does several things:
# 1. It uses the Docker BuildKit's cache mount feature to speed up the build process by caching the installation layers.
# 2. It installs Poetry via pip.
# 3. It configures Poetry to not create a virtual environment inside the Docker container.
# 4. It installs the project dependencies specified in `pyproject.toml`.
#    The `--no-dev` flag excludes development dependencies to keep the container lightweight.
#    The `--no-interaction` and `--no-ansi` flags are used to make the build output cleaner and non-interactive, 
#    which is suitable for automated build environments like CI/CD pipelines.
COPY pyproject.toml poetry.lock /app/
RUN --mount=type=cache,target=/root/.cache \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of your app's source code from your host to your image filesystem.
COPY src/ /app/

# Run bot.py when the container launches
CMD ["python", "./main.py"]

