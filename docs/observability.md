---
icon: lucide/telescope
---

# Observability

This project features enterprise-grade observability to help you monitor, debug, and optimize your API in real-time.

## 📈 Prometheus Metrics
We use the `prometheus-fastapi-instrumentator` to automatically collect and expose performance metrics for your FastAPI application.

### Accessing Metrics
The metrics are automatically exposed by the application at:
- **Endpoint**: `http://localhost:8000/metrics`

You can configure your Prometheus server to scrape this endpoint to generate real-time monitoring dashboards (e.g., in Grafana) to track:
- Request latency.
- Request counts by status code.
- Endpoint-specific performance.

## 🪵 Structured Logging (Structlog)
Standard Python logging has been replaced with **Structlog** to provide machine-readable, structured JSON logs.

### Why Structured Logging?
- **Searchability**: Easily filter logs by specific keys (e.g., `event`, `level`, `timestamp`).
- **Observability**: Integrates seamlessly with log aggregation services (like ELK stack or Datadog) for centralized monitoring.

*For more information on logging configuration, see `app/core/logger.py`.*

## 🎯 Error Tracking (Sentry)
This project integrates [Sentry](https://sentry.io/) for proactive error tracking and performance monitoring, utilizing the native FastAPI integration for enhanced trace fidelity.

### Configuration
To enable Sentry, you need to provide your Sentry DSN (Data Source Name).

1. **Get your DSN**:
   - Log in to your [Sentry Dashboard](https://sentry.io/).
   - Create a project in your Sentry dashboard.
   - Find your DSN under **Settings > Projects > [Your Project] > Client Keys (DSN)**.

2. **Update Environment Variable**:
   Add your DSN to the `.env` file:
   ```bash
   SENTRY_DSN="https://your-key@sentry.io/your-project-id"
   ```

3. **Restart Application**:
   Once the environment variable is set, the Sentry SDK will automatically initialize on startup and begin capturing unhandled exceptions.

*Note: If `SENTRY_DSN` is not provided, the Sentry SDK will remain inactive, ensuring no errors are logged to the service during local development.*
