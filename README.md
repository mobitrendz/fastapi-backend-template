# FastAPI AI-Optimized Enterprise Backend Template

A production-ready foundation for scalable web applications leveraging **FastAPI**, **SQLModel**, and **Alembic**. This template is engineered for high-performance Python 3.14+ environments, utilizing **uv** for deterministic dependency management and **Docker Compose** for full-stack orchestration.

## 🌟 Key Features

*   **AI-Driven Development**: Optimized for **Gemini CLI** for autonomous engineering, refactoring, and feature implementation.
*   **Python 3.14+ Runtime**: Leverages the latest interpreter performance enhancements.
*   **Enterprise Observability**: Structured JSON logging with **Structlog** and real-time metrics with **Prometheus**.
*   **API Standardization**: Integrated **Pagination** for uniform list responses and **Rate Limiting** via SlowAPI.
*   **Modern Dependency Management**: Powered by [uv](https://astral.sh) for lightning-fast, reproducible builds.
*   **Full-Stack Orchestration**: Integrated **PostgreSQL 18** and **pgAdmin 4** services.
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

### 🛠️ Tooling & Infrastructure
- 📦 **uv** — Next-generation, lightning-fast Python package and project manager.
- 🐳 **Docker & Compose** — Full-stack container orchestration for environmental parity.
- 🦀 **Zensical** — Ultra-fast, Rust-powered documentation generator for this project.
- 🤖 **Gemini CLI** — AI-powered autonomous agent for rapid, surgical engineering.

### 🧪 Quality Assurance
- 🧪 **Pytest & Coverage** — Mature testing framework with detailed coverage reporting.
- 🧹 **Ruff** — Extremely fast, all-in-one Python linter and code formatter.
- 🔍 **Mypy** — Strict static type checking to eliminate runtime type errors.

## 🤖 Gemini CLI AI-Driven Development

This project is built and maintained using **Gemini CLI**, an advanced AI agent for software engineering.

### Core Benefits:
- **Autonomous Engineering**: Gemini CLI can research the codebase, plan complex changes, and execute them surgically.
- **Context Awareness**: Leverages the `GEMINI.md` mandates to ensure all AI-generated code adheres to project-specific architectural standards.
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

The project utilises a multi-container architecture managed via `docker-compose.yaml`. This ensures environmental parity across development, staging, and production.

### Service Architecture

| Service | Technology | Role |
| :--- | :--- | :--- |
| **API** | FastAPI / Uvicorn | Primary application server with built-in health monitoring. |
| **DB** | PostgreSQL 18 | Relational data store with persisted volume mapping. |
| **pgAdmin** | pgAdmin 4 | Web-based database administration and query interface. |
| **Seeder** | Python/Shell | Lifecycle service; executes migrations and populates initial system state. |

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
│   ├── models/                    # SQLModels, Tables, and DTOs (Data Transfer Objects)
│   ├── services/                  # Complex business logic and external integrations
│   └── main.py                    # FastAPI application initialization
├── alembic/                       # Database migrations and environment setup
├── docs/                          # Zensical documentation source (Markdown)
├── site/                          # Generated Zensical static documentation
├── scripts/                       # Shell scripts for deployment and startup
├── tests/                         # Pytest suite for unit and integration testing
├── .env                           # Environment variables (Internal)
├── .env.example                   # Template for environment variables
├── alembic.ini                    # Alembic configuration
├── docker-compose.override.yml    # Container Orchestration Manifest for dev env
├── docker-compose.yaml            # Container Orchestration Manifest
├── Dockerfile                     # Multi-stage, non-root Production Build
├── pyproject.toml                 # Dependency management (uv)
├── zensical.toml                  # Zensical documentation configuration
└── README.md                      # Project documentation
```

## 🏁 Getting Started

### 1. Clone the Repository
```bash
git clone -b develop git@github.com:mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template
```

### 2. Environment Configuration

Update the following variables in .env file:

**Security & Super user**

Generate a secure SECRET_KEY for JWT tokens (e.g., using [JWT Secret Key Generator](https://jwtsecretkeygenerator.com)).
```bash
SECRET_KEY="your-generated-hs256-key"

# Superuser details
ADMIN_USER_NAME="admin"
ADMIN_USER_EMAIL="admin@example.com"
ADMIN_USER_PASSWORD="securepassword"      #Password must be min. 8 characters
```

**Database Connection**

```bash
# Postgres Connection Settings
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=database                     # change it
POSTGRES_USER=username                   # change it
POSTGRES_PASSWORD=password               # change it

# The app will construct the URL as:
# postgresql+psycopg://username:password@localhost:5432/database
```

**pgAdmin settings**
```bash
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

### 3. Orchestration Launch

Deploy the entire stack with a single command:
```bash
docker compose up --build
```

This triggers the following automated sequence:

1, Database Provisioning: Postgres 18 initialises with health checks.

2, API Warm-up: The FastAPI service starts and waits for database readiness.

3, Lifecycle Task (Seeder): Once the API is healthy, the seeder container runs alembic upgrade head and populates the database with initial administrative credentials.

**The Log Noise Fix (Detached Mode)**

In an enterprise setup, you typically don't want pgAdmin logs cluttering your terminal while you are coding the API. Run the stack in detached mode and only "follow" the logs for your FastAPI app:

```bash
# Start everything in the background
docker compose up -d

# Only watch your API logs
docker compose logs -f api
```

### 4. Application Entry Points
- API Documentation: http://localhost:8000/docs
- Database Management: http://localhost:5050
- Health Status: http://localhost:8000/health

### 5. 🛠️ Local Development
For native development, ensure you have the uv package manager installed:
```bash
# Sync environment and dependencies
uv sync

# Activate Pre-commit hooks
uv uv run pre-commit install

# Activate virtual environment
source .venv/bin/activate

# Execute schema migrations
uv run alembic upgrade head

# Start development server (Auto-reload enabled)
uv run fastapi dev
```

### 6. 🧪 Quality Assurance
Maintain system integrity and code quality with the integrated toolchain:

#### 🧹 Linting & Formatting (Ruff)
Ruff is used for extremely fast linting and formatting.
```bash
# Check for linting issues
uv run ruff check .

# Automatically fix fixable issues
uv run ruff check --fix .

# Format the code
uv run ruff format .
```

#### 🔍 Static Type Checking (Mypy)
Mypy ensures type safety throughout the application.
```bash
# Run strict type checking
uv run mypy .
```

#### 🛡️ Security Analysis (Bandit)
Bandit scans for common security vulnerabilities.
```bash
# Run security scan
uv run bandit -c pyproject.toml -r app
```

#### ✅ Test Suite
Run the full test suite with coverage reporting:
```bash
# Run unit and integration tests
uv run pytest
```

### 7. 📚 Documentation (Zensical)
The project documentation is built with **Zensical**, a high-performance, Rust-powered documentation generator.

#### Serve Documentation Locally
To preview the documentation with hot-reloading:
```bash
uv run zensical serve
```
Access the local documentation at: http://localhost:3000

#### Build Static Site
To generate the static documentation site in the `site/` directory:
```bash
uv run zensical build
```
