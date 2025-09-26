from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from db import SessionDep
from service import auth
from model.auth import Token
from model.user import User
from dependencies.auth import get_current_active_user

router = APIRouter(
  prefix="/auth",
  tags=["authentication"]
)

@router.post("/login")
def login(
  response: Response,
  session: SessionDep, 
  form_data: OAuth2PasswordRequestForm = Depends()
):
  """Login endpoint that sets JWT token as httpOnly cookie."""
  try:
    token = auth.login(session, form_data.username, form_data.password)
    
    # Set httpOnly cookie
    response.set_cookie(
      key="access_token",
      value=token.access_token,
      httponly=True,
      secure=True,  # Set to True in production with HTTPS
      samesite="none", # As frontend is on a different domain 'none' is necessary to avoid cross-site issues
      max_age=30 * 60,  # 30 minutes (same as token expiry)
      path="/"
    )
    
    return {"message": "Login successful", "token_type": token.token_type}
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Login failed"
    )

@router.post("/logout")
def logout(response: Response):
  """Logout endpoint that clears the authentication cookie."""
  response.delete_cookie(
    key="access_token",
    path="/",
    httponly=True,
    secure=True,
    samesite="none", # As frontend is on a different domain 'none' is necessary to avoid cross-site issues
  )
  return {"message": "Logout successful"}

@router.get("/me")
async def get_current_user(
  current_user: User = Depends(get_current_active_user)
):
  """Get current authenticated user information."""
  return {
    "id": current_user.id,
    "email": current_user.email,
    "username": current_user.username,
    "role": current_user.role,
    "entitlements": current_user.entitlements,
    "is_active": current_user.is_active,
    "full_name": current_user.full_name,
  }
