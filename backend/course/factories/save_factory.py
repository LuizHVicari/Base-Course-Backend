import factory

from course.models import Save
from .lesson_factory import LessonFactory
from .user_factory import UserFactory


class SaveFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Save

  user = factory.SubFactory(UserFactory)
  lesson = factory.SubFactory(LessonFactory)