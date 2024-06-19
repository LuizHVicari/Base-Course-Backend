from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.utils.pagination.pagination_classes import StandardPagination
from course.models import Course
from api.serializers import CourseSerializerV1


most_recent_serializer = CourseSerializerV1


class CourseListCreate(ListCreateAPIView):
  queryset = Course.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination


  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CourseSerializerV1
    return most_recent_serializer 
  

class CourseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Course.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CourseSerializerV1
    return most_recent_serializer 
  
  