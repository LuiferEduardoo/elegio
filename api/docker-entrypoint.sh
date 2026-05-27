#!/bin/sh
set -e

ATTEMPTS="${MIGRATION_ATTEMPTS:-10}"
DELAY="${MIGRATION_RETRY_DELAY:-3}"

echo "[entrypoint] Applying migrations (alembic upgrade head)..."

i=1
while true; do
  if alembic upgrade head; then
    echo "[entrypoint] Migrations applied successfully."
    break
  fi
  if [ "$i" -ge "$ATTEMPTS" ]; then
    echo "[entrypoint] Migrations failed after ${i} attempts. Aborting." >&2
    exit 1
  fi
  echo "[entrypoint] Migration attempt ${i}/${ATTEMPTS} failed (DB not ready or config error); retrying in ${DELAY}s..." >&2
  i=$((i + 1))
  sleep "$DELAY"
done

echo "[entrypoint] Starting: $*"
exec "$@"
