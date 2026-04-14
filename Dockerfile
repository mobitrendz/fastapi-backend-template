# 1. Use official python 3.14 (or slim) image
FROM python:3.14-slim-bookworm

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Setup environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# 4. Install dependencies
# Using --mount=type=cache speeds up builds by caching uv packages
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 5. Copy application and .env
COPY . .

# 6. Install project itself (if package mode is enabled)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 7. Add .venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# 8. Run Alembic and Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
