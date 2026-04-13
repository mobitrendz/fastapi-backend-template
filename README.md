# FastAPI Backend Template

A professional template for building scalable backends with **FastAPI**, **SQLModel**, and **Alembic**. This project is configured for modern Python development using uv for lightning-fast dependency management.

## 🚀 Features
- **FastAPI**: Modern, high-performance web framework.
- **SQLModel**: Seamless integration between SQL databases and Pydantic models.
- **Alembic**: Robust database migrations.
- **JWT Authentication**: Secure token-based auth (PyJWT + pwdlib).
- **Settings Management**: Pydantic-settings for environment-based configuration.
- **Developer Friendly**: Pre-configured with pytest and coverage reporting.

## 🛠️ Tech Stack
- **Language**: Python >= 3.14
- **Database**: PostgreSQL (psycopg3)
- **Migrations**: Alembic
- **Async Support**: Standard FastAPI ASGI

## 📂 Project Structure

```
fastapi-backend-template/
├── app/                        # Main Application Logic
│   ├── alembic/                # Database migrations and environment setup
│   ├── api/                    # API Entry points
│   │   └── v1/                 # API Versioning
│   │       ├── endpoints/      # Individual route handlers (e.g., users.py)
│   │       └── router.py       # Main router merging all v1 endpoints
│   ├── core/                   # Global configuration and security (JWT, Auth)
│   ├── crud/                   # Reusable database CRUD operations
│   ├── db/                     # Connection engine, session, and seed data
│   ├── models/                 # SQLModels, Tables, and DTOs (Data Transfer Objects)
│   ├── services/               # Complex business logic and external integrations
│   └── main.py                 # FastAPI application initialization
├── scripts/                    # Shell scripts for deployment and startup
├── tests/                      # Pytest suite for unit and integration testing
├── .env                        # Environment variables (Internal)
├── .env.example                # Template for environment variables
├── alembic.ini                 # Alembic configuration
├── pyproject.toml              # Dependency management (uv/pip)
└── README.md                   # Project documentation
```

## 📝 Project Description

This project is built on a **Modular Service-Oriented Architecture**, specifically designed to handle enterprise-level scale while remaining developer-friendly.

### Core Architectural Pillars

- API & Versioning (app/api/v1). 
Decouples the interface from the logic. By versioning the API, we ensure that new feature rollouts do not break existing client integrations.

- Business Logic Separation (app/services)

Unlike basic templates, this structure separates **Services** from **CRUD**. While crud/ handles direct database interactions, services/ contains complex business rules, calculations, and third-party API calls, ensuring the code remains DRY (Don't Repeat Yourself).

- Data Integrity (app/models & app/db)

Leverages **SQLModel** to unify Pydantic validation and SQLAlchemy ORM. The db/ module manages the lifecycle of the asynchronous database engine and handles automated data seeding on startup.

- Infrastructure & Automation (scripts/)

Includes dedicated shell scripts to streamline container startup, database wait-checks, and migration application, making the project **Docker-ready** out of the box.

- Security First (app/core)

Centralizes sensitive logic, including **OAuth2 with Password flow, JWT token generation**, and **Argon2 password hashing**, ensuring a consistent security posture across the entire application.

## 🏁 Getting Started
### 1. Clone the Repository
```bash
git clone -b develop git@github.com:mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template
```

### 2. Install Dependencies
This project uses uv for dependency management. If you don't have it, install it here.

**Sync environment and install dependencies**
```bash
uv sync
```

**Activate the virtual environment**
```bash
source .venv/bin/activate
```

### 3. Environment Configuration
Update the following variables in .env file:

**Database Connection**

**[!IMPORTANT] - Ensure PostgreSQL is running locally with an empty database created.**

```bash
POSTGRES_URL="postgresql+psycopg://username:password@localhost:5432/dbname"
```

**Security & Superuser**

Generate a secure SECRET_KEY for JWT tokens (e.g., using [JWT Secret Key Generator](https://jwtsecretkeygenerator.com)).
```bash
SECRET_KEY="your-generated-hs256-key"

# Superuser details 
SUPER_USER_NAME="admin"
SUPER_USER_EMAIL="admin@example.com"
SUPER_USER_PASSWORD="securepassword"      #Password must be min. 8 characters
```

## 🗄️ Database Migrations
Apply the predefined database schema to your PostgreSQL instance:
```bash
uv run alembic upgrade head
```

## 🏃 Running the Application
Start the FastAPI development server:
```bash
uv run fastapi dev
```

### Verify Installation
Once the server is running, you can access:
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Health Check/Demo**: http://127.0.0.1:8000/Harry%20Potter

## 🧪 Testing
Run the test suite with coverage reporting:
```bash
uv run pytest
```

