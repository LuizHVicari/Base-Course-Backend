from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import Http404

from api.utils.pagination.pagination_classes import StandardPagination
from course.models import Course, Lesson
from api.serializers import CourseSerializerV1


most_recent_serializer = CourseSerializerV1


class CourseListCreate(ListCreateAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination


  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CourseSerializerV1
    return most_recent_serializer 
  

  def get_queryset(self):
    queryset = Course.objects.all()

    title = self.request.query_params.get('title')
    category = self.request.query_params.get('category')
    max_lessons = self.request.query_params.get('max_lessons')
    min_lessons = self.request.query_params.get('min_lessons')

    if title != None:
      queryset = queryset.filter(title__icontains=title)
    
    if category != None:
      queryset = queryset.filter(category__name__icontains=category)

    if max_lessons != None:
      max_lessons = int(max_lessons)
      queryset = queryset.annotate(
        lesson_count=Count('lesson')).filter(
          lesson_count__lte=max_lessons)

    if min_lessons != None:
      min_lessons = int(min_lessons)
      queryset = queryset.annotate(
        lesson_count=Count('lesson')).filter(
          lesson_count__gte=min_lessons)
    
    if not queryset: raise Http404
    return queryset.order_by('-updated_at')
  

class CourseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CourseSerializerV1
    return most_recent_serializer 
  
  
  def get_object(self):
    title = self.kwargs.get('title')
    if title != None:
      return get_object_or_404(Course, title=title)
    return get_object_or_404(Course, pk=self.kwargs.get('pk'))
    
  
  