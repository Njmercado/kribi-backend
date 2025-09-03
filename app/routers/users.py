from fastapi import APIRouter
from db import SessionDep
from service import users

router = APIRouter(
  prefix="/user"
)

@router.get("/{user_id}")
def get_user(session: SessionDep, user_id: int):
  return users.get_user(session, user_id)
