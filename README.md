# FastAPI AI-Optimized Enterprise Backend Template

[![Docker Validation](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/docker-compose-test.yml/badge.svg?branch=develop)](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/docker-compose-test.yml)
[![Backend Code Quality](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-fastapi-backend-template.yml/badge.svg?branch=develop)](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-fastapi-backend-template.yml)
[![Coverage](coverage.svg)](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-coverage.yml)

A production-ready foundation for scalable web applications leveraging **FastAPI**, **SQLModel**, and **Alembic**. This template is engineered for high-performance Python 3.14+ environments, utilizing **uv** for deterministic dependency management and **Docker Compose** for full-stack orchestration.

## 🌟 Key Features

*   **AI-Driven Development**: Optimized for **Codex** and **Gemini CLI** assisted engineering, refactoring, code review, and feature implementation.
*   **Python 3.14+ Runtime**: Leverages the latest interpreter performance enhancements.
*   **Enterprise Observability**: Structured JSON logging with **Structlog** and real-time metrics with **Prometheus**.
*   **API Standardization**: Integrated **Pagination** for uniform list responses and **Rate Limiting** via SlowAPI.
*   **Modern Dependency Management**: Powered by [uv](https://astral.sh) for lightning-fast, reproducible builds.
*   **Full-Stack Orchestration**: Integrated **PostgreSQL 18**, **Traefik**, and development-only admin/email tooling.
*   **Enterprise Security**: Centralised OAuth2, JWT implementation, Argon2-based hashing, and automated **Security Scanning** via Bandit.
*   **Robust Health Monitoring**: Integrated Docker health checks ensuring zero-downtime dependency readiness.

## 🛠️ Tech Stack

### 🏗️ Core Architecture
- 🐍 **Python 3.14+** — Latest high-performance interpreter with advanced language features.
- ⚡ **FastAPI** — High-performance, production-ready web framework for building APIs.
- 📐 **Pydantic v2** — Modern data validation and settings management using type hints.
- 🔢 **FastAPI-Pagination** — Uniform pagination support for clean and consistent list responses.

### 🗄️ Persistence & Data
- 🐘 **PostgreSQL 18** — The world's most advanced open-source relational database.
- 🧬 **SQLModel** — Elegant unification of SQLAlchemy and Pydantic for data modeling.
- 🛠️ **Alembic** — Robust database migration management for versioned schema updates.
- 🔌 **psycopg3** — Modern, high-performance PostgreSQL adapter for Python.

### 🛡️ Security & Health
- 🔑 **OAuth2 + JWT** — Industry-standard secure authentication and authorization.
- 🔒 **Argon2** — State-of-the-art password hashing for maximum credential security.
- 🚦 **SlowAPI** — Advanced rate limiting to protect endpoints from automated abuse.
- 🛡️ **Bandit** — Automated security linting to identify and mitigate vulnerabilities.

### 📊 Observability & Resilience
- 🪵 **Structlog** — High-performance structured logging for deep system visibility.
- 📈 **Prometheus** — Real-time metrics instrumentation for monitoring system health.
- 🎯 **Sentry SDK** — Proactive error tracking and performance monitoring.
- 🔄 **Tenacity** — Sophisticated retry logic for handling transient operational failures.

### 📧 Email & Templating
- ✉️ **Emails** — Simplifies sending emails with custom headers and attachments.
- 🎨 **Jinja2** — Modern and designer-friendly templating engine for Python.
- 🔍 **Email-Validator** — Robust validation for email addresses to ensure data integrity.

### 🛠️ Tooling & Infrastructure
- 📦 **uv** — Next-generation, lightning-fast Python package and project manager.
- 🐳 **Docker & Compose** — Full-stack container orchestration for environmental parity.
- 🧭 **Traefik** — Local reverse proxy for stable `.test` service URLs.
- 📥 **MailCatcher** — Instant SMTP server for capturing and inspecting emails during development.
- 🦀 **Zensical** — Ultra-fast, Rust-powered documentation generator for this project.
- 🤖 **Codex** — AI coding collaborator for implementation, review, documentation, and repository maintenance.
- 🤖 **Gemini CLI** — AI-powered autonomous agent for rapid, surgical engineering.

### 🧪 Quality Assurance
- 🧪 **Pytest & Coverage** — Mature testing framework with detailed coverage reporting.
- 🧹 **Ruff** — Extremely fast, all-in-one Python linter and code formatter.
- 🔍 **Mypy** — Strict static type checking to eliminate runtime type errors.
- ⚓ **Prek** — Ultra-fast, Rust-powered Git hook manager for automated code quality checks.

## 🤖 AI-Driven Development

This project is built to work well with AI coding assistants such as **Codex** and **Gemini CLI**.

### Core Benefits:
- **Autonomous Engineering**: AI assistants can research the codebase, plan complex changes, and execute focused edits.
- **Context Awareness**: Leverages repository guidance such as `GEMINI.md`, existing code patterns, tests, and documentation to keep changes aligned with local standards.
- **Automated Validation**: Integrated workflow for running tests and linters immediately after code modifications.

To interact with this project using Gemini CLI:
```bash
# Start an interactive session
gemini

# Sandbox - restrict the CLI's access strictly to your current project directory
gemini --sandbox seatbelt

# Example directive
> "Add a new CRUD endpoint for 'Products' following the existing user pattern"
```

## 🛠️ Infrastructure & Orchestration

The project utilises a multi-container architecture managed via Docker Compose. The base `docker-compose.yaml` contains production-oriented services, while `docker-compose.override.yml` adds local development tools such as pgAdmin and MailCatcher.

### Service Architecture

| Service | Technology | Role |
| :--- | :--- | :--- |
| **Traefik** | Traefik v3 | Reverse proxy for host-based routing. Uses `traefik/dynamic.yml` in the base stack and `traefik/dynamic.local.yml` in local development. |
| **API** | FastAPI / Uvicorn | Primary application server with built-in health monitoring. |
| **DB** | PostgreSQL 18 | Relational data store with persisted volume mapping. |
| **Prestart** | Python/Alembic | Lifecycle service; executes migrations and populates initial system state. |
| **pgAdmin** | pgAdmin 4 | Development-only database administration interface from `docker-compose.override.yml`. |
| **MailCatcher** | MailCatcher | Development-only SMTP server and web interface from `docker-compose.override.yml`. |

## 📂 Project Structure

```
fastapi-backend-template/
├── .vscode/                       # Debugging env configuration (launch.json)
├── app/                           # Main Application Logic
│   ├── api/                       # API Entry points
│   │   └── v1/                    # API Versioning
│   │       ├── endpoints/         # Individual route handlers (e.g., users.py)
│   │       └── router.py          # Main router merging all v1 endpoints
│   ├── core/                      # Global configuration and security (JWT, Auth)
│   ├── crud/                      # Reusable database CRUD operations
│   ├── db/                        # Connection engine, session, and seed data
│   ├── email-templates/           # MJML/HTML templates for system emails
│   ├── models/                    # SQLModels, Tables, and DTOs (Data Transfer Objects)
│   ├── services/                  # Complex business logic and external integrations
│   └── main.py                    # FastAPI application initialization
├── alembic/                       # Database migrations and environment setup
├── docs/                          # Zensical documentation source (Markdown)
├── site/                          # Generated Zensical static documentation
├── scripts/                       # Shell scripts for deployment and startup
├── traefik/                       # Traefik file-provider route configuration
├── tests/                         # Pytest suite for unit and integration testing
├── .env                           # Environment variables (Internal)
├── .env.example                   # Template for environment variables
├── .pre-commit-config.yaml        # Prek/Pre-commit hook configuration
├── alembic.ini                    # Alembic configuration
├── docker-compose.override.yml    # Container Orchestration Manifest for dev env
├── docker-compose.yaml            # Container Orchestration Manifest
├── Dockerfile                     # Multi-stage, non-root Production Build
├── GEMINI.md                      # AI mandates and architectural context
├── pyproject.toml                 # Dependency management (uv)
├── uv.lock                        # Deterministic dependency lock file
├── zensical.toml                  # Zensical documentation configuration
└── README.md                      # Project documentation
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### 📦 uv (Fastest Python Package Manager)
This project uses **uv** for high-performance dependency management.

- **macOS/Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **More info**: [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

### 🐳 Docker & Docker Compose
Used for full-stack orchestration and environmental parity.

- **Desktop (macOS/Windows/Linux)**: [Install Docker Desktop](https://docs.docker.com/get-docker/)
- **Linux (Engine only)**: [Install Docker Engine](https://docs.docker.com/engine/install/)

## 🏁 Getting Started

### 1. Clone the Repository
```bash
git clone -b develop git@github.com:mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template
```

### 2. Environment Configuration

Update the following variables in `.env` file:

**Security & Super user**

Generate a secure SECRET_KEY for JWT tokens (e.g., using [JWT Secret Key Generator](https://jwtsecretkeygenerator.com)).
```bash
SECRET_KEY="your-generated-hs256-key"

# Superuser details
SUPER_USER_NAME="Sreeraj Sreenivasan"
SUPER_USER_EMAIL="sreeraj.dev@icloud.com"
SUPER_USER_PASSWORD="admin123"      # Password must be min. 8 characters
```

**Database Connection**

```bash
# Postgres Connection Settings
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_template_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

# The app will construct the URL as:
# postgresql+psycopg://postgres:admin@localhost:5432/fastapi_template_db
```

**Local pgAdmin settings**
```bash
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
```
These are used only when `docker-compose.override.yml` is included for local development.

### 3. Orchestration Launch

Deploy the local development stack with a single command:
```bash
docker compose up --build
```

For a base stack without development-only pgAdmin and MailCatcher services, run:
```bash
docker compose -f docker-compose.yaml up --build
```

This triggers the following automated sequence:

1. **Database Provisioning**: Postgres 18 initialises with health checks.
2. **Migration & Seeding**: The `prestart` container runs `alembic upgrade head` and `app/db/initial_data.py`.
3. **API Warm-up**: The FastAPI service starts only after `prestart` completes successfully.

**Development Note**: Migration files are synchronized between the host and container via Docker volumes.

### 4. Application Entry Points
- API Documentation: http://localhost:8000/docs
- API via Traefik: http://api.fastapi-template.test/docs
- Database Management: http://localhost:5050 or http://pgadmin.fastapi-template.test
- MailCatcher UI: http://localhost:1080 or http://mail.fastapi-template.test
- Traefik Dashboard: http://traefik.fastapi-template.test:8080
- Health Status: http://localhost:8000/health

### 5. 🛠️ Local Development
For native development, ensure you have the [uv](https://astral.sh) package manager installed:

```bash
# Sync environment and dependencies
uv sync

# Activate Prek hooks
uv run prek install

# Activate virtual environment
source .venv/bin/activate

# 1. Generate migrations (after making model changes)
uv run alembic revision --autogenerate -m "description of changes"

# 2. Execute schema migrations
uv run alembic upgrade head

# 3. Seed initial data (superuser, etc.)
uv run python app/db/initial_data.py

# 4. Start development server (Auto-reload enabled)
uv run fastapi dev
```

### 🌐 Local Access via Traefik
The local Compose override mounts `traefik/dynamic.local.yml`, which routes the API and development tools through custom `.test` domains. To access them, add the following to your `/etc/hosts` file:
```text
127.0.0.1 traefik.fastapi-template.test api.fastapi-template.test pgadmin.fastapi-template.test mail.fastapi-template.test
```
Services are then available at:
- **API**: `http://api.fastapi-template.test`
- **pgAdmin**: `http://pgadmin.fastapi-template.test`
- **Mailcatcher**: `http://mail.fastapi-template.test`
- **Traefik Dashboard**: `http://traefik.fastapi-template.test:8080`

The base Traefik config in `traefik/dynamic.yml` excludes pgAdmin and MailCatcher so those local-only services are not published when running with `docker-compose.yaml` alone.

### 6. 🧪 Quality Assurance
Maintain system integrity and code quality with the integrated toolchain:

#### 🧹 Linting & Formatting (Ruff)
```bash
# Check for linting issues
uv run ruff check .

# Automatically fix fixable issues
uv run ruff check --fix .

# Format the code
uv run ruff format .
```

#### 🔍 Static Type Checking (Mypy)
```bash
# Run strict type checking
uv run mypy .
```

#### 🛡️ Security Analysis (Bandit)
```bash
# Run security scan
uv run bandit -c pyproject.toml -r app
```

#### ✅ Test Suite
```bash
# Run unit and integration tests
uv run pytest
```

### 7. 📚 Documentation (Zensical)
The project documentation is built with **Zensical**, a high-performance, Rust-powered documentation generator.

#### Serve Documentation Locally
```bash
uv run zensical serve
```
Access the local documentation at: http://localhost:3000

#### Build Static Site
```bash
uv run zensical build
```
