from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import CategorySerializerV1
from course.models import Category
from api.utils.pagination.pagination_classes import StandardPagination


most_recent_serializer = CategorySerializerV1

class CategoryListCreate(ListCreateAPIView):
  queryset = Category.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]
  pagination_class = StandardPagination

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CategorySerializerV1
    
    return most_recent_serializer
  

class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
  queryset = Category.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly, ]

  def get_serializer_class(self):
    if self.request.version == 'v1':
      return CategorySerializerV1
    
    return most_recent_serializer

  