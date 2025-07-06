#!/usr/bin/env sh

# Set default PostgreSQL port if not provided
: "${POSTGRES_PORT:=5432}"

# Ensure required environment variables are set
: "${POSTGRES_USER:?POSTGRES_USER not set}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set}"
: "${POSTGRES_HOST:?POSTGRES_HOST not set}"
: "${POSTGRES_DB:?POSTGRES_DB not set}"
: "${BACKEND_URL:?BACKEND_URL not set}"

# Compose the DATABASE_URL
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Wait for BACKEND_URL to be reachable
MAX_RETRIES=30
RETRIES=$MAX_RETRIES

while ! wget -q --method=HEAD "$BACKEND_URL" > /dev/null 2>&1 && [ "$RETRIES" -gt 0 ]; do
  echo "⏳ Waiting for $BACKEND_URL to be ready, $RETRIES attempts remaining..."
  RETRIES=$((RETRIES - 1))
  sleep 10
done

# Final check after loop
if ! wget -q --method=HEAD "$BACKEND_URL" > /dev/null 2>&1; then
  echo "❌ Celery exiting: $BACKEND_URL failed to become ready after $MAX_RETRIES attempts."
  exit 1
else
  echo "✅ $BACKEND_URL is ready!"
fi

# Start Celery worker
exec poetry run celery -A temba worker --beat -l debug -Q flows,msgs,handler,celery -c 2
