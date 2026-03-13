from model.user import User, UserCreateDTO, UserUpdateDTO
from data import users
from db import SessionDep
from fastapi import HTTPException, Response, exceptions
from utils.words import transform_input_to_regexp
from utils.responses import USER_RESTORED_SUCCESSFULLY

def search_user(session: SessionDep, current_user: User, value: str, page: int, limit: int):
  try:
    return users.search_user(session, current_user.id, transform_input_to_regexp(value), page, limit)
  except Exception as e:
    raise HTTPException(status_code=404, detail="Could not find any matching users")

def restore_user(session: SessionDep, user_id: int):
  try:
    user = users.get_user_by_id(session, user_id)
    if not user:
      raise exceptions.ValidationException(f"User with ID {user_id} not found.")
    users.restore_user(session, user)
    return Response(status_code=204)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def delete_user(session: SessionDep, user_id: int):
  try:
    user = users.get_user_by_id(session, user_id)
    if not user:
      raise exceptions.ValidationException(f"User with ID {user_id} not found.")
    users.delete_user(session, user)
    return Response(status_code=204)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def update_user(session: SessionDep, user_data: UserUpdateDTO):
  try:
    existing_user = users.get_user_by_id(session, user_data.id)
    if not existing_user:
      raise exceptions.ValidationException(f"User with ID {user_data.id} not found.")
    return users.update_user(session, existing_user, user_data)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def create_user(session: SessionDep, user: UserCreateDTO, current_user: User):
  try:
    return users.create_user(session, user, current_user.id)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))