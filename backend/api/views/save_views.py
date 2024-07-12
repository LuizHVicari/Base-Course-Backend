from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import SaveSerializerV1
from course.models import Save
from api.utils.pagination.pagination_classes import StandardPagination
from api.utils.permissions import IsStaffOrOwner


most_recent_serializer = SaveSerializerV1


class SaveListCreate(ListCreateAPIView):
  permission_classes = [IsAuthenticated, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return SaveSerializerV1

    return most_recent_serializer
  

  def get_queryset(self):
    if self.request.user.is_staff:
      queryset = Save.objects.all()
    else:
      queryset = Save.objects.filter(user=self.request.user)
    return queryset
  

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context
  

class SaveRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAuthenticated, IsStaffOrOwner,]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return SaveSerializerV1
    
    return most_recent_serializer
  

  def get_queryset(self):
    if self.request.user.is_staff:
      queryset = Save.objects.all()
    else:
      queryset = Save.objects.filter(user=self.request.user)
    return queryset