from fastapi import APIRouter

from app.db import SessionDep

router = APIRouter(
  prefix="/admin",
)

@router.get("/users")
def get_users():
	return {"users": []}
