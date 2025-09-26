import os
from app.db import engine
from app.model.user import User, Role, Entitlement
from passlib.context import CryptContext
from sqlmodel import Session
from dotenv import load_dotenv

load_dotenv()

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD", "admin123")

def create_admin_users():
  with Session(engine) as session:
    user = User(
      email="njesusmercado@gmail.com",
      username="admin",
      hashed_password=crypt_context.hash(ADMIN_PASSWORD),
      name="Admin",
      last_name="User",
      full_name="Admin User",
      is_active=True,
      is_superuser=True,
      role=Role.SUPER_ADMIN,
      entitlements=[
        Entitlement.CREATE_USER.value,
        Entitlement.VIEW_USER.value,
        Entitlement.UPDATE_USER.value,
        Entitlement.DELETE_USER.value,
        Entitlement.RESTORE_USER.value
      ]
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    print(f"Super Admin user created: {user.email}")

if __name__ == "__main__":
  create_admin_users()
