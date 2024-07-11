import factory
from datetime import timedelta

from backend.faker_base import faker 
from course.models import Category

class CategoryFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Category

  name = factory.LazyAttribute(lambda _: faker.unique.word())
  description = factory.LazyAttribute(lambda _: faker.text())
  color = factory.LazyAttribute(lambda _: faker.hex_color())
