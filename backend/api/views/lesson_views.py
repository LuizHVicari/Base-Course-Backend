from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import Http404

from api.serializers import LessonSerializerV1
from course.models import Lesson
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = LessonSerializerV1


class LessonListCreate(ListCreateAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return LessonSerializerV1

    return most_recent_serializer
  
  def get_queryset(self):
    queryset = Lesson.objects.all()

    course = self.request.query_params.get('course')
    title = self.request.query_params.get('title')
    author = self.request.query_params.get('author')

    if course != None:
      queryset = queryset.filter(course__title__icontains=course)
    if title != None:
      queryset = queryset.filter(title__icontains=title)
    if author != None:
      queryset = queryset.filter(author__username__icontains=author)
    if not queryset: raise Http404
    return queryset.order_by('-updated_at')
  

class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return LessonSerializerV1

    return most_recent_serializer
  

  def get_object(self):
    title = self.kwargs.get('title')
    if title is not None:
      return get_object_or_404(Lesson, title=title)
    return get_object_or_404(Lesson, pk=self.kwargs.get('pk'))

