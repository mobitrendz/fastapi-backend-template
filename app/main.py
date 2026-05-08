from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import EmailStr
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router as v1_router
from app.core.config import settings
from app.core.logger import setup_logging
from app.core.security import generate_test_email, send_email
from app.db import initial_data
from app.models.generic import Message

setup_logging()
logger = structlog.get_logger(__name__)


# Main application setup using FastAPI. This module defines the main application instance and includes the API router for version 1 of the API, which contains all the endpoint routers for user management, authentication, and welcome messages. The application also includes a health check endpoint to verify that the application is running and healthy.
# The lifespan function is used to run startup and shutdown logic for the application. During startup, it seeds the initial data into the database, ensuring that necessary data is present before the application starts handling requests. The shutdown logic can be used to perform any necessary cleanup when the application is shutting down. The use of asynccontextmanager allows for asynchronous operations during startup and shutdown, making it suitable for tasks that may involve I/O operations, such as database interactions.
# The application is organized to promote maintainability and scalability, with a clear separation of concerns between the main application setup, API routing, database interactions, and initial data seeding. This structure allows for easy extension of the application in the future, such as adding new API endpoints, additional database models, or more complex startup and shutdown logic as needed. The use of logging provides feedback on the application's startup process, making it easier to monitor and debug during development and production. Overall, this setup provides a solid foundation for building a robust and scalable FastAPI application.


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: UP043
    # --- STARTUP LOGIC ---
    logger.info("--- START SEEDING INITIAL DATA ---")
    logger.debug("Application summary", summary=app.summary)

    # 1. Run migrations (Optional: see note below)
    # 2. Seed initial data
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

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Include the API router for version 1 of the API, which contains all the endpoint routers for user management, authentication, and welcome messages. This organizes the API endpoints under a common prefix (e.g., /api/v1) and allows for easy versioning of the API in the future.
app.include_router(v1_router, prefix=settings.API_V1_STR)


# Health check endpoint to verify that the application is running and healthy. This endpoint can be used by monitoring tools or load balancers to check the health of the application and ensure that it is responding to requests as expected.
@app.get("/health", tags=["Health Check"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


# Test email endpoint to verify that the email sending functionality is working correctly. This endpoint accepts an email address as input and sends a test email to that address, returning a message indicating that the test email was sent successfully. This can be used to verify that the email configuration is correct and that emails are being sent as expected.
@app.post("/test-email/", tags=["Test email"], status_code=201)
def test_email(email_to: EmailStr) -> Message:
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")
