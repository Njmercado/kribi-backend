import os
from fastapi import FastAPI
from internal import admin
from routers import word, articles, users, auth
from contextlib import asynccontextmanager
from db import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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

@asynccontextmanager
def lifespan(app: FastAPI):
  print("Application is starting...")
  create_db_and_tables()

@app.get("/")
def read_root():
  return {"message": "Hello, from Kribi!"}
