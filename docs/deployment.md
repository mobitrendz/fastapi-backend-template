---
icon: lucide/ship
---

# Deployment

The project is designed to be deployed using **Docker Compose** for seamless environment parity.

## 🐳 Docker Compose Architecture

The `docker-compose.yaml` defines several key services:

| Service | Technology | Role |
| :--- | :--- | :--- |
| **API** | FastAPI / Uvicorn | The application server. |
| **DB** | PostgreSQL 18 | The primary database. |
| **pgAdmin** | pgAdmin 4 | Database administration interface. |
| **MailCatcher** | MailCatcher | Local SMTP server for email testing (Development). |
| **Seeder** | Python | Handles migrations and initial data. |

## 🚀 Deployment Steps

### 1. Configure Environment
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Ensure `SECRET_KEY` and database credentials are set securely.

### 2. Launch Stack
```bash
docker compose up -d --build
```

### 3. Verify Health
Check service health:
```bash
docker compose ps
```

## 💾 Data Persistence
Database volumes are mapped to the host to ensure data persists across container restarts:
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

## 🏗️ Production Build
The `Dockerfile` uses a multi-stage build process:
1.  **Builder**: Installs `uv`, syncs dependencies, and builds the application environment.
2.  **Runner**: A slim, non-root image optimized for production execution.

### Build Target
```bash
docker build -t fastapi-backend:latest .
```

## 🏥 Health Checks
The API service includes a health check to ensure it's ready before dependent services start:
```bash
# Verify manually
curl http://localhost:8000/health
```
