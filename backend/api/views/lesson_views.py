from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import LessonSerializerV1
from course.models import Lesson
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = LessonSerializerV1


class LessonListCreate(ListCreateAPIView):
  queryset = Lesson.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return LessonSerializerV1

    return most_recent_serializer
  

class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Lesson.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return LessonSerializerV1

    return most_recent_serializer
