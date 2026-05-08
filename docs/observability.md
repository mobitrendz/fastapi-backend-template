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
