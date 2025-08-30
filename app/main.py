from fastapi import FastAPI
from app.internal import admin
from app.routers import word, articles
from contextlib import asynccontextmanager
from . import db

app = FastAPI()

app.include_router(word.router)
app.include_router(articles.router)
app.include_router(admin.router)

@asynccontextmanager
def lifespan(app: FastAPI):
  print("Application is starting...")
  db.create_db_and_tables()

@app.get("/")
def read_root():
  return {"message": "Hello, from Kribi!"}
