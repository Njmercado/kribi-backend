from app.db import SessionDep
from app.model.word import Word

def get_word_by_id(word_id: str):
	return SessionDep.get(Word, word_id)

def get_word(session: SessionDep, word: str) -> Word:
	try:
		return session.get(Word, word)
	except Exception as e:
		print(f"Error occurred while fetching word: {e}")
		return

def get_all_words_from_letter(session: SessionDep, letter: str):
	return {"letter": letter}

def delete_word(word: str):
	return {"word": word}

def create_word(word: str):
	return {"word": word}
