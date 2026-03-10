from app.model.user import User, UserUpdateDTO
from data import users
from db import SessionDep
from fastapi import HTTPException, exceptions
from utils.words import transform_input_to_regexp
from utils.responses import USER_RESTORED_SUCCESSFULLY, USER_DELETED_SUCCESSFULLY

def get_user_by_id(session: SessionDep, user_id: int):
  try:
    return users.get_user_by_id(session, user_id)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def get_user_by_email(session: SessionDep, email: str):
  try:
    return users.get_user_by_email(session, email)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
def get_user_by_username(session: SessionDep, username: str):
  try:
    return users.get_user_by_username(session, username)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
def get_user_by_name(session: SessionDep, name: str):
  try:
    regex_name = transform_input_to_regexp(name)
    return users.get_user_by_name(session, regex_name)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def restore_user(session: SessionDep, user_id: int):
  try:
    user = users.get_user_by_id(session, user_id)
    if not user:
      raise exceptions.ValidationException(f"User with ID {user_id} not found.")
    users.restore_user(session, user)
    return USER_RESTORED_SUCCESSFULLY(user_id)
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
    return USER_DELETED_SUCCESSFULLY(user_id)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

def update_user(session: SessionDep, current_user: User, user_data: UserUpdateDTO):
  try:
    existing_user = users.get_user_by_id(session, user_data.id)
    if not existing_user:
      raise exceptions.ValidationException(f"User with ID {user_data.id} not found.")
    return users.update_user(session, current_user, user_data)
  except exceptions.ValidationException as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
