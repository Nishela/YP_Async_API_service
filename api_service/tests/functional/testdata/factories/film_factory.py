import factory
from factory import fuzzy

from src.models import models
from .base_factory import ElasticBaseFactory

__all__ = (
    'FilmFactory',
)


class FilmFactory(ElasticBaseFactory):
    """Фабрика жанров. Используется базовая модель жанров.
    Уникальность сгенерированных значений контролирует metaclass MetaModel
    """
    id = factory.Faker('uuid4')
    title = factory.Faker('company')
    imdb_rating = fuzzy.FuzzyDecimal(0, 10, precision=3)
    description = factory.Faker('paragraph')
    genre = factory.ListFactory()
    actors = factory.ListFactory()
    writers = factory.ListFactory()
    directors = factory.ListFactory()

    class Meta:
        model = models.Film
