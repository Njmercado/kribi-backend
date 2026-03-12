from fastapi import APIRouter, Body, Depends, Query
from db import SessionDep
from service import users
from typing import Annotated
from model.user import User, UserCreateDTO, UserUpdateDTO
from dependencies.auth import (
  CreateUserRequired,
  ViewUserRequired,
  RestoreUserRequired,
  DeleteUserRequired,
  UpdateUserRequired,
  get_current_active_user
)

router = APIRouter(
  prefix="/user"
)

@router.get("/search", dependencies=[ViewUserRequired])
def search_users(
  session: SessionDep,
  value: Annotated[str, Query()],
  current_user: User = Depends(get_current_active_user),
  page: int = Query(1, ge=1),
  limit: int = Query(10, ge=1, le=100)
):
  return users.search_user(session, current_user, value, page, limit)

@router.post("/restore/{user_id}", dependencies=[RestoreUserRequired])
def restore_user(session: SessionDep, user_id: int):
  return users.restore_user(session, user_id)

@router.delete("/{user_id}", dependencies=[DeleteUserRequired])
def delete_user(session: SessionDep, user_id: int):
  return users.delete_user(session, user_id)

@router.put("/", dependencies=[UpdateUserRequired])
def update_user(
  session: SessionDep,
  user: Annotated[UserUpdateDTO, Body()],
):
  return users.update_user(session, user)

@router.post("/", dependencies=[CreateUserRequired])
def create_user(
  session: SessionDep,
  user: Annotated[UserCreateDTO, Body()],
  current_user: User = Depends(get_current_active_user)
):
  return users.create_user(session, user, current_user)