#!/usr/bin/env sh

export POSTGRES_PORT="${POSTGRES_PORT:-5432}"
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:$POSTGRES_PORT/${POSTGRES_DB}"

RETRIES=10
PASSFILE=$HOME/.pgpass
echo "*:*:*:$POSTGRES_USER:$POSTGRES_PASSWORD" > $PASSFILE
chmod 0600 $PASSFILE
until PGPASSFILE=$PASSFILE psql -lqt -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $RETRIES remaining attempts ..."
  RETRIES=$((RETRIES-=1))
  sleep 5
done

PGPASSFILE=$PASSFILE psql -lqt -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER > /dev/null 2>&1
DB_CONN_STATUS=$?
if [ "$DB_CONN_STATUS" -ne 0 ]; then
  echo "unable to connect to the database"
  exit 1
fi

DB_EXISTS="$(PGPASSFILE=$PASSFILE psql -lqt -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER | cut -d\| -f1 | grep -w "\b$POSTGRES_DB\b")"
if [ "$DB_EXISTS" != "$POSTGRES_DB" ]; then
  echo "Creating database $POSTGRES_DB"
  PGPASSFILE=$PASSFILE psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"
fi

echo "running migrations, might take a while ..."
poetry run ./manage.py migrate

echo "creating admin user ..."
poetry run ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser(\"$ADMIN_USERNAME\", \"$ADMIN_EMAIL\", \"$ADMIN_PASSWORD\")"

poetry run ./manage.py runserver 0.0.0.0:8000
