from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from db import SessionDep
from service import auth
from model.auth import Token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/login", response_model=Token)
def login(
  session: SessionDep, 
  form_data: OAuth2PasswordRequestForm = Depends()
):
  """Login endpoint that returns JWT token."""
  try:
    token = auth.login(session, form_data.username, form_data.password)
    return token
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Login failed"
    )
