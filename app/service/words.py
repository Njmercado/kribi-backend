from model.user import User
from data import words
from db import SessionDep
from fastapi import exceptions, Response, HTTPException 
from model.word import Word
from utils import responses
from utils.words import transform_input_to_regexp
from utils.logger import log

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

def search_words(session: SessionDep, substring: str, page: int, limit: int):
	try:
		results = words.get_all_words_from_search(session, transform_input_to_regexp(substring), page, limit)
		return {
			"words": results[0],
			"has_next_page": results[1]
		}
	except Exception as e:
		log(f"Search failed: {str(e)}")
		raise HTTPException(status_code=404, detail="Could not find any matching words")

def delete_word(session: SessionDep, word_id: int, user_id: int):
	try:
		words.delete_word(session, word_id, user_id)
		return responses.WORD_DELETED_SUCCESSFULLY()
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

def update_word(session: SessionDep, word_id: int, word: Word, user_id: int):
	try:
		response = words.update_word(session, word_id, word, user_id)
		return Response(status_code=200)
	except exceptions.ValidationException as e:
		raise HTTPException(status_code=400, detail=str(e))

def get_random_words(session: SessionDep, quantity: int):
	try:
		return words.get_random_words(session, quantity)
	except Exception as e:
		raise HTTPException(status_code=404, detail="Could not retrieve random word(s)")