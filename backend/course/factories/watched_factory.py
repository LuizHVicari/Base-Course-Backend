import factory

from backend.faker_base import faker
from course.models import Watched
from .lesson_factory import LessonFactory
from .user_factory import UserFactory


class WatchedFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Watched

  user = factory.SubFactory(UserFactory)
  lesson = factory.SubFactory(LessonFactory)
  watched_time = factory.LazyAttribute(lambda _: faker.random_int(min=0, max=100))
