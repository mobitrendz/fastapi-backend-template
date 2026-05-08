# FastAPI AI-Optimized Enterprise Backend Template

[![Docker Validation](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/docker-compose-test.yml/badge.svg?branch=develop)](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/docker-compose-test.yml)
[![Backend Code Quality](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-fastapi-backend-template.yml/badge.svg?branch=develop)](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-fastapi-backend-template.yml)
[![Coverage](coverage.svg)](https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-coverage.yml)

A production-ready FastAPI template designed for scalable, high-performance web applications. This project provides a robust, modular foundation that integrates enterprise-grade security, comprehensive observability, and automated quality assurance workflows out of the box.

## 🌟 Key Features

*   **AI-Driven Development**: Optimized for **Google Antigravity** and **Gemini CLI** assisted engineering, refactoring, code review, and feature implementation.
*   **Python 3.12+ Runtime**: Leverages the latest interpreter performance enhancements.
*   **Enterprise Observability**: Structured JSON logging with **Structlog** and real-time metrics with **Prometheus**.
*   **API Standardization**: Integrated **Pagination** for uniform list responses and **Rate Limiting** via SlowAPI.
*   **Modern Dependency Management**: Powered by [uv](https://astral.sh) for lightning-fast, reproducible builds.
*   **Full-Stack Orchestration**: Integrated **PostgreSQL 18**, **Traefik**, and development-only admin/email tooling.
*   **Enterprise Security**: Centralised OAuth2, JWT implementation, Argon2-based hashing, and automated **Security Scanning** via Bandit.
*   **Robust Health Monitoring**: Integrated Docker health checks ensuring zero-downtime dependency readiness.

## 🛠️ Tech Stack

### 🏗️ Core Architecture
- 🐍 **Python 3.12+** — Latest high-performance interpreter with advanced language features.
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
- 🤖 **Google Antigravity** — AI coding collaborator for implementation, review, documentation, and repository maintenance.
- 🤖 **Gemini CLI** — AI-powered autonomous agent for rapid, surgical engineering.

### 🧪 Quality Assurance
- 🧪 **Pytest & Coverage** — Mature testing framework with detailed coverage reporting.
- 🧹 **Ruff** — Extremely fast, all-in-one Python linter and code formatter.
- 🔍 **Mypy** — Strict static type checking to eliminate runtime type errors.
- ⚓ **Prek** — Ultra-fast, Rust-powered Git hook manager for automated code quality checks.

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
SUPER_USER_NAME="Admin User"
SUPER_USER_EMAIL="admin@example.com"
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
- Database Management: http://localhost:5050
- MailCatcher UI: http://localhost:1080
- Health Status: http://localhost:8000/health

### 5. 🛠️ Local Development
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
The project documentation is built with **Zensical**, a high-performance, Rust-powered documentation generator. It serves as the primary resource for deep-dives into our architecture, development workflows, and deployment strategies.

#### Access & Build
- **Serve Locally**: `uv run zensical serve` (Available at: http://localhost:3000)
- **Build Static Site**: `uv run zensical build`

*For an in-depth understanding of the system, please explore the full [Documentation Portal](http://localhost:3000).*

---

## 📝 Release Notes
See the full [Release Notes](release-notes.md) for a detailed history of changes.
## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 💡 Inspiration
This project is heavily inspired by the official [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) in the FastAPI repository. It builds upon those foundational concepts, incorporating modern toolchain upgrades, enhanced observability, and AI-optimized developer workflows.
