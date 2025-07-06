#!/usr/bin/env sh

export MAILROOM_ADDRESS=0.0.0.0
export MAILROOM_DB="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@$POSTGRES_HOST:$POSTGRES_PORT/${POSTGRES_DB}?sslmode=disable"

exec ./mailroom
