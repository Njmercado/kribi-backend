from app.data import words
from app.db import SessionDep
from fastapi import exceptions, Response, HTTPException

from app.model.word import Word

def get_word(session: SessionDep, word: str):
	try:
		return words.get_word(session, word)
	except Exception as e:
		print('Exception: ', e)
		return HTTPException(status_code=404, detail="Word not found")

def get_word_by_id(session: SessionDep, word_id: int):
	try:
		return words.get_word_by_id(session, word_id)
	except Exception as e:
		print('Exception: ', e)
		return HTTPException(status_code=404, detail=f"Error retrieving word: {e}")

def get_all_words_from_letter(session: SessionDep, letter: str):
	try:
		return words.get_all_words_from_letter(session, letter)
	except Exception as e:
		print('Exception: ', e)
		return HTTPException(status_code=404, detail="Words not found")

def search_words(session: SessionDep, substring: str):
	try:
		return words.get_all_words_from_search(session, substring)
	except Exception as e:
		print('Exception: ', e)
		return HTTPException(status_code=404, detail="Words not found")

def delete_word(session: SessionDep, word_id: int):
	try:
		words.delete_word(session, word_id)
		return Response(status_code=200, content=f"Word with id '{word_id}' deleted successfully :)")
	except exceptions.ValidationException as e:
		print('Exception: ', e)
		return HTTPException(status_code=404, detail=str(e))
	except Exception as e:
		print('Exception: ', e)
		return HTTPException(status_code=400, detail=f"Error deleting word: {e}")

def create_word(session: SessionDep, word: Word):
	try:
		words.create_word(session, word)
		return Response(status_code=201, content=f"Word '{word.word}' created successfully :)")
	except exceptions.ValidationException as e:
		print('Exception: ', e)
		return HTTPException(status_code=400, detail=str(e))

def update_word(session: SessionDep, word_id: int, word: Word):
	try:
		response = words.update_word(session, word_id, word)
		return Response(status_code=200, content=f"Word '{response.word}' updated successfully :)")
	except exceptions.ValidationException as e:
		print('Exception: ', e)
		return HTTPException(status_code=400, detail=str(e))