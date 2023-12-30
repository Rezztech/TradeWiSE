#!/bin/sh

export KEYRING_ENCRYPTION_KEY=$(python -c "from secrets import token_urlsafe; print(token_urlsafe(32))")

# Remove the --reload flag in production
uvicorn main:app --host 0.0.0.0 --port 80 --reload
