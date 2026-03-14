from app.db import engine
from sqlmodel import Session, update 
from app.model.article import Article

def fill_cover_column_with_empty_str():
  with Session(engine) as session:
    try:
      print("Starting cover column update for articles...")
      session.exec(
        update(Article)
        .values(cover="")
      )
      session.commit()
      print("Cover column update completed successfully.")
    except Exception as e:
      print('Error updating cover column:', e)

if __name__ == "__main__":
  fill_cover_column_with_empty_str()
