# FastAPI AI-Optimized Enterprise Backend Template

<a href="https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/docker-compose-test.yml" target="_blank"><img src="https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/docker-compose-test.yml/badge.svg?branch=develop" alt="Docker Validation"></a>
<a href="https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-fastapi-backend-template.yml" target="_blank"><img src="https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-fastapi-backend-template.yml/badge.svg?branch=develop" alt="Backend Code Quality"></a>
<a href="https://github.com/mobitrendz/fastapi-backend-template/actions/workflows/test-coverage.yml" target="_blank"><img src="coverage.svg" alt="Coverage"></a>

A production-ready FastAPI template designed for scalable, high-performance web applications. This project provides a robust, modular foundation that integrates enterprise-grade security, comprehensive observability, and automated quality assurance workflows out of the box.

## 🌟 Key Features

*   **AI-Driven Development**: Optimized for **Google Antigravity** and **Gemini CLI** assisted engineering, refactoring, code review, and feature implementation.
*   **Python 3.12+ Runtime**: Leverages the latest interpreter performance enhancements.
*   **Enterprise Observability**: Structured JSON logging with **Structlog** and real-time metrics with **Prometheus**.
*   **API Standardization**: Integrated **Pagination** for uniform list responses and **Rate Limiting** via SlowAPI.
*   **Modern Dependency Management**: Powered by <a href="https://astral.sh" target="_blank">uv</a> for lightning-fast, reproducible builds.
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
- 🎯 **Sentry SDK** — Proactive error tracking and performance monitoring with native FastAPI integration.
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
- **More info**: <a href="https://docs.astral.sh/uv/getting-started/installation/" target="_blank">uv Installation Guide</a>

### 🐳 Docker & Docker Compose
Used for full-stack orchestration and environmental parity.

- **Desktop (macOS/Windows/Linux)**: <a href="https://docs.docker.com/get-docker/" target="_blank">Install Docker Desktop</a>
- **Linux (Engine only)**: <a href="https://docs.docker.com/engine/install/" target="_blank">Install Docker Engine</a>

## 🏁 Getting Started

### 1. Clone the Repository
```bash
git clone git@github.com:mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template
```

### 2. Environment Configuration

Refer to the <a href="http://localhost:3000/development/#environment-configuration" target="_blank">Environment Configuration</a> section in the development documentation for details on setting up your `.env` file, database credentials, and security keys.

*Note: The documentation portal requires Zensical to be running locally (`uv run zensical serve`) to access these links.*

### 3. Orchestration Launch

Deploy the local development stack with a single command:
```bash
docker compose up --build
```

For a base stack without development-only pgAdmin and MailCatcher services, run:
```bash
docker compose -f docker-compose.yaml up --build
```

### 4. Documentation (Zensical)
The project documentation is built with **Zensical**, a high-performance, Rust-powered documentation generator. It serves as the primary resource for deep-dives into our architecture, development workflows, and deployment strategies.

#### Access & Build
- **Serve Locally**: `uv run zensical serve` (Available at: http://localhost:3000)
- **Build Static Site**: `uv run zensical build`

*For an in-depth understanding of the system, please explore the full <a href="http://localhost:3000" target="_blank">Documentation Portal</a>.*

---

### 5. Local API Development (Hybrid Setup)

For developers who prefer running the database services via Docker while developing the FastAPI application natively on their host machine for faster iteration:

1. **Start Database Services only**:
   ```bash
   docker compose up -d db pgadmin mailcatcher
   ```

2. **Configure Local Environment**:
   Ensure your `.env` connects to the local Docker ports (e.g., `POSTGRES_SERVER=localhost` and `POSTGRES_PORT=5432`).

3. Run API Natively:
   ```bash
   # Sync environment and dependencies
   uv sync

   # Activate virtual environment
   source .venv/bin/activate

   # Start development server (Auto-reload enabled)
   uv run fastapi dev
   ```

4. **Access Endpoints**:
   - API Documentation: http://localhost:8000/docs
   - Prometheus Metrics: http://localhost:8000/metrics
   - pgAdmin: http://localhost:5050
   - MailCatcher UI: http://localhost:1080
   - Health Status: http://localhost:8000/health

---

### 6. 🛠️ Local Development
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
The project documentation is built with **Zensical**, a high-performance, Rust-powered documentation generator. It serves as the primary resource for deep-dives into our **architecture, development workflows, and deployment strategies**.

#### Access & Build
- **Serve Locally**: `uv run zensical serve` (Available at: http://localhost:3000)
- **Build Static Site**: `uv run zensical build`

*For an in-depth understanding of the system, please explore the full <a href="http://localhost:3000" target="_blank">Documentation Portal</a>.*

---

## 📝 Release Notes
See the full <a href="release-notes.md" target="_blank">Release Notes</a> for a detailed history of changes.

## ⚖️ License
This project is licensed under the <a href="LICENSE" target="_blank">MIT License</a>.

## 💡 Inspiration
This project is heavily inspired by the official <a href="https://github.com/fastapi/full-stack-fastapi-template" target="_blank">full-stack-fastapi-template</a> in the FastAPI repository. It builds upon those foundational concepts, incorporating modern toolchain upgrades, enhanced observability, and AI-optimized developer workflows.
