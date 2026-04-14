#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/db/backend_pre_start.py

echo "--- RUNNING MIGRATIONS ---"
alembic upgrade head

# Create initial data in DB
python app/db/initial_data.py
