from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404

from api.serializers import WatchedSerializerV1
from course.models import Watched
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = WatchedSerializerV1


class WatchedListCreate(ListCreateAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return WatchedSerializerV1

    return most_recent_serializer
  
  def get_queryset(self):
    queryset = Watched.objects.all()
    lesson : str | None = self.request.query_params.get('lesson')
    if lesson != None:
      queryset = queryset.filter(lesson__title__icontains=lesson)
    
    if not queryset: raise Http404
    return queryset.order_by('-updated_at')
  

class WatchedRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Watched.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return WatchedSerializerV1

    return most_recent_serializer