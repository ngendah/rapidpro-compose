#!/usr/bin/env sh

export POSTGRES_PORT="${POSTGRES_PORT:-5432}"
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:$POSTGRES_PORT/${POSTGRES_DB}"

RETRIES=30
STATUS=1
until wget -q --method=HEAD $BACKEND_URL > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for $BACKEND_URL server to be ready, $RETRIES remaining attempts ..."
  RETRIES=$((RETRIES-=1))
  sleep 10
done

wget -q --method=HEAD $BACKEND_URL > /dev/null 2>&1
STATUS=$?
if [ "$STATUS" -ne 0 ]; then
  echo "celery exiting, $BACKEND_URL failed to be ready"
  exit 1
fi

poetry run celery -A temba worker --beat -l debug -Q flows,msgs,handler,celery -c 2
