from fastapi import APIRouter, Depends, Path, Body, Query
from service import words
from db import SessionDep
from typing import Annotated
from model.word import Word
from model.user import User
from dependencies.auth import (
  get_current_active_user, 
  CreateWordRequired, 
  EditWordRequired, 
  DeleteWordRequired,
)

router = APIRouter(
  prefix="/word",
  tags=["words"]
)

# Public
@router.get("/id/{word_id}")
def get_word_by_id(session: SessionDep, word_id: int):
  return words.get_word_by_id(session, word_id)

@router.get("/filter/{letter}")
def get_filtered_words_by_letter(
  session: SessionDep, 
  letter: Annotated[str, Path(max_length=2)], 
  page: int = 1, 
  limit: int = 10
):
  """Get words filtered by letter with pagination - Public access"""
  return words.get_all_words_from_letter(session, letter, page, limit)

@router.get("/search")
def search_words(session: SessionDep, word: Annotated[str, Query(min_length=3, description="Search term")]):
  """Search words by substring or exact match - Public access"""
  return words.search_words(session, word)

@router.get("/random")
def get_random_words(session: SessionDep, quantity: int = Query(1, ge=1, le=10)):
  """Get a random word - Public access"""
  return words.get_random_words(session, quantity)

@router.get("/{word}")
def get_word(session: SessionDep, word: Annotated[str, Path(min_length=1)]):
  return words.get_word(session, word)

# Private endpoints
@router.post("/", dependencies=[CreateWordRequired])
def create_word(
  session: SessionDep, 
  word: Annotated[Word, Body()],
  current_user: User = Depends(get_current_active_user)
):
  """Create a new word - Requires CREATE_WORD entitlement or admin role"""
  return words.create_word(session, word, current_user)

@router.put("/{word_id}", dependencies=[EditWordRequired])
def update_word(
  session: SessionDep, 
  word_id: int, 
  word: Annotated[Word, Body()],
  current_user: User = Depends(get_current_active_user)
):
  """Update an existing word - Requires EDIT_WORD entitlement or admin role"""
  return words.update_word(session, word_id, word)

@router.delete("/{word_id}", dependencies=[DeleteWordRequired])
def delete_word(
  session: SessionDep, 
  word_id: int,
  current_user: User = Depends(get_current_active_user)
):
  """Delete a word - Requires DELETE_WORD entitlement or admin role"""
  return words.delete_word(session, word_id, current_user.id)
