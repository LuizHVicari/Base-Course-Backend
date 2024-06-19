import factory

from backend.faker_base import faker
from course.models import Course
from .category_factory import CategoryFactory


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: faker.text())
    category = factory.SubFactory(CategoryFactory)
    cover = factory.django.ImageField(color=faker.hex_color())