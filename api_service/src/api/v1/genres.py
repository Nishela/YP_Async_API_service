import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services import GenreService, get_genre_service, GenresService, get_genres_service

router = APIRouter()


class Genre(BaseModel):
    id: uuid.UUID
    name: str


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return Genre(id=genre.id, name=genre.name)


@router.get('', response_model=list[Genre])
async def all_genres(genres_service: GenresService = Depends(get_genres_service)) -> list[Genre]:
    genres = await genres_service.get_all_data()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return [Genre(id=genre.id, name=genre.name) for genre in genres]
