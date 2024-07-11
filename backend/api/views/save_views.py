from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import SaveSerializerV1
from course.models import Save
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = SaveSerializerV1


class SaveListCreate(ListCreateAPIView):
  queryset = Save.objects.all()
  permission_classes = [IsAuthenticated, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return SaveSerializerV1

    return most_recent_serializer
  

class SaveRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Save.objects.all()
  permission_classes = [IsAuthenticated, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return SaveSerializerV1

    return most_recent_serializer