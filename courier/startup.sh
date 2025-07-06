#!/usr/bin/env sh

# Set service address and database connection string
export COURIER_ADDRESS="0.0.0.0"
export COURIER_DB="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}?sslmode=disable"

# Wait for BACKEND_URL to become reachable
MAX_RETRIES=30
RETRIES=$MAX_RETRIES

while ! wget -q --method=HEAD "$BACKEND_URL" > /dev/null 2>&1 && [ "$RETRIES" -gt 0 ]; do
  echo "⏳ Waiting for $BACKEND_URL server... ($RETRIES retries remaining)"
  RETRIES=$((RETRIES - 1))
  sleep 10
done

# Final connection check
if wget -q --method=HEAD "$BACKEND_URL" > /dev/null 2>&1; then
  echo "✅ Connected to $BACKEND_URL"
else
  echo "❌ Courier unable to connect to $BACKEND_URL after $MAX_RETRIES attempts"
  exit 1
fi

# Start the courier service
exec ./courier

