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

## 🏁 Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/mobitrendz/fastapi-backend-template.git
cd fastapi-backend-template
```

### 2. Install Dependencies
This project uses uv for dependency management. If you don't have it, install it here.

```bash
# Sync environment and install dependencies
uv sync

# Activate the virtual environment
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

