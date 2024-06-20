from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import WatchedSerializerV1
from course.models import Watched
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = WatchedSerializerV1


class WatchedListCreate(ListCreateAPIView):
  queryset = Watched.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return WatchedSerializerV1

    return most_recent_serializer
  

class WatchedRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Watched.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return WatchedSerializerV1

    return most_recent_serializer