#!/usr/bin/env sh

export MAILROOM_ADDRESS=0.0.0.0
export MAILROOM_DB="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@$POSTGRES_HOST:$POSTGRES_PORT/${POSTGRES_DB}?sslmode=disable"

RETRIES=30
STATUS=1
until wget -q --method=HEAD $BACKEND_URL > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for $BACKEND_URL server, $RETRIES remaining attempts ..."
  RETRIES=$((RETRIES-=1))
  sleep 10
done

wget -q --method=HEAD $BACKEND_URL > /dev/null 2>&1
STATUS=$?
if [ "$STATUS" -ne 0 ]; then
  echo "mailroom unable to connect to $BACKEND_URL"
  exit 1
fi

exec mailroom
