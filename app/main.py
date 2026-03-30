from fastapi import FastAPI
from app.api import welcome

app = FastAPI()

app.include_router(welcome.router)