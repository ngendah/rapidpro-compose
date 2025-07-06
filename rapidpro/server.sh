#!/usr/bin/env sh

# Set default port if not provided
: "${POSTGRES_PORT:=5432}"

# Construct the full database URL (optional use)
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Create a .pgpass file for non-interactive authentication
PASSFILE="$HOME/.pgpass"
echo "*:*:*:${POSTGRES_USER}:${POSTGRES_PASSWORD}" > "$PASSFILE"
chmod 0600 "$PASSFILE"

# Retry connection until successful or limit reached
RETRIES=10
until PGPASSFILE="$PASSFILE" psql -lqt -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1 || [ "$RETRIES" -eq 0 ]; do
  echo "Waiting for PostgreSQL server, $RETRIES remaining attempts..."
  RETRIES=$((RETRIES - 1))
  sleep 5
done

# Final check: can we connect?
if ! PGPASSFILE="$PASSFILE" psql -lqt -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; then
  echo "❌ Unable to connect to the PostgreSQL server."
  exit 1
fi

# Check if the target database exists
DB_EXISTS=$(PGPASSFILE="$PASSFILE" psql -lqt -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" \
  | cut -d '|' -f1 | awk '{$1=$1};1' | grep -Fx "$POSTGRES_DB")

if [ -z "$DB_EXISTS" ]; then
  echo "✅ Creating database: $POSTGRES_DB"
  PGPASSFILE="$PASSFILE" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" \
    -c "CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";"
else
  echo "✅ Database $POSTGRES_DB already exists."
fi

echo "running migrations, might take a while ..."
poetry run ./manage.py migrate

echo "Compressing assets ..."
poetry run ./manage.py collectstatic --noinput --verbosity=0

echo "creating admin user ..."
poetry run ./manage.py admin --root --username="$ADMIN_USERNAME" --email="$ADMIN_EMAIL" --password="$ADMIN_PASSWORD"
poetry run ./manage.py runserver 0.0.0.0:8000
