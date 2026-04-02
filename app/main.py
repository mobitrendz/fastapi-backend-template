import logging

from app import initial_data, backend_pre_start

from fastapi import FastAPI
from app.api import welcome


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("FastAPI starting...")
    backend_pre_start.main()
    initial_data.main()


app.include_router(welcome.router)


@app.on_event("shutdown")
def on_shutdown():
    logger.info("FastAPI stopping...")