#New FastAPI project 
#Sreeraj Sreenivasan
#30 Mar 2026

My FastAPI - A FastAPI learning project

Create a python project using UV (Assuming UV is already installed)
uv init my-fastapi
cd my-fastapi

Create python virtual environment
uv venv

Activate virtual environment
source .venv/bin/activate

To check the active virtual environment
which python

Install FastAPI dependency
uv add fastapi --extra standard

Modify main.py 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

Run FastAPI
uv run fastapi dev


