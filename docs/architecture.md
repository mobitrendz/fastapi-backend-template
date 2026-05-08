---
icon: lucide/boxes
---

# Architecture

The project follows a **Layered Modular Architecture** designed for scalability, maintainability, and clear separation of concerns.

## 🏗️ Layered Structure

``` mermaid
graph TD
    API[API Layer - app/api] --> Services[Service Layer - app/services]
    Services --> CRUD[CRUD Layer - app/crud]
    CRUD --> DB[(Database)]
    Services --> Email[Email Service / MailCatcher]
    Models[Model Layer - app/models] -.-> API
    Models -.-> Services
    Models -.-> CRUD
```

### 1. API Layer (`app/api/v1`)
- **Responsibility**: Request handling, validation, and response serialization.
- **Routing**: Versioned endpoints using `APIRouter`.
- **Logic**: Minimal. Delegates complex tasks to the Service Layer.

### 2. Service Layer (`app/services`)
- **Responsibility**: Business logic orchestration.
- **Role**: Coordinates multiple CRUD operations, external API calls, and domain-specific rules.
- **Email Integration**: Orchestrates the rendering of **MJML templates** from `app/email-templates` before sending via the configured SMTP provider.

### 3. CRUD Layer (`app/crud`)
- **Responsibility**: Atomic database operations.
- **Role**: Reusable functions for Create, Read, Update, and Delete operations on specific models.
- **Tooling**: Built on **SQLModel** and **SQLAlchemy**.

### 4. Model Layer (`app/models`)
- **Responsibility**: Data definitions.
- **Unified Models**: Uses `SQLModel` to define both Database Tables and Pydantic Schemas.
- **DTOs**: Explicitly separates `Read`, `Create`, and `Update` models to prevent sensitive data leakage.

## 📡 External Integrations

### Email (MailCatcher)
- **Development**: All outgoing emails are captured by **MailCatcher** in the development environment.
- **Production**: Configurable via environment variables to use any standard SMTP provider.

## 🗄️ Database & Migrations

- **Database**: PostgreSQL 18.
- **Migrations**: **Alembic** manages all schema changes.
- **Workflow**:
    1. Update `SQLModel` definitions in `app/models`.
    2. Generate migration: `uv run alembic revision --autogenerate -m "desc"`.
    3. Apply migration: `uv run alembic upgrade head`.

## 🛡️ Security
- **Authentication**: OAuth2 with Password Flow.
- **JWT**: Tokens generated using HS256.
- **Hashing**: Argon2 via `pwdlib`.
- **Validation**: Pydantic v2 ensures strict data typing and validation.
