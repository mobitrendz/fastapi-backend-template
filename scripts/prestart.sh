#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running Alembic Migrations..."

# 1. Generate the initial migration (if it doesn't exist)
# -m "init tables"
alembic revision --autogenerate -m "init tables" || echo "Migration already exists or failed to generate"

# 2. Apply migrations to the database
alembic upgrade head

echo "Migrations complete. Starting FastAPI..."