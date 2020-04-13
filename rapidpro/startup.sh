#!/usr/bin/env sh

TYPE=${BOXTYPE:-rapidpro}
if [ "$TYPE" == "celery-base" ]; then
  echo "Starting $TYPE server..."
  exec celery --beat --app=temba worker --loglevel=$LOG_LEVEL --queues=celery,flows
elif [ "$TYPE" == "celery-msgs" ]; then
  echo "Starting $TYPE server..."
  exec celery --beat --app=temba worker --loglevel=$LOG_LEVEL --queues=msgs,handler
elif [ "$TYPE" == "rapidpro" ]; then
  DB_URL=$(python3 -c "from urllib.parse import urlparse; dburl=urlparse('$DATABASE_URL'); database=dburl.path.replace('/',''); port=dburl.port or '5432'; print(f'{dburl.hostname}:{port}:{database}:{dburl.username}:{dburl.password}');")

  DB_URL="$DB_URL"
  DB_HOST=$(echo $DB_URL | cut -d":" -f1)
  DB_PORT=$(echo $DB_URL | cut -d":" -f2)
  DB_NAME=$(echo $DB_URL | cut -d":" -f3)
  DB_USER=$(echo $DB_URL | cut -d":" -f4)
  DB_PASS=$(echo $DB_URL | cut -d":" -f5)

  if [ "$DB_HOST" == "$DB_URL" ]; then
    echo "Unable to parse the databse URL"
    exit 1
  fi

  PASSFILE=$HOME/.pgpass

  echo "*:*:*:$DB_USER:$DB_PASS" > $PASSFILE
  chmod 0600 $PASSFILE

  RETRIES=5

  until PGPASSFILE=$PASSFILE psql -lqt -h $DB_HOST -U $DB_USER > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
    echo "Waiting for postgres server, $RETRIES remaining attempts..."
    RETRIES=$((RETRIES-=1))
    sleep 1
  done

  DB_EXISTS="$(PGPASSFILE=$PASSFILE psql -lqt -h $DB_HOST -U $DB_USER | cut -d\| -f1 | grep -w "\b$DB_NAME\b")"

  if [ "$DB_EXISTS" != "$DB_NAME" ]; then
    echo "Creating database $DB_NAME"
    PGPASSFILE=$PASSFILE psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
  fi
  if [ "x$MANAGEPY_COLLECTSTATIC" = "xon" ]; then
    python manage.py collectstatic --noinput --no-post-process
  fi
  if [ "x$CLEAR_COMPRESSOR_CACHE" = "xon" ]; then
    python clear-compressor-cache.py
  fi
  if [ "x$MANAGEPY_COMPRESS" = "xon" ]; then
    python manage.py compress --extension=".haml" --force -v0
  fi
  if [ "x$MANAGEPY_INIT_DB" = "xon" ]; then 
    python manage.py dbshell < init_db.sql
  fi
  if [ "x$MANAGEPY_MIGRATE" = "xon" ]; then
    python manage.py migrate
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser(\"$ADMIN_USERNAME\", \"$ADMIN_EMAIL\", \"$ADMIN_PASSWORD\")"
  fi
  if [ "x$MANAGEPY_IMPORT_GEOJSON" = "xon" ]; then
    echo "Downloading geojson for relation_ids $OSM_RELATION_IDS"
    python manage.py download_geojson $OSM_RELATION_IDS
    python manage.py import_geojson ./geojson/*.json
    echo "Imported geojson for relation_ids $OSM_RELATION_IDS"
  fi
  echo "Starting $TYPE server..."
  exec python manage.py runserver 0.0.0.0:8000
fi
