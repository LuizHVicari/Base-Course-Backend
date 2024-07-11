import factory
from django.contrib.auth.models import User

from backend.faker_base import faker


class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = User

  username = factory.LazyAttribute(lambda _: faker.unique.user_name())
  email = factory.LazyAttribute(lambda _: faker.email())
  password = factory.LazyAttribute(lambda _: faker.password())
  first_name = factory.LazyAttribute(lambda _: faker.first_name())
  last_name = factory.LazyAttribute(lambda _: faker.last_name())
