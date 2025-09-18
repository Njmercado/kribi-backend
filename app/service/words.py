from model.user import User
from data import words
from db import SessionDep
from fastapi import exceptions, Response, HTTPException
from model.word import Word
from utils import responses
from utils.words import transform_word_to_regexp

def get_word(session: SessionDep, word: str):
	try:
		return words.get_word(session, word)
	except Exception as e:
		raise HTTPException(status_code=404, detail="Word not found")

def get_word_by_id(session: SessionDep, word_id: int):
	try:
		return words.get_word_by_id(session, word_id)
	except Exception as e:
		raise HTTPException(status_code=404, detail=f"Error retrieving word: {e}")

def get_all_words_from_letter(session: SessionDep, letter: str, page: int, limit: int):
	try:
		return words.get_all_words_from_letter(session, letter, page, limit)
	except Exception as e:
		raise HTTPException(status_code=404, detail="Words not found")

def search_words(session: SessionDep, substring: str):
	try:
		return words.get_all_words_from_search(session, transform_word_to_regexp(substring))
	except Exception as e:
		raise HTTPException(status_code=404, detail="Words not found")

def delete_word(session: SessionDep, word_id: int, user_id: int):
	try:
		words.delete_word(session, word_id, user_id)
		return responses.WORD_DELETED_SUCCESSFULLY(word_id)
	except exceptions.ValidationException as e:
		return HTTPException(status_code=404, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=400, detail=f"Error deleting word: {e}")

def create_word(session: SessionDep, word: Word, user: User):
	try:
		words.create_word(session, word, user)
		return responses.WORD_CREATED_SUCCESSFULLY(word.word)
	except exceptions.ValidationException as e:
		raise HTTPException(status_code=400, detail=str(e))

def update_word(session: SessionDep, word_id: int, word: Word):
	try:
		response = words.update_word(session, word_id, word)
		return Response(status_code=200, content=f"Word '{response.word}' updated successfully :)")
	except exceptions.ValidationException as e:
		raise HTTPException(status_code=400, detail=str(e))
