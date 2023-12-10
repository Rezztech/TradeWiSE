FROM python:3.8-slim
WORKDIR /tests

# Copy only what is needed for installing dependencies
COPY requirements.txt /tests/
RUN pip install -r requirements.txt

# Copy your test scripts
COPY . /tests

# Set the command to run tests
CMD ["pytest"]

