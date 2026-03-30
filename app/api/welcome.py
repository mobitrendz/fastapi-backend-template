from fastapi import APIRouter

router = APIRouter(prefix="", tags=["welcome"])

@router.get("/")
def get_welcome_message():
    return {"message": "Welcome User!"}