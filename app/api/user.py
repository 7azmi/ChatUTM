from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def user_login(username: str, password: str):
    return {"message": "User authentication will be implemented later."}
