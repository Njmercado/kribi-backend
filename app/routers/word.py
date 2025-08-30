from fastapi import APIRouter, Query, Path, Body
from app.service import words
from app.db import SessionDep
from typing import Annotated
from app.model.word import Word

router = APIRouter(
  prefix="/word",
)

@router.get("/id/{word_id}")
def get_word_by_id(session: SessionDep, word_id: int):
  return words.get_word_by_id(session, word_id)

@router.get("/{word}")
def get_word(session: SessionDep, word: Annotated[str, Path(min_length=1)]):
	return words.get_word(session, word)

@router.get("/filter/{letter}")
def get_filtered_words_by_letter(session: SessionDep, letter: Annotated[str, Path(max_length=2)]):
	return words.get_all_words_from_letter(session, letter)

@router.get("/search/{substring}")
def search_words(session: SessionDep, substring: Annotated[str, Path(min_length=3)]):
	return words.search_words(session, substring)

@router.put("/{word_id}")
def update_word(session: SessionDep, word_id: int, word: Annotated[Word, Body(embed=True)]):
	return words.update_word(session, word_id, word)

@router.delete("/{word_id}")
def delete_word(session: SessionDep, word_id: int):
	return words.delete_word(session, word_id)

@router.post("/")
def create_word(session: SessionDep, word: Annotated[Word, Body(embed=True)]):
	return words.create_word(session, word)
