import os
from app.db import engine
from app.model.word import Word, WORD_TYPES, DEFAULT_WORD_TYPE 
from pandas import read_csv
from sqlmodel import delete, Session

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "dictionary.csv")

def reload_words_migration():
  with Session(engine) as session:
    print("Starting words migration...")
    try:
      session.exec(delete(Word))
      session.commit()
      df = read_csv(csv_path)
      for _, row in df.iterrows():
        word = Word()
        word.word = row['termino']
        word.definitions = [row['significado']]
        word.translations = row[['traduccion_1', 'traduccion_2', 'traduccion_3', 'traduccion_4']].dropna().tolist()
        word.type = WORD_TYPES.get(row['etiqueta'], DEFAULT_WORD_TYPE)
        session.add(word)
        session.commit()
        print(f"Word added: {word.word}")
      print("Words migration completed successfully.")
    except Exception as e:
      session.close()
      print('Error loading words:', e)

if __name__ == "__main__":
  reload_words_migration()