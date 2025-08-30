from app.data import words
from app.db import SessionDep

def get_word(session: SessionDep, word: str):
	return words.get_word(session, word)

def get_all_words_from_letter(letter: str):
	return {"letter": letter}

def delete_word(word: str):
	return {"word": word}

def create_word(word: str):
	return {"word": word}
