from db import SessionDep
from model.word import Word
from sqlmodel import select
from fastapi import exceptions
from datetime import datetime
from sqlalchemy.orm import load_only 
from model.user import User
from utils.words import transform_word_to_regexp

def get_word_by_id(session: SessionDep, word_id: str) -> Word: 
	return session.exec(
		select(Word)
  	.where(Word.id == word_id, Word.deleted == False)
		.options(load_only(Word.word, Word.definitions, Word.translations, Word.type))
	).first()

def get_word(session: SessionDep, word: str) -> Word:
	return session.exec(select(Word).where(Word.word == word, Word.deleted == False)).one()

def get_all_words_from_letter(session: SessionDep, letter: str):
	return session.exec(select(Word).where(Word.word.startswith(letter), Word.deleted == False)).all()

def get_all_words_from_search(session: SessionDep, subs: str):
	return session.exec(
  	select(Word)
   	.where(
			Word.word.op('~')(transform_word_to_regexp(subs)),
      Word.deleted == False
    )
  ).all()

def delete_word(session: SessionDep, word_id: int):
	found_word = session.exec(select(Word).where(Word.id == word_id, Word.deleted == False)).first()
	if found_word:
		found_word.deleted = True
		session.add(found_word)
		session.commit()
	else:
		raise exceptions.ValidationException("Word not found")

def create_word(session: SessionDep, word: Word, user: User):
	if not session.exec(select(Word).where(Word.word == word.word)).first():
		word.created_by = user.id
		word.updated_by = user.id
		session.add(word)
		session.commit()
	else:
		raise exceptions.ValidationException("Word already exists")

def update_word(session: SessionDep, word_id: int, word: Word):
	found_word = session.exec(select(Word).where(Word.id == word_id, Word.deleted == False)).first()
	if found_word:
		found_word.word = word.word or found_word.word
		found_word.definitions = word.definitions or found_word.definitions
		found_word.type = word.type or found_word.type
		found_word.translations = word.translations or found_word.translations
		found_word.updated_at = datetime.now()
		session.add(found_word)
		session.commit()
		return found_word
	else:
		raise exceptions.ValidationException("Word not found")
