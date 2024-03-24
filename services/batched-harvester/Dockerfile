# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
#COPY ./requirements.txt /app/requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml poetry.lock /app/
RUN --mount=type=cache,target=/root/.cache \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of your app's source code from your host to your image filesystem.
COPY src/ /app/

# Run bot.py when the container launches
CMD ["python", "./main.py"]

