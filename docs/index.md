---
icon: lucide/home
---

# Introduction

Welcome to the **FastAPI Backend Template** documentation. This project is a production-ready foundation for scalable web applications leveraging **FastAPI**, **SQLModel**, and **Alembic**.

## 🌟 Key Features

*   **Python 3.12+ Runtime**: Leverages the latest interpreter performance enhancements.
*   **Modular Architecture**: Clean separation of API, Services, CRUD, and Models.
*   **Enterprise Security**: OAuth2 with JWT, Argon2 password hashing.
*   **Observability**: Structured JSON logging with Structlog and Prometheus metrics.
*   **Local Reverse Proxy**: Traefik routes local services through stable `.test` domains.
*   **Email Testing**: Integrated **MailCatcher** for capturing and inspecting outgoing emails locally.
*   **Automated Quality**: Fast linting, formatting, and type-checking powered by **Ruff**, **Mypy**, and **Prek**.
*   **Modern Tooling**: Powered by [uv](https://astral.sh) for dependency management.
*   **AI-Optimized**: Native support for **Gemini CLI** autonomous engineering.

## 📁 Project Structure

```text
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


## 🤖 AI-Driven Development

This project is engineered for **Gemini CLI**, enabling autonomous refactoring, research, and implementation. By leveraging `GEMINI.md` mandates, the AI ensures all changes adhere to local architectural standards.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed:
- **Python 3.12+**
- **[uv](https://astral.sh)**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **[Docker & Docker Compose](https://docs.docker.com/get-docker/)**

### 2. Setup
```bash
# Clone the repository
git clone git@github.com:mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template

# Sync dependencies
uv sync

# Install Prek hooks
uv run prek install

# Activate virtual environment
source .venv/bin/activate

# Create .env from example
cp .env.example .env
```

### 3. Run with Docker
```bash
# Deploy local development stack
docker compose up --build
```
This automatically runs migrations and seeds the initial data via the `prestart` service.

Access the API at http://localhost:8000/docs or, after adding the local hosts entries, at http://api.fastapi-template.test/docs.

### 4. Quality Assurance
Ensure the system is stable by running the test suite:
```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=app --cov-report=term-missing
```

## 📚 Documentation Sections

- [**Tech Stack**](tech-stack.md): Detailed overview of the project's technology stack.
- [**Architecture**](architecture.md): Understand the modular design and data flow.
- [**AI-Driven Development**](ai-development.md): Guide for optimizing development with AI tools.
- [**Development**](development.md): Guide for local setup, testing, and observability.
- [**Deployment**](deployment.md): Production builds, Docker, and CI/CD pipelines.
- [**Contributing**](contributing.md): Guidelines for contributing to the project.
