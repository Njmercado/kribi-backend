import os
from fastapi import FastAPI
from internal import admin
from routers import word, articles, users, auth
from contextlib import asynccontextmanager
from db import create_db, close_db_connections, get_connection_info
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup
  print("Application is starting...")
  CREATE_TABLES = os.getenv("CREATE_TABLES", "false").lower() == "true"
  if CREATE_TABLES:
    create_db()
    print("Database created/verified")

  yield

  # Shutdown
  print("Application is shutting down...")
  close_db_connections()
  print("Database connections closed")

app = FastAPI(lifespan=lifespan)

origins = [
  "http://localhost",
  os.getenv("ADMIN_FRONTEND_URL", "http://localhost:3000"),
  os.getenv("FRONTEND_URL", "http://localhost:5173"),
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(word.router)
app.include_router(articles.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root():
  return {"message": "Hello, from Kribi!"}

@app.get("/health/db")
def database_health():
  """Check database connection pool health."""
  return get_connection_info()
