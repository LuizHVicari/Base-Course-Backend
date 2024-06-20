import factory

from backend.faker_base import faker
from course.models import Lesson
from .course_factory import CourseFactory
from .user_factory import UserFactory


class LessonFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Lesson

  title = factory.LazyAttribute(lambda _: faker.sentence())
  description = factory.LazyAttribute(lambda _: faker.text())
  course = factory.SubFactory(CourseFactory)
  cover = factory.django.ImageField(color=faker.hex_color())
  video = factory.django.FileField(filename='video.mp4')
  text = factory.LazyAttribute(lambda _: faker.text())
  author = factory.SubFactory(UserFactory)