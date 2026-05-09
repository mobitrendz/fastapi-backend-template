from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import sentry_sdk
import structlog
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import EmailStr
from sentry_sdk.integrations.fastapi import FastApiIntegration
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router as v1_router
from app.core.config import settings
from app.core.limiter import limiter
from app.core.logger import setup_logging
from app.core.security import generate_test_email, send_email
from app.db import initial_data
from app.middleware.activity_logger import ActivityLoggerMiddleware
from app.models.generic import Message

setup_logging()
logger = structlog.get_logger(__name__)


# Main application setup using FastAPI.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: UP043
    # --- STARTUP LOGIC ---
    logger.info("--- START SEEDING INITIAL DATA ---")
    logger.debug("Application summary", summary=app.summary)

    try:
        await initial_data.init()
        logger.info("--- FINISH SEEDING INITIAL DATA ---")
    except Exception as e:
        logger.error("Seeding failed", error=str(e))

    yield  # The app is now running and "healthy"

    # --- SHUTDOWN LOGIC ---
    logger.info("--- SYSTEM SHUTDOWN ---")


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        integrations=[
            FastApiIntegration(),
        ],
    )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(ActivityLoggerMiddleware)

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

# Initialize Pagination
add_pagination(app)


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Include the API router for version 1 of the API
app.include_router(v1_router, prefix=settings.API_V1_STR)


# Health check endpoint to verify that the application is running and healthy.
@app.get("/health", tags=["Health Check"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


# Test email endpoint to verify email sending functionality.
@app.post("/test-email/", tags=["Test email"], status_code=201)
def test_email(email_to: EmailStr) -> Message:
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")
