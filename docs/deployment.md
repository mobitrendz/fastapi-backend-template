---
icon: lucide/ship
---

# Deployment

The project is designed to be deployed using **Docker Compose** for seamless environment parity. The base `docker-compose.yaml` is production-oriented; local-only services are added by `docker-compose.override.yml`.

## 🐳 Docker Compose Architecture

The base `docker-compose.yaml` defines these key services:

| Service | Technology | Role |
| :--- | :--- | :--- |
| **Traefik** | Traefik v3 | Reverse proxy for host-based routing. |
| **API** | FastAPI / Uvicorn | The application server. |
| **DB** | PostgreSQL 18 | The primary database. |
| **Seeder** | Python | Handles migrations and initial data. |

Development-only services live in `docker-compose.override.yml`:

| Service | Technology | Role |
| :--- | :--- | :--- |
| **pgAdmin** | pgAdmin 4 | Local database administration interface. |
| **MailCatcher** | MailCatcher | Local SMTP server and email inspection UI. |

## 🚀 Deployment Steps

### 1. Configure Environment
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Ensure `SECRET_KEY` and database credentials are set securely.

### 2. Launch Stack
For production-style deployment without local-only tools:
```bash
docker compose -f docker-compose.yaml up -d --build
```

For local development, where Compose automatically includes `docker-compose.override.yml`:
```bash
docker compose up -d --build
```

The base Traefik route file is `traefik/dynamic.yml`. The local override mounts `traefik/dynamic.local.yml`, which adds pgAdmin and MailCatcher routes.

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
The `Dockerfile` uses a multi-stage build process to ensure a lean and secure production image. It leverages `uv.lock` for deterministic, reproducible builds.

1.  **Builder**: Installs `uv`, syncs dependencies from `uv.lock`, and builds the application environment.
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
