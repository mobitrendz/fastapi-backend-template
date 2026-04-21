import logging
from contextlib import asynccontextmanager

# from app.db import initial_data, backend_pre_start
from fastapi import FastAPI

from app.api.v1.router import api_router as v1_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("--- SYSTEM STARTUP ---")
    print(app.summary)

    # 1. Run migrations (Optional: see note below)
    # 2. Seed initial data
    try:
        print("--- SEEDING COMPLETE ---")
    except Exception as e:
        print(f"Seeding failed: {e}")

    yield  # The app is now running and "healthy"

    # --- SHUTDOWN LOGIC ---
    print("--- SYSTEM SHUTDOWN ---")


app = FastAPI(lifespan=lifespan)


app.include_router(v1_router, prefix="/api/v1")


@app.get("/health", tags=["Health Check"])
async def health():
    return {"status": "ok"}
