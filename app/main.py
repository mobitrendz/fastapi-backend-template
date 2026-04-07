from app.api.login import login_access_token
import logging

from app.core import initial_data, backend_pre_start

from fastapi import FastAPI
from app.api import welcome, users, login


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")  # ty:ignore[deprecated]
def on_startup():
    logger.info("FastAPI starting...")
    backend_pre_start.main()
    initial_data.main()
    
app.include_router(welcome.router)
app.include_router(users.router)
app.include_router(login.router)


@app.on_event("shutdown")  # ty:ignore[deprecated]
def on_shutdown():
    logger.info("FastAPI stopping...")

