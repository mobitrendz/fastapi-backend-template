---
icon: lucide/code
---

# Development Guide

This guide covers everything you need to know to develop, test, and contribute to the FastAPI Backend Template.

## 🛠️ Local Environment Setup

### 1. Install `uv`
This project uses `uv` for lightning-fast dependency management.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Docker & Docker Compose
Used for full-stack orchestration and environmental parity.
- [Install Docker Desktop](https://docs.docker.com/get-docker/)

### 3. Sync & Setup Environment
```bash
# Sync dependencies
uv sync

# Install Prek hooks
uv run prek install

# Activate virtual environment
source .venv/bin/activate
```

## 🚀 Running the API Locally

### Start Native Development Server
```bash
uv run fastapi dev
```
The server will start with hot-reload enabled at http://localhost:8000.

### Start Docker Development Stack
```bash
docker compose up --build
```
Docker Compose uses `docker-compose.override.yml` by default in local development. That override adds pgAdmin, MailCatcher, hot reload, and the local Traefik route file at `traefik/dynamic.local.yml`.

#### 🌐 Local Network Access via Traefik
When using the Docker development stack, services are routed through Traefik using custom `.test` domains. To access them, ensure the following are in your `/etc/hosts` file:
```text
127.0.0.1 traefik.fastapi-template.test api.fastapi-template.test pgadmin.fastapi-template.test mail.fastapi-template.test
```
Services are then available at:
- **API**: `http://api.fastapi-template.test`
- **pgAdmin**: `http://pgadmin.fastapi-template.test`
- **Mailcatcher**: `http://mail.fastapi-template.test`
- **Traefik Dashboard**: `http://traefik.fastapi-template.test:8080`

pgAdmin and MailCatcher are local-only services. They are defined in `docker-compose.override.yml` and are not part of the base `docker-compose.yaml` stack.

## 🗄️ Database Migrations & Seeding

This project uses **Alembic** for migrations and a custom script for initial data seeding.

### 1. Generate a New Migration
Always generate migrations after making changes to your models in `app/models/`.
```bash
uv run alembic revision --autogenerate -m "describe your changes"
```
Verify the generated script in `alembic/versions/`.

### 2. Apply Migrations
```bash
uv run alembic upgrade head
```

### 3. Seed Initial Data
To create the initial superuser and system data:
```bash
uv run python app/db/initial_data.py
```

## 🧪 Testing

We use **Pytest** for our testing suite.

### Run All Tests
```bash
uv run pytest
```

### Run with Coverage
```bash
uv run pytest --cov=app --cov-report=term-missing
```

## 📧 Email Testing (MailCatcher)

For local development and testing of password recovery or other email-related features, we use **MailCatcher**.

- **SMTP Port**: `1025`
- **Web Interface**: http://localhost:1080 or http://mail.fastapi-template.test

When running via Docker Compose, the backend is configured to route emails through the `mailcatcher` service. You can view all outgoing emails in the web interface.

## 🎨 Email Templates (MJML)

Email templates are located in `app/email-templates`.
- **`src/`**: Contains MJML source files for responsive email design.
- **`build/`**: Contains the compiled HTML templates used by the application.

To add or modify templates, update the MJML files and ensure they are rendered correctly via the `render_email_template` utility in `app.core.security`.

## 🧹 Linting & Formatting

We use **Ruff** for linting and formatting.

### Run Linter
```bash
uv run ruff check .
```

### Fix Linting Errors
```bash
uv run ruff check --fix .
```

### Run Formatter
```bash
uv run ruff format .
```

## 🔍 Type Checking

We use **Mypy** for static type checking.
```bash
uv run mypy .
```

## 🛡️ Security Analysis (Bandit)

We use **Bandit** to perform automated security linting and identify potential vulnerabilities in the application code.
```bash
# Run security scan
uv run bandit -c pyproject.toml -r app
```
*Note: Bandit is also automatically executed as part of the `pre-commit` workflow.*

## 🤖 Gemini CLI

This project is optimized for AI-driven development.
```bash
# Research and modify
gemini "Add a new endpoint to list users"
```
Refer to `GEMINI.md` for project-specific AI mandates.
