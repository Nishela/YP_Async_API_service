import asyncio
from random import randint

import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient

from src.core import REDIS_CONFIG, PROJECT_NAME, ELASTIC_CONFIG
from src.main import app
from src.models import Genre, Film, Person
from tests.functional.utils import clean_index, RoleTypes
from .settings import SERVICE_URL
from .testdata.factories import GenreFactory, FilmFactory, PersonFactory


@pytest_asyncio.fixture(scope='session', autouse=True)
async def es_client():
    """Фикстура создания коннекта Elasticsearch"""
    client = AsyncElasticsearch(ELASTIC_CONFIG)
    yield client
    await client.close()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def redis():
    """Фикстура создания коннекта redis"""
    redis.redis = await aioredis.from_url(REDIS_CONFIG, encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis.redis), prefix=f'test_{PROJECT_NAME}_cache')
    yield redis.redis
    await redis.redis.close()


@pytest_asyncio.fixture(scope='session')
async def fastapi_client():
    """Фикстура создания коннекта fastapi"""
    client = AsyncClient(app=app, base_url=SERVICE_URL)
    yield client
    await client.aclose()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def drop_indexes(es_client):
    """Фикстура удаления индексов из Elasticsearch после завершения тестирования"""
    models = (Genre, Film, Person,)
    yield
    for model in models:
        await es_client.indices.delete(index=model.ModelConfig.es_index)


@pytest_asyncio.fixture(autouse=True)
async def drop_cache(redis):
    """Фикстура очистки кеша после каждого теста"""
    yield redis
    await redis.flushall()


@pytest_asyncio.fixture
async def create_list_genres():
    """Фикстура создания списка жанров"""
    genres = await GenreFactory.async_create_batch(randint(1, 10))
    yield genres
    await clean_index(genres)


@pytest_asyncio.fixture
async def create_one_genre():
    """Фикстура создания одного жанра"""
    genre = await GenreFactory.async_create()
    yield genre
    await clean_index(genre)


@pytest_asyncio.fixture
async def create_list_films():
    """Фикстура создания списка фильмов"""
    films = await FilmFactory.async_create_batch(randint(1, 10))
    yield films
    await clean_index(films)


@pytest_asyncio.fixture
async def create_one_film(create_list_genres, create_list_persons):
    """Фикстура для создания фильма. Для фильма создаются жанры и персоны.
    Передаются в фабрику фильмов для создания фильма"""
    genres = [genre.__dict__ for genre in create_list_genres]
    actors = [person.get_short() for person in create_list_persons if RoleTypes.ACTOR.value in person.role]
    writers = [person.get_short() for person in create_list_persons if RoleTypes.WRITER.value in person.role]
    directors = [person.get_short() for person in create_list_persons if RoleTypes.DIRECTOR.value in person.role]
    film = await FilmFactory.async_create(genre=genres, actors=actors, writers=writers, directors=directors)

    yield film
    await clean_index(film)


@pytest_asyncio.fixture
async def create_one_person(create_list_films):
    """Фикстура создания одной персоны с привязанными к ней фильмами"""
    films = create_list_films
    film_ids = [film.id for film in films]
    person = await PersonFactory.async_create(film_ids=film_ids)
    yield person
    await clean_index(person)


@pytest_asyncio.fixture
async def create_list_persons():
    """Фикстура создания списка персон"""
    persons = await PersonFactory.async_create_batch(randint(1, 10))
    yield persons
    await clean_index(persons)