from websockets.version import tag
import logging

#from app.db import initial_data, backend_pre_start

from fastapi import FastAPI

from app.api.v1.router import api_router as v1_router


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")  # ty:ignore[deprecated]
def on_startup():
    logger.info("FastAPI starting...")
#    backend_pre_start.main()
#    initial_data.main()
    

app.include_router(v1_router, prefix="/api/v1")


@app.on_event("shutdown")  # ty:ignore[deprecated]
def on_shutdown():
    logger.info("FastAPI stopping...")


@app.get("/health", tags=["Health Check"])
async def health():
    return {"status": "ok"}