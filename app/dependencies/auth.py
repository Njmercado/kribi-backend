from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from service.auth import verify_token
from data.users import get_user_by_email
from db import SessionDep
from model.user import User, Role, Entitlement
from typing import List, Callable

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_active_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
  """Get current active user from JWT Token"""

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  token_data = verify_token(token)
  user = get_user_by_email(session, email=token_data.email)
  if user is None:
    raise credentials_exception

  if not user.is_active:
    raise HTTPException(status_code=400, detail="Inactive user")
  return user

def require_roles(allowed_roles: List[Role]) -> Callable:
  """Dependency factory to check if user has required roles."""
  def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role not in allowed_roles:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
      )
    return current_user
  return role_checker

def require_entitlements(required_entitlements: List[Entitlement]) -> Callable:
  """Dependency factory to check if user has required entitlements."""
  def entitlement_checker(current_user: User = Depends(get_current_active_user)) -> User:
    user_entitlements = [Entitlement(ent) for ent in current_user.entitlements] if current_user.entitlements else []
    
    # Super admins have all entitlements
    if current_user.role == Role.SUPER_ADMIN:
      return current_user
    
    # Check if user has all required entitlements
    missing_entitlements = [ent for ent in required_entitlements if ent not in user_entitlements]
    if missing_entitlements:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Access denied. Missing entitlements: {[ent.value for ent in missing_entitlements]}"
      )
    return current_user
  return entitlement_checker

def require_admin() -> Callable:
  """Dependency to check if user is an admin (SUPER_ADMIN, WORD_ADMIN, or ARTICLE_ADMIN)."""
  return require_roles([Role.SUPER_ADMIN, Role.WORD_ADMIN, Role.ARTICLE_ADMIN])

def require_super_admin() -> Callable:
  """Dependency to check if user is a super admin."""
  return require_roles([Role.SUPER_ADMIN])

def require_word_admin() -> Callable:
  """Dependency to check if user is a word admin or super admin."""
  return require_roles([Role.SUPER_ADMIN, Role.WORD_ADMIN])

def require_article_admin() -> Callable:
  """Dependency to check if user is an article admin or super admin."""
  return require_roles([Role.SUPER_ADMIN, Role.ARTICLE_ADMIN])

# Pre-built dependencies for common use cases
AdminRequired = Depends(require_admin())
SuperAdminRequired = Depends(require_super_admin())
WordAdminRequired = Depends(require_word_admin())
ArticleAdminRequired = Depends(require_article_admin())

# Entitlement-based dependencies
CreateWordRequired = Depends(require_entitlements([Entitlement.CREATE_WORD]))
EditWordRequired = Depends(require_entitlements([Entitlement.EDIT_WORD]))
DeleteWordRequired = Depends(require_entitlements([Entitlement.DELETE_WORD]))
ViewWordRequired = Depends(require_entitlements([Entitlement.VIEW_WORD]))
