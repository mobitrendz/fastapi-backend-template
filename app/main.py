from fastapi import FastAPI
from app.api import welcome

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World!"}

app.include_router(welcome.router)