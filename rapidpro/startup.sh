#!/usr/bin/env sh

# set -ex

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
	set +x
	echo "*:*:*:*:$(echo \"$DATABASE_URL\" | cut -d'@' -f1 | cut -d':' -f3)" > $HOME/.pgpass
	set -x
	chmod 0600 $HOME/.pgpass
	python manage.py dbshell < init_db.sql
	rm $HOME/.pgpass
fi
if [ "x$MANAGEPY_MIGRATE" = "xon" ]; then
	python manage.py migrate
fi
if [ "x$MANAGEPY_IMPORT_GEOJSON" = "xon" ]; then
	echo "Downloading geojson for relation_ids $OSM_RELATION_IDS"
	python manage.py download_geojson $OSM_RELATION_IDS
	python manage.py import_geojson ./geojson/*.json
	echo "Imported geojson for relation_ids $OSM_RELATION_IDS"
fi

TYPE=${BOXTYPE:-rapidpro}
if [ "$TYPE" == "celery-base" ]; then
    exec celery --beat --app=temba worker --loglevel=$LOG_LEVEL --queues=celery,flows
elif [ "$TYPE" == "celery-msgs" ]; then
    exec celery --beat --app=temba worker --loglevel=$LOG_LEVEL --queues=msgs,handler
elif [ "$TYPE" == "rapidpro" ]; then
    exec python manage.py runserver 0.0.0.0:8000
fi
