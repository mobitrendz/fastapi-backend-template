#!/bin/bash
set -e

echo "Running migrations..."
python -m alembic upgrade head

echo "Seeding initial data..."
python -m app.db.initial_data

echo "Prestart complete."
