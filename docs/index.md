---
icon: lucide/home
---

# Introduction

Welcome to the **FastAPI Backend Template** documentation. This project is a production-ready foundation for scalable web applications leveraging **FastAPI**, **SQLModel**, and **Alembic**.

## 🌟 Key Features

*   **Python 3.14+ Runtime**: Leverages the latest interpreter performance enhancements.
*   **Modular Architecture**: Clean separation of API, Services, CRUD, and Models.
*   **Enterprise Security**: OAuth2 with JWT, Argon2 password hashing.
*   **Observability**: Structured JSON logging with Structlog and Prometheus metrics.
*   **Email Testing**: Integrated **MailCatcher** for capturing and inspecting outgoing emails locally.
*   **Automated Quality**: Fast linting, formatting, and type-checking powered by **Ruff**, **Mypy**, and **Prek**.
*   **Modern Tooling**: Powered by [uv](https://astral.sh) for dependency management.
*   **AI-Optimized**: Native support for **Gemini CLI** autonomous engineering.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.14+
- [uv](https://astral.sh)
- Docker & Docker Compose

### 2. Setup
```bash
# Clone the repository
git clone git@github.com:mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template

# Sync dependencies
uv sync

# Create .env from example
cp .env.example .env
```

### 3. Run with Docker
```bash
docker compose up --build
```
Access the API at: http://localhost:8000/docs

## 📚 Documentation Sections

- [**Architecture**](architecture.md): Understand the modular design and data flow.
- [**Development**](development.md): Guide for local setup, testing, and linting.
- [**Deployment**](deployment.md): Production builds and infrastructure details.
