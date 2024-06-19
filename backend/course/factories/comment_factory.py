import factory

from backend.faker_base import faker
from course.models import Comment
from .lesson_factory import LessonFactory
from .user_factory import UserFactory


class CommentFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Comment

  user = factory.SubFactory(UserFactory)
  lesson = factory.SubFactory(LessonFactory)
  text = factory.LazyAttribute(lambda _: faker.text())
  stars = factory.LazyAttribute(lambda _: faker.random_int(min=0, max=5))
