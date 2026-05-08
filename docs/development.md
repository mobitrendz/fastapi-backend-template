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

## ⚙️ Environment Configuration

To set up your local environment, copy the example configuration file:

```bash
cp .env.example .env
```

You must update the following variables in your `.env` file:

### Security & Superuser
Generate a secure `SECRET_KEY` for JWT tokens (e.g., using a [JWT Secret Key Generator](https://jwtsecretkeygenerator.com)).
```bash
SECRET_KEY="your-generated-hs256-key"

# Superuser details
SUPER_USER_NAME="Admin User"
SUPER_USER_EMAIL="admin@example.com"
SUPER_USER_PASSWORD="adminpassword" # Password must be at least 8 characters
```

### Database Connection
```bash
# Postgres Connection Settings
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_template_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

# The app constructs the URL as:
# postgresql+psycopg://postgres:admin@localhost:5432/fastapi_template_db
```

### Local pgAdmin settings
```bash
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
```
*Note: These are used only when running with `docker-compose.override.yml` for local development.*

---

## 🚀 Running the API Locally

### Start Native Development Server (Hybrid Setup)
For developers who prefer running the database services via Docker while developing the FastAPI application natively on their host machine for faster iteration:

1. **Start Database Services only**:
   ```bash
   docker compose up -d db pgadmin mailcatcher
   ```

2. **Configure Local Environment**:
   Ensure your `.env` connects to the local Docker ports (e.g., `POSTGRES_SERVER=localhost` and `POSTGRES_PORT=5432`).

3. **Run API Natively**:
   ```bash
   # Sync environment and dependencies
   uv sync

   # Activate virtual environment
   source .venv/bin/activate

   # Start development server (Auto-reload enabled)
   uv run fastapi dev
   ```
   The API will be available at:
   - **API Documentation**: `http://localhost:8000/docs`
   - **pgAdmin**: `http://localhost:5050`
   - **MailCatcher UI**: `http://localhost:1080`
   - **Prometheus Metrics**: `http://localhost:8000/metrics`
   - **Health Status**: `http://localhost:8000/health`

   These endpoints will communicate with the PostgreSQL instance running inside Docker.

### Start Full Docker Development Stack
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

We use **Pytest** for our testing suite, enhanced with **Testcontainers** for isolated infrastructure and **Hypothesis** for property-based testing.

### Run All Tests
```bash
uv run pytest
```

### Run with Coverage
```bash
uv run pytest --cov=app --cov-report=term-missing
```

### Property-based Testing (Hypothesis)
We use Hypothesis to generate edge-case data for our core utilities and validation logic.
```bash
uv run pytest tests/test_hypothesis.py
```
*Note: Testcontainers will automatically spin up a clean PostgreSQL instance for your tests when needed.*

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

## 🧹 Linting & Formatting (Ruff)

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

## ⚓ Automated Code Quality (Prek)

We use **Prek** (a Rust-powered Git hook manager) to automate code quality and security checks before every commit. These hooks enforce linting, type checking, and security standards automatically.

### Install Git Hooks
You must install the hooks locally to enable the automation:
```bash
uv run prek install
```

### Run Hooks Manually
You can run all configured quality checks manually at any time:
```bash
uv run prek run --all-files
```
*Note: This command will execute Ruff, Mypy, Bandit, and Zensical build checks.*

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

## 📈 Observability & Monitoring

This project features enterprise-grade observability to monitor, debug, and optimize your API in real-time.

### Prometheus Metrics
We use the `prometheus-fastapi-instrumentator` to automatically collect and expose performance metrics for your FastAPI application.

#### Accessing Metrics
The metrics are automatically exposed by the application at:
- **Endpoint**: `http://localhost:8000/metrics`

You can configure your Prometheus server to scrape this endpoint to generate real-time monitoring dashboards (e.g., in Grafana) to track:
- Request latency.
- Request counts by status code.
- Endpoint-specific performance.

### Structured Logging (Structlog)
Standard Python logging has been replaced with **Structlog** to provide machine-readable, structured JSON logs.

#### Why Structured Logging?
- **Searchability**: Easily filter logs by specific keys (e.g., `event`, `level`, `timestamp`).
- **Observability**: Integrates seamlessly with log aggregation services (like ELK stack or Datadog) for centralized monitoring.

*For more information on logging configuration, see `app/core/logger.py`.*

### Error Tracking (Sentry)
This project integrates [Sentry](https://sentry.io/) for proactive error tracking and performance monitoring, utilizing the native FastAPI integration for enhanced trace fidelity.

#### Configuration
To enable Sentry, you need to provide your Sentry DSN (Data Source Name).

1. **Get your DSN**:
   - Log in to your [Sentry Dashboard](https://sentry.io/).
   - Create a project in your Sentry dashboard.
   - Find your DSN under **Settings > Projects > [Your Project] > Client Keys (DSN)**.

2. **Update Environment Variable**:
   Add your DSN to the `.env` file:
   ```bash
   SENTRY_DSN="https://your-key@sentry.io/your-project-id"
   ```

3. **Restart Application**:
   Once the environment variable is set, the Sentry SDK will automatically initialize on startup and begin capturing unhandled exceptions.

*Note: If `SENTRY_DSN` is not provided, the Sentry SDK will remain inactive, ensuring no errors are logged to the service during local development.*
