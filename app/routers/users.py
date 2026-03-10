from fastapi import APIRouter, Body, Depends
from app.model.user import UserUpdateDTO
from db import SessionDep
from service import users
from typing import Annotated
from model.user import User
from dependencies.auth import (
  VIEW_USER,
  RESTORE_USER,
  DELETE_USER,
  UPDATE_USER,
  get_current_active_user
)

router = APIRouter(
  prefix="/user"
)

@router.get("/{user_id}", dependencies=[VIEW_USER])
def get_user_by_id(session: SessionDep, user_id: int):
  return users.get_user_by_id(session, user_id)

@router.get("/email/{email}", dependencies=[VIEW_USER])
def get_user_by_email(session: SessionDep, email: str):
  return users.get_user_by_email(session, email)

@router.get("/username/{username}", dependencies=[VIEW_USER])
def get_user_by_username(session: SessionDep, username: str):
  return users.get_user_by_username(session, username)

@router.get("/name/{name}", dependencies=[VIEW_USER])
def get_user_by_name(session: SessionDep, name: str):
  return users.get_user_by_name(session, name)

@router.post("/restore/{user_id}", dependencies=[RESTORE_USER])
def restore_user(session: SessionDep, user_id: int):
  return users.restore_user(session, user_id)

@router.delete("/{user_id}", dependencies=[DELETE_USER])
def delete_user(session: SessionDep, user_id: int):
  return users.delete_user(session, user_id)

@router.put("/", dependencies=[UPDATE_USER])
def update_user(
  session: SessionDep,
  user: Annotated[UserUpdateDTO, Body()],
  current_user: User = Depends(get_current_active_user)
):
  return users.update_user(session, current_user, user)